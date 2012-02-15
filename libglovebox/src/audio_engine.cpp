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

#include "audio_engine.h"
#include "pd_engine.h"
#include "ofMath.h"

AudioEngine::AudioEngine() : audio_(0), pd_(new PdEngine), is_open_(false), started_(false), bsize_(0) {
	Pa_Initialize();
}

AudioEngine::~AudioEngine() {
	Close();
	Pa_Terminate();
}

namespace {
	int AudioEngineCallback(const void* input_buffer, void* output_buffer, unsigned long, const PaStreamCallbackTimeInfo*, PaStreamCallbackFlags, void* data) {
		// data is an audio engine
		AudioEngine* me = static_cast<AudioEngine*>(data);
		me->Process(static_cast<const float*>(input_buffer), static_cast<float*>(output_buffer));
		return 0;
	}
}

bool AudioEngine::Open(const audio_settings& s) {
	if(is_open_)
		Close();
	
	PaStreamParameters input_parameters;
	input_device = s.input_device;
	input_parameters.device = s.input_device.id;
	input_parameters.channelCount = s.nb_input_channels();
	input_parameters.sampleFormat = paFloat32;
	input_parameters.hostApiSpecificStreamInfo = 0;
	
	PaStreamParameters output_parameters;
	output_device = s.output_device;
	output_parameters.device = s.output_device.id;
	output_parameters.channelCount = s.nb_output_channels();
	output_parameters.sampleFormat = paFloat32;
	output_parameters.hostApiSpecificStreamInfo = 0;
	
	bsize_ = next_power_of_two(s.buffer_size);
	
	PaError err = Pa_OpenStream(&audio_, (s.nb_input_channels() == 0 ? NULL : &input_parameters), (s.nb_output_channels() == 0 ? NULL : &output_parameters), s.sample_rate, bsize_, paNoFlag, &AudioEngineCallback, this);
	if(err != paNoError) return false;
	
	if(!pd_->Open(s))
		return false;
	
	is_open_ = true;
	return true;
}

void AudioEngine::Close() {
	Stop();
	Pa_AbortStream(audio_);
	is_open_ = false;
}

void AudioEngine::Start() {
	if(!is_open_)
		return;
	
	Pa_StartStream(audio_);
	pd_->Start();
	started_ = true;
}

void AudioEngine::Stop() {
	if(!is_open_)
		return;
	Pa_StopStream(audio_);
	pd_->Stop();
	started_ = false;
}

void AudioEngine::Process(const float* input, float* output) {
	if(started_)
		pd_->Process(input, output);
	else
		std::fill(output, output + bsize_, 0);
}

std::string AudioEngine::OpenPatch(std::string s) {
	if(!is_open_)
		return std::string();
	return pd_->OpenPatch(s);
}

void AudioEngine::ClosePatch(std::string s) {
	if(!is_open_)
		return;
	pd_->ClosePatch(s);
}

void AudioEngine::SendToPatchF(std::string s, std::string k, float f) {
	if(!is_open_)
		return;
	pd_->SendToPatch(s, k, f);
}

void AudioEngine::SendToPatchS(std::string s, std::string k, std::string f) {
	if(!is_open_)
		return;
	pd_->SendToPatch(s, k, f);
}

void AudioEngine::RedirectPatchAudioToMaster(std::string p) {
	if(!is_open_)
		return;
	
	pd_->RedirectPatchAudioToMaster(p);
}

void AudioEngine::RedirectPatchAudioToPatch(std::string p, std::string d) {
	if(!is_open_)
		return;
	
	pd_->RedirectPatchAudioToPatch(p, d);
}


void AudioEngine::TurnOnPatch(std::string p) {
	if(!is_open_)
		return;
	
	pd_->TurnOnPatch(p);
}

void AudioEngine::TurnOffPatch(std::string p) {
	if(!is_open_)
		return;
	
	pd_->TurnOffPatch(p);
}

void AudioEngine::AddToPatchSearchPatch(std::string p) {
	pd_->AddToSearchPath(p);
}