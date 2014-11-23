/*
 GloveBox. An experimental improvised music environment.
 Copyright (C) 2012, 2014 Jonathan Aceituno
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


#ifndef LEAP_CAMERAMAN_H_783787

#include "../cameraman.h"
#include "Leap.h"

class LeapCameraman : public Cameraman {
public:
	LeapCameraman();
	~LeapCameraman();
	bool Open(const camera_settings&);
	void ShowConfigurationWindow();
	void Close();
	void Start();
	void Stop();
	void GrabLastFrame();
	bool HasNewFrameArrived();
	unsigned char* last_frame();
private:
	void dealloc_pixels();
	bool paused_;
	unsigned char* pixelsL_;
	unsigned char* pixelsR_;
	Leap::Controller controller_;
};

#endif