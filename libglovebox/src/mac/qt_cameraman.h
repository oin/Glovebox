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

#ifndef QT_CAMERAMAN_H_16ESD574
#define QT_CAMERAMAN_H_16ESD574

#include "../cameraman.h"
#include "qt_includes.h"

class QTSequenceGrabber;

class QTCameraman : public Cameraman {
public:
	QTCameraman();
	~QTCameraman();
	bool Open(const camera_settings&);
	void ShowConfigurationWindow();
	void Close();
	void Start();
	void Stop();
	void GrabLastFrame();
	bool HasNewFrameArrived();
	unsigned char* last_frame();
protected:
	void SelectDefaultDevice();
private:
	bool paused_;
	camera_settings original_settings_;
	QTSequenceGrabber* grabber_;
	Rect frame_rect_;
	GWorldPtr graphics_world_;
	unsigned char* offscreen_graphics_world_;
	unsigned char* offscreen_graphics_world2_;
	unsigned char* pixels_;
	bool new_frame_flag_;
	bool new_frame_grabbed_;
	SGGrabCompleteBottleUPP callback_reference_;
};

#endif /* end of include guard: QT_CAMERAMAN_H_16ESD574 */
