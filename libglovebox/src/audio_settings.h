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

#ifndef AUDIO_SETTINGS_H_WRZRC80W
#define AUDIO_SETTINGS_H_WRZRC80W

#include "audio_device.h"

struct audio_settings {
	audio_settings() : sample_rate(44100), buffer_size(512) {}
	audio_device input_device;
	audio_device output_device;
	int nb_output_channels() const { return output_device.nb_output_channels; }
	int nb_input_channels() const { return input_device.nb_input_channels; }
	int sample_rate;
	int buffer_size;
	// int buffer_nb;
};

#endif /* end of include guard: AUDIO_SETTINGS_H_WRZRC80W */
