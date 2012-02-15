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

#ifndef SYSTEM_AUDIO_H_QZFA1V1G
#define SYSTEM_AUDIO_H_QZFA1V1G

#include "audio_device.h"

class system_audio {
public:
	system_audio();
	~system_audio();
	audio_device default_input_device();
	audio_device default_output_device();
	std::vector<audio_device> devices;
};

#endif /* end of include guard: SYSTEM_AUDIO_H_QZFA1V1G */
