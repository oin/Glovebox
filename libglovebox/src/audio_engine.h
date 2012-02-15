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

#ifndef AUDIO_ENGINE_H_5Y2WCTAE
#define AUDIO_ENGINE_H_5Y2WCTAE

#include <portaudio.h>
#include "audio_settings.h"
#include <string>

class PdEngine;

struct AudioEngine {
	AudioEngine();
	virtual ~AudioEngine();
	bool Open(const audio_settings&);
	void Close();
	void Start();
	void Stop();
	bool is_open() { return is_open_; }
	
	std::string OpenPatch(std::string);
	void ClosePatch(std::string);
	void SendToPatchF(std::string, std::string, float);
	void SendToPatchS(std::string, std::string, std::string);
	
	void RedirectPatchAudioToMaster(std::string);
	void RedirectPatchAudioToPatch(std::string, std::string);
	void TurnOnPatch(std::string);
	void TurnOffPatch(std::string);
	
	void AddToPatchSearchPatch(std::string);
	
	void Process(const float*, float*);
	
	audio_device input_device;
	audio_device output_device;
protected:
	;
private:
	PaStream* audio_;
	PdEngine* pd_;
	bool is_open_;
	bool started_;
	int bsize_;
};

#endif /* end of include guard: AUDIO_ENGINE_H_5Y2WCTAE */