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

#ifndef CAMERA_SETTINGS_H_3W674EU4
#define CAMERA_SETTINGS_H_3W674EU4

#include <string>

struct camera_settings {
	camera_settings() : image_width(640), image_height(480), desired_framerate(60) {}
	camera_settings(unsigned int w, unsigned int h, unsigned int f) : image_width(w), image_height(h), desired_framerate(f) {}
	unsigned int image_width;
	unsigned int image_height;
	unsigned int desired_framerate;
	std::string calibration_file;
};

#endif /* end of include guard: CAMERA_SETTINGS_H_3W674EU4 */
