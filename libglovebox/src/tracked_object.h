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

#ifndef TRACKED_OBJECT_H_NHI265BF
#define TRACKED_OBJECT_H_NHI265BF

#include "ofMatrix4x4.h"

struct tracked_object {
	tracked_object() : id(-1), frame_last_seen(0) {}
	virtual ~tracked_object() {}
	
	int id;
	ofMatrix4x4 model_view_matrix;
	unsigned long frame_last_seen;
	
	bool operator==(const tracked_object& o) {
		return id == o.id;
	}
};

#endif /* end of include guard: TRACKED_OBJECT_H_NHI265BF */
