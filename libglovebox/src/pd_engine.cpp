/*
 GloveBox. An experimental improvised music environment.
 Copyright (C) 2012 Jonathan Aceituno
 http://glovebox.oin.name
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "pd_engine.h"
extern "C" {
	#include "z_libpd.h"
}
#include <cstdio>
#include <fstream>
#include <iostream>
#include <boost/filesystem.hpp>
#include "pd_patch.h"

namespace {
	void PrintFromPd(const char* s) {
		std::cout << "(pd) " << s << std::endl;
	}
	static const char* ServerPdPatchFileContents = /*"#N canvas 0 22 450 300 10;\n\
#X obj 145 103 osc~ 440;\n\
#X obj 156 178 dac~;\n\
#X obj 256 50 loadbang;\n\
#X msg 258 75 HELLO;\n\
#X obj 262 104 print;\n\
#X connect 0 0 1 0;\n\
#X connect 0 0 1 1;\n\
#X connect 2 0 3 0;\n\
#X connect 3 0 4 0;\n\
";*//*"#N canvas 521 529 450 300 10;\
#X text 7 5 GloveBox audio framework;\
#X obj 21 201 catch~ master;\
#X obj 25 260 dac~;\
#X obj 21 230 *~ 0.3;\
#X msg 328 66 \\; pd dsp \\$1;\
#X obj 328 41 tgl 15 0 empty empty empty 17 7 0 10 -262144 -1 -1 1\
1;\
#X connect 1 0 3 0;\
#X connect 3 0 2 0;\
#X connect 3 0 2 1;\
#X connect 5 0 4 0;\
"*/"#N canvas 669 217 261 305 10;\
#X obj 21 201 catch~ master;\
#X obj 25 260 dac~;\
#X obj 21 230 *~ 0.3;\
#X obj 24 25 adc~ 1 2 3 4 5 6 7 8;\
#X obj 24 52 send~ in1;\
#X obj 33 74 send~ in2;\
#X obj 46 93 send~ in3;\
#X obj 58 113 send~ in4;\
#X obj 130 120 send~ in8;\
#X obj 126 98 send~ in7;\
#X obj 112 77 send~ in6;\
#X obj 95 52 send~ in5;\
#X connect 0 0 2 0;\
#X connect 2 0 1 0;\
#X connect 2 0 1 1;\
#X connect 3 0 4 0;\
#X connect 3 1 5 0;\
#X connect 3 2 6 0;\
#X connect 3 3 7 0;\
#X connect 3 4 11 0;\
#X connect 3 5 10 0;\
#X connect 3 6 9 0;\
#X connect 3 7 8 0;\
";
}

PdEngine::PdEngine() : ticks_per_buffer_(0), input_buffer_(0), server_patch_handle_(0) {
	
}

PdEngine::~PdEngine() {
	Close();
}

bool PdEngine::Open(const audio_settings& s) {
	if(input_buffer_)
		delete[] input_buffer_;
	
	boost::mutex::scoped_lock lock(mutex_);
	
	// Calculate the number of ticks per buffer, given a buffer size and the block size wanted by pd
	int block_size = libpd_blocksize();
	ticks_per_buffer_ = s.buffer_size / block_size;
	
	// Set a print hook
	libpd_printhook = (t_libpd_printhook)PrintFromPd;
	
	// Initialize the pd subsystem
	libpd_init();
	int err = libpd_init_audio(s.nb_input_channels(), s.nb_output_channels(), s.sample_rate);
	if(err != 0) return false;
	
	// Create a temporary file containing the server pd patch
	// (tmpnam is bad for your health but...)
	std::string temp_file_name(tmpnam(NULL));
	temp_file_name += ".pd";
	{
		std::ofstream temp_file(temp_file_name.c_str());
		temp_file << ServerPdPatchFileContents;
	}
	// Decompose the temporary file name
	boost::filesystem::path temp_file_path(temp_file_name);
	std::string dirname = temp_file_path.parent_path().string();
	std::string basename = temp_file_path.filename().string();
	
	// Load the patch into pd
	server_patch_handle_ = libpd_openfile(basename.c_str(), dirname.c_str());
	
	// Delete the temporary file
	remove(temp_file_name.c_str());
	
	if(server_patch_handle_ == NULL)
		return false;
	
	return true;
}

void PdEngine::Close() {
	Stop();
	// if(input_buffer_) {
	// 	delete[] input_buffer_;
	// 	input_buffer_ = 0;
	// }
}

void PdEngine::Start() {
	boost::mutex::scoped_lock lock(mutex_);
	libpd_start_message(MaximumPdMessageLength);
	libpd_add_float(1.0f);
	libpd_finish_message("pd", "dsp");
}

void PdEngine::Stop() {
	boost::mutex::scoped_lock lock(mutex_);
	libpd_start_message(MaximumPdMessageLength);
	libpd_add_float(0.0f);
	libpd_finish_message("pd", "dsp");
}

void PdEngine::Process(const float* input, float* output) {
	boost::mutex::scoped_lock lock(mutex_);
	libpd_process_float(ticks_per_buffer_, const_cast<float*>(input), output);
}

std::string PdEngine::OpenPatch(std::string filename) {
	boost::mutex::scoped_lock lock(mutex_);
	PdPatch* new_patch = 0;
	try {
		new_patch = new PdPatch(filename, *this);
	} catch(int) {
		return std::string();
	}
	std::string name = new_patch->name();
	patches_[name] = PdPatchPtr(new_patch);
	return name;
}

void PdEngine::ClosePatch(std::string name) {
	boost::mutex::scoped_lock lock(mutex_);
	if(patches_.count(name) > 0) {
		patches_.erase(name);
	}
}

void PdEngine::SendToPatch(std::string name, std::string key, float value) {
	boost::mutex::scoped_lock lock(mutex_);
	if(patches_.count(name) > 0)
		patches_[name]->SendMessage(key, value);
}

void PdEngine::SendToPatch(std::string name, std::string key, std::string value) {
	boost::mutex::scoped_lock lock(mutex_);
	if(patches_.count(name) > 0)
		patches_[name]->SendMessage(key, value);
}

void PdEngine::RedirectPatchAudioToMaster(std::string p) {
	boost::mutex::scoped_lock lock(mutex_);
	if(patches_.count(p) > 0)
		patches_[p]->RedirectAudioToMaster();
}

void PdEngine::RedirectPatchAudioToPatch(std::string p, std::string d) {
	boost::mutex::scoped_lock lock(mutex_);
	if(patches_.count(p) > 0 && patches_.count(d) > 0)
		patches_[p]->RedirectAudioTo(*patches_[d]);
}

void PdEngine::TurnOnPatch(std::string p) {
	boost::mutex::scoped_lock lock(mutex_);
	if(patches_.count(p) > 0)
		patches_[p]->TurnOn();
}

void PdEngine::TurnOffPatch(std::string p) {
	boost::mutex::scoped_lock lock(mutex_);
	if(patches_.count(p) > 0)
		patches_[p]->TurnOff();
}

void PdEngine::AddToSearchPath(std::string s) {
	libpd_add_to_search_path(s.c_str());
}