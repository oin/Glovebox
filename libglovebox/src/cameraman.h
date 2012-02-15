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

#ifndef CAMERAMAN_H_OG5BTAI9
#define CAMERAMAN_H_OG5BTAI9

#include "camera_settings.h"

class Cameraman {
public:
	virtual ~Cameraman() {}
	virtual bool Open(const camera_settings&) = 0;
	virtual void ShowConfigurationWindow() = 0;
	virtual void Close() = 0;
	virtual void Start() = 0;
	virtual void Stop() = 0;
	virtual void GrabLastFrame() = 0;
	virtual bool HasNewFrameArrived() = 0;
	virtual unsigned char* last_frame() = 0;
};

Cameraman* CreateSystemCameraman();

#endif /* end of include guard: CAMERAMAN_H_OG5BTAI9 */
