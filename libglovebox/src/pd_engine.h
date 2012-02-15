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

#ifndef PD_ENGINE_H_7JJKZCSX
#define PD_ENGINE_H_7JJKZCSX

#include "audio_settings.h"
#include <boost/shared_ptr.hpp>
#include <boost/thread/mutex.hpp>
#include <map>
#include <string>

static const int MaximumPdMessageLength = 32;

class PdPatch;

struct PdEngine {
	PdEngine();
	virtual ~PdEngine();
	bool Open(const audio_settings&);
	void Close();
	void Start();
	void Stop();
	void Process(const float*, float*);
	std::string OpenPatch(std::string);
	void ClosePatch(std::string);
	void SendToPatch(std::string, std::string, float);
	void SendToPatch(std::string, std::string, std::string);
	void RedirectPatchAudioToMaster(std::string);
	void RedirectPatchAudioToPatch(std::string, std::string);
	void TurnOnPatch(std::string);
	void TurnOffPatch(std::string);
	
	void AddToSearchPath(std::string);
protected:
	;
private:	
	typedef boost::shared_ptr<PdPatch> PdPatchPtr;
	
	int ticks_per_buffer_;
	float* input_buffer_;
	void* server_patch_handle_;
	std::map<std::string, PdPatchPtr> patches_;
	boost::mutex mutex_;
};

#endif /* end of include guard: PD_ENGINE_H_7JJKZCSX */