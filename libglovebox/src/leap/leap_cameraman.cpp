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

#include "leap_cameraman.h"
#include <iostream>

Cameraman* CreateSystemCameraman() {
	return new LeapCameraman;
}

LeapCameraman::LeapCameraman() : paused_(false), pixelsL_(0), pixelsR_(0) {

	// Set the controller policy to images
	controller_.setPolicy(Leap::Controller::POLICY_IMAGES);
}

LeapCameraman::~LeapCameraman() {
	Close();
	dealloc_pixels();
}

void LeapCameraman::dealloc_pixels() {
	if(pixelsL_) {
		free(pixelsL_);
		pixelsL_ = 0;
	}
	if(pixelsR_) {
		free(pixelsR_);
		pixelsR_ = 0;
	}
}

bool LeapCameraman::Open(const camera_settings& s) {
	dealloc_pixels();
	unsigned int imgsize = 3 * s.image_width * s.image_height;
	// Allocate images
	pixelsL_ = new unsigned char[imgsize];
	pixelsR_ = new unsigned char[imgsize];
	// Clear them
	for(unsigned int i=0; i<imgsize; ++i) {
		pixelsL_[i] = 0;
		pixelsR_[i] = 0;
	}

	return true;
}

void LeapCameraman::ShowConfigurationWindow() {
	bool waspaused = paused_;
	if(!waspaused)
		Stop();

	// Nothing.
	
	if(!waspaused)
		Start();
}

void LeapCameraman::Close() {
	dealloc_pixels();
}

void LeapCameraman::Start() {
	paused_ = false;
	
}

void LeapCameraman::Stop() {
	paused_ = true;
	
}

void LeapCameraman::GrabLastFrame() {
	Leap::Frame frame = controller_.frame();
	Leap::Image imgL = frame.images()[0];
	Leap::Image imgR = frame.images()[1];
	const unsigned char* bufferL = imgL.data();
	const unsigned char* bufferR = imgR.data();

	unsigned int imgSize = imgL.width() * imgL.height();
	for(unsigned int i=0; i<imgSize; ++i) {
		pixelsL_[i*3] = bufferL[i];
		pixelsL_[i*3+1] = bufferL[i];
		pixelsL_[i*3+2] = bufferL[i];
	}
	imgSize = imgR.width() * imgR.height();
	for(unsigned int i=0; i<imgSize; ++i) {
		pixelsR_[i*3] = bufferR[i];
		pixelsR_[i*3+1] = bufferR[i];
		pixelsR_[i*3+2] = bufferR[i];
	}
}

bool LeapCameraman::HasNewFrameArrived() {
	return true;
}

unsigned char* LeapCameraman::last_frame() {
	return pixelsL_;
}
