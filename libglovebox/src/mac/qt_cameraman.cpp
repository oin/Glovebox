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

// Inspired from ofVideoGrabber, http://www.openframeworks.cc, and various other sources
#include "qt_cameraman.h"
#include "qt_sequence_grabber.h"
#include <boost/detail/endian.hpp>
#include <QuickTime/QuickTimeComponents.h>
#include "QuickDrawCompatibility.h"
#include <algorithm>
#include <iostream>

Cameraman* CreateSystemCameraman() {
	return new QTCameraman;
}

namespace {
	ComponentResult QuickTimeDidGrabAFrame(SGChannel channel, short nb_buffers, Boolean* is_done, long watch_pointer) {
		ComponentResult err = SGGrabFrameComplete(channel, nb_buffers, is_done);
		bool* new_frame_flag = reinterpret_cast<bool*>(watch_pointer);
		*new_frame_flag = true;
		return err;
	}
	Boolean SeqGrabberModalFilterUPP(DialogPtr, const EventRecord *theEvent, short *, long refCon) {
		Boolean  handled = false;
		if ((theEvent->what == updateEvt) &&
			((WindowPtr) theEvent->message == (WindowPtr) refCon))
		{
			BeginUpdate ((WindowPtr) refCon);
			EndUpdate ((WindowPtr) refCon);
			handled = true;
		}
		return (handled);
	}
	#include "ofxConvert32to24.h"
}

QTCameraman::QTCameraman() : paused_(false), grabber_(0), graphics_world_(0), offscreen_graphics_world_(0), pixels_(0), new_frame_flag_(false), new_frame_grabbed_(true) {
	EnterMovies();
}

QTCameraman::~QTCameraman() {
	Close();
	ExitMovies();
}

bool QTCameraman::Open(const camera_settings& s) {
	original_settings_ = s;
	
	// Initialize the sequence grabber
	grabber_ = new QTSequenceGrabber(s);
	if(!grabber_->initialized)
		return false;
	
	// Set the dimensions for frames
	MacSetRect(&frame_rect_, 0, 0, s.image_width, s.image_height);
	
	// Set up a properly sized offscreen graphics world	
	// and then set up a graphics world
	// http://www.meandmark.com/textureloadingpart6.html
	pixels_ = new unsigned char[3 * s.image_width * s.image_height];
	
#ifdef BOOST_BIG_ENDIAN
	offscreen_graphics_world2_ = new unsigned char[4 * s.image_width * s.image_height + 32];
	offscreen_graphics_world_ = new unsigned char[3 * s.image_width * s.image_height];
	QTNewGWorldFromPtr(&graphics_world_, k32ARGBPixelFormat, &frame_rect_, NULL, NULL, 0, offscreen_graphics_world2_, 4 * s.image_width);
#else
	offscreen_graphics_world_ = new unsigned char[3 * s.image_width * s.image_height];
	QTNewGWorldFromPtr(&graphics_world_, k24RGBPixelFormat, &frame_rect_, NULL, NULL, 0, offscreen_graphics_world_, 3 * s.image_width);
#endif
	
	// LockPixels(GetGWorldPixMap(graphics_world_));
	// LockPixels(GetPortPixMap(graphics_world_));
	SetGWorld(graphics_world_, NULL);
	SGSetGWorld(grabber_->sequence_grabber, graphics_world_, nil);
	
	// Set the default device
	SelectDefaultDevice();
	
	// Set the channel usage
	OSStatus err = noErr;
	err = SGSetChannelUsage(grabber_->video_channel, seqGrabPreview | seqGrabLowLatencyCapture);
	if(err != noErr) return false;
	
	// Set a pointer to watch
	err = SGSetChannelRefCon(grabber_->video_channel, (long)&new_frame_flag_);
	if(err != noErr) return false;
	
	// Get the current video bottlenecks
	VideoBottles bottlenecks;
	bottlenecks.procCount = 9;
	err = SGGetVideoBottlenecks(grabber_->video_channel, &bottlenecks);
	if(err != noErr) return false;
	
	// Add a callback function to the bottlenecks
	callback_reference_ = NewSGGrabCompleteBottleUPP(QuickTimeDidGrabAFrame);
	bottlenecks.grabCompleteProc = callback_reference_;
	err = SGSetVideoBottlenecks(grabber_->video_channel, &bottlenecks);
	if(err != noErr) return false;
	
	// Set the channel bounds
	err = SGSetChannelBounds(grabber_->video_channel, &frame_rect_);
	if(err != noErr) return false;
	
	// Prepare the grabber as a preview
	err = SGPrepare(grabber_->sequence_grabber, true, false);
	if(err != noErr) return false;
	
	// Start the preview
	err = SGStartPreview(grabber_->sequence_grabber);
	if(err != noErr) return false;
	
	// Attempt to set the frame rate
	SGSetFrameRate(grabber_->video_channel, IntToFixed(s.desired_framerate));
	
	return true;
}

void QTCameraman::ShowConfigurationWindow() {
	bool waspaused = paused_;
	if(!waspaused)
		Stop();
	
	// Create a modal filter
	static SGModalFilterUPP g_modal_filter = NewSGModalFilterUPP(SeqGrabberModalFilterUPP);
	// Show the dialog
	SGSettingsDialog(grabber_->sequence_grabber, grabber_->video_channel, 0, nil, 0, g_modal_filter, nil);
	
	if(!waspaused)
		Start();
}

void QTCameraman::Close() {
	if(grabber_) {
		delete grabber_;
		grabber_ = 0;
	}
	DisposeSGGrabCompleteBottleUPP(callback_reference_);
	if(offscreen_graphics_world_) {
		delete[] offscreen_graphics_world_;
		offscreen_graphics_world_ = 0;
	}
	if(offscreen_graphics_world2_) {
		delete[] offscreen_graphics_world2_;
		offscreen_graphics_world2_ = 0;
	}
	if(pixels_) {
		delete[] pixels_;
		pixels_ = 0;
	}
}

void QTCameraman::Start() {
	paused_ = false;
	SGPause(grabber_->sequence_grabber, false);
}

void QTCameraman::Stop() {
	paused_ = true;
	SGPause(grabber_->sequence_grabber, true);
}

void QTCameraman::GrabLastFrame() {
	SGIdle(grabber_->sequence_grabber);
	if(new_frame_flag_) {
#ifdef BOOST_BIG_ENDIAN
		Convert32To24Pixels(offscreen_graphics_world2_, offscreen_graphics_world_, original_settings_.image_width, original_settings_.image_height);
#endif
		std::copy(offscreen_graphics_world_, offscreen_graphics_world_ + original_settings_.image_width * original_settings_.image_height * 3, pixels_);
		new_frame_flag_ = false;
		new_frame_grabbed_ = true;
	} else {
		new_frame_grabbed_ = false;
	}
}

bool QTCameraman::HasNewFrameArrived() {
	return new_frame_grabbed_;
}

void QTCameraman::SelectDefaultDevice() {
	SGDeviceList deviceList;
	SGGetChannelDeviceList(grabber_->video_channel, sgDeviceListIncludeInputs, &deviceList);
	unsigned char pascalName[64];
	unsigned char pascalNameInput[64];

	int numDevices = (*deviceList)->count;
	if(numDevices == 0)
		return;
	
	for(int i=0 ; i<numDevices; ++i) {
		SGDeviceName nameRec = (*deviceList)->entry[i];
		SGDeviceInputList deviceInputList = nameRec.inputs;
		
		int numInputs = 0;
		if(deviceInputList)
			numInputs = ((*deviceInputList)->count);

		memcpy(pascalName, (*deviceList)->entry[i].name, sizeof(char) * 64);
		memset(pascalNameInput, 0, sizeof(char)*64);
		
		if(nameRec.flags != sgDeviceNameFlagDeviceUnavailable) {
			for(int j=0; j<numInputs; j++) {
				if(deviceInputList) {
					SGDeviceInputName inputNameRec = (*deviceInputList)->entry[j];
					memcpy(pascalNameInput, inputNameRec.name, sizeof(char) * 64);
				}
				OSErr err1 = SGSetChannelDevice(grabber_->video_channel, pascalName);
				OSErr err2 = SGSetChannelDeviceInput(grabber_->video_channel, j);
				if((err1 == noErr && err2 == noErr) || ((err1 == paramErr || err1 == noErr) && (err2 == noErr || err2 == paramErr))) {
					// std::cout << "Default video device selected : " << p2cstr(pascalName) << " - " << p2cstr(pascalNameInput) << std::endl;
					return;
				}
			}
		}
	}
}

unsigned char* QTCameraman::last_frame() {
	return pixels_;
}