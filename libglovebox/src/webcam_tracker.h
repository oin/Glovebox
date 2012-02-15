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

#ifndef WEBCAM_TRACKER_H_KB63FLDH
#define WEBCAM_TRACKER_H_KB63FLDH

#include "camera_settings.h"
#include "tracked_object.h"
#include <map>
#include "ofMatrix4x4.h"

class Cameraman;
class GlTexture;

namespace ARToolKitPlus {
	class TrackerSingleMarker;
}

class WebcamTracker {
public:
	WebcamTracker();
	virtual ~WebcamTracker();
	bool Open(const camera_settings&);
	void ShowConfigurationWindow();
	bool is_open() { return is_open_; }
	void Close();
	void Start();
	void Stop();
	bool Update(unsigned long);
	void DrawCurrentFrame(float w, float h);
	ofVec2f ProjectToNormalizedScreen(const ofMatrix4x4&);
	
	std::map<int, tracked_object> objects;
	ofMatrix4x4 projection_matrix;
	
	int image_width, image_height;
private:
	bool is_open_;
	Cameraman* cameraman_;
	ARToolKitPlus::TrackerSingleMarker* tracker_;
	GlTexture* texture_;
};

#endif /* end of include guard: WEBCAM_TRACKER_H_KB63FLDH */
