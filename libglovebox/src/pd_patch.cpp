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

#include "pd_patch.h"
#include "pd_engine.h"
#include <boost/filesystem.hpp>
#include <boost/lexical_cast.hpp>
extern "C" {
	#include "z_libpd.h"
}

PdPatch::PdPatch(std::string file, PdEngine& e) throw(int) :  dollar_zero_(0), path_(file), engine_(e), handle_(0) {
	boost::filesystem::path path(file);
	std::string dirname = path.parent_path().string();
	std::string basename = path.filename().string();
	name_ = path.stem().string();
	
	// Load the patch into pd
	handle_ = libpd_openfile(basename.c_str(), dirname.c_str());
	
	if(handle_ == NULL)
		throw 0;
	
	dollar_zero_ = libpd_getdollarzero(handle_);
	std::string dollar_zero_str_ = boost::lexical_cast<std::string>(dollar_zero_);
	receiver_ = "glovebox";
	receiver_ += dollar_zero_str_;
	name_ += dollar_zero_str_;
}

PdPatch::~PdPatch() {
	Close();
}

void PdPatch::Close() {
	libpd_closefile(handle_);
}

void PdPatch::SendMessage(std::string key, float value) {
	libpd_start_message(MaximumPdMessageLength);
	libpd_add_float(value);
	libpd_finish_message(receiver_.c_str(), key.c_str());
}

void PdPatch::SendMessage(std::string key, std::string value) {
	libpd_start_message(MaximumPdMessageLength);
	libpd_add_symbol(value.c_str());
	libpd_finish_message(receiver_.c_str(), key.c_str());
}

void PdPatch::RedirectAudioToMaster() {
	SendMessage("redirect", "master");
}

void PdPatch::RedirectAudioTo(const PdPatch& p) {
	std::string dollar_zero_str = boost::lexical_cast<std::string>(p.dollar_zero_);
	std::string dest = "gloveboxinput";
	dest += dollar_zero_str;
	SendMessage("redirect", dest);
}

void PdPatch::TurnOn() {
	SendMessage("active", 1);
}

void PdPatch::TurnOff() {
	SendMessage("active", 0);
}