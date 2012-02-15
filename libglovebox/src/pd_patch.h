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

#ifndef PD_PATCH_H_GZUL0RXC
#define PD_PATCH_H_GZUL0RXC

#include <string>

class PdEngine;

struct PdPatch {
	PdPatch(std::string, PdEngine&) throw(int);
	~PdPatch();
	std::string name() { return name_; }
	void SendMessage(std::string, float);
	void SendMessage(std::string, std::string);
	int dollar_zero() { return dollar_zero_; }
	void RedirectAudioToMaster();
	void RedirectAudioTo(const PdPatch&);
	void TurnOn();
	void TurnOff();
	void Close();
	
	int dollar_zero_;
private:
	std::string path_;
	std::string name_;
	PdEngine& engine_;
	void* handle_;
	std::string receiver_;
};

#endif /* end of include guard: PD_PATCH_H_GZUL0RXC */
