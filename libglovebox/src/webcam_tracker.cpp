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

#include "webcam_tracker.h"
#include "cameraman.h"
#include "gl_texture.h"
#include "ARToolKitPlus/TrackerSingleMarker.h"
#include <iostream>
#include "ofMath.h"
#include <OpenGL/GLU.h>

WebcamTracker::WebcamTracker() : image_width(0), image_height(0), is_open_(false), cameraman_(0), tracker_(0), texture_(0) {
	
}

WebcamTracker::~WebcamTracker() {
	if(is_open_)
		Close();
}

bool WebcamTracker::Open(const camera_settings& settings) {
	if(is_open_)
		Close();
	
	camera_settings s = settings;
	s.image_width = next_power_of_two(s.image_width);
	s.image_height = next_power_of_two(s.image_height);
	image_width = s.image_width;
	image_height = s.image_height;
	
	if(texture_)
		delete texture_;
	texture_ = new GlTexture(s.image_width, s.image_height);
	
	cameraman_ = CreateSystemCameraman();
	if(!cameraman_->Open(s))
		return false;
	
	tracker_ = new ARToolKitPlus::TrackerSingleMarker(s.image_width, s.image_height, 10, 6, 6, 6, 0);
	
	float near = 4.f;
	float far = 1000.f;
	
	
	if(s.calibration_file.empty())
		return false;
	
	try {
		tracker_->init(s.calibration_file.c_str(), near, far);
	} catch(...) {
		return false;
	}
	
	tracker_->setBorderWidth(0.125f);
	tracker_->activateAutoThreshold(true);
	tracker_->setUndistortionMode(ARToolKitPlus::UNDIST_LUT);
	tracker_->activateVignettingCompensation(true);
	tracker_->setPoseEstimator(ARToolKitPlus::POSE_ESTIMATOR_RPP);
	tracker_->setMarkerMode(ARToolKitPlus::MARKER_ID_BCH);
	tracker_->setPixelFormat(ARToolKitPlus::PIXEL_FORMAT_BGR);
	
	projection_matrix = tracker_->getProjectionMatrix();
	is_open_ = true;
	return true;
}

void WebcamTracker::Close() {
	if(texture_)
		delete texture_;
	texture_ = 0;
	cameraman_->Close();
	is_open_ = false;
}

void WebcamTracker::Start() {
	if(is_open_)
		cameraman_->Start();
}

void WebcamTracker::Stop() {
	if(is_open_)
		cameraman_->Stop();
}

void WebcamTracker::ShowConfigurationWindow() {
	if(is_open_)
		cameraman_->ShowConfigurationWindow();
}

bool WebcamTracker::Update(unsigned long frame_number) {
	if(!is_open_)
		return false;
	
	cameraman_->GrabLastFrame();
	bool new_stuff = cameraman_->HasNewFrameArrived();
	
	if(new_stuff) {
		texture_->Load(cameraman_->last_frame());
		
		int nb_markers = 0;
		ARToolKitPlus::ARMarkerInfo* info = 0;
		std::vector<int> markers = tracker_->calc(cameraman_->last_frame(), &info, &nb_markers);
		
		for(unsigned int i=0; i<markers.size(); ++i) {
			int id = markers[i];
			tracker_->selectDetectedMarker(id);
			tracked_object current = objects[id];
			current.id = id;
			current.frame_last_seen = frame_number;
			current.model_view_matrix = tracker_->getModelViewMatrix();
			objects[id] = current;
		}
	}
	
	return new_stuff;
}

void WebcamTracker::DrawCurrentFrame(float w, float h) {
	if(!is_open_)
		return;
	
	texture_->Draw(w, h);
}

ofVec2f WebcamTracker::ProjectToNormalizedScreen(const ofMatrix4x4& m) {
	// What's behind gluProject: http://www.opengl.org/resources/faq/technical/transformations.htm (9.011)
	static const GLint viewport[4] = { 0, 0, 1, 1 };
	GLdouble x = -1;
	GLdouble y = -1;
	GLdouble z = -1;

	GLdouble modelViewMatrix[16];
	GLdouble projectionMatrix[16];
	std::copy(m.getPtr(), m.getPtr() + 16, modelViewMatrix);
	std::copy(projection_matrix.getPtr(), projection_matrix.getPtr() + 16, projectionMatrix);

	gluProject(0, 0, 0, modelViewMatrix, projectionMatrix, viewport, &x, &y, &z);

	return ofVec2f(x, 1 - y);
}