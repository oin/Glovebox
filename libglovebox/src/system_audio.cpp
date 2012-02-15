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

#include "system_audio.h"
#include <portaudio.h>

system_audio::system_audio() {
	// Get every device on the planet
	int nb_devices = Pa_GetDeviceCount();
	
	if(nb_devices < 0)
		return;
	for(int i=0; i<nb_devices; ++i) {
		const PaDeviceInfo* device_info = Pa_GetDeviceInfo(i);
		audio_device device;
		device.name = device_info->name;
		device.nb_input_channels = device_info->maxInputChannels;
		device.nb_output_channels = device_info->maxOutputChannels;
		device.default_input_latency = device_info->defaultLowInputLatency;
		device.default_output_latency = device_info->defaultLowOutputLatency;
		device.default_sample_rate = device_info->defaultSampleRate;
		device.id = i;
		
		devices.push_back(device);
	}
}

system_audio::~system_audio() {}

audio_device system_audio::default_input_device() {
	int i = Pa_GetDefaultInputDevice();
	return devices[i];
}

audio_device system_audio::default_output_device() {
	int i = Pa_GetDefaultOutputDevice();
	return devices[i];
}