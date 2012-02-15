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

#ifndef AUDIO_DEVICE_H_7CFODFOS
#define AUDIO_DEVICE_H_7CFODFOS

#include <vector>
#include <string>

struct audio_device {
	audio_device() : nb_input_channels(0), nb_output_channels(0), default_input_latency(0), default_output_latency(0), default_sample_rate(44100), id(-1) {}
	std::string name;
	int nb_input_channels;
	int nb_output_channels;
	double default_input_latency;
	double default_output_latency;
	double default_sample_rate;
	int id;
	bool operator==(const audio_device& o) const {
		return id == o.id;
	}
};

#endif /* end of include guard: AUDIO_DEVICE_H_7CFODFOS */
