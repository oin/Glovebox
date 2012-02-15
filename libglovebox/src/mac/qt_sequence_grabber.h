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

#ifndef QT_SEQUENCE_GRABBER_H_GTC4G19G
#define QT_SEQUENCE_GRABBER_H_GTC4G19G

#include "../camera_settings.h"
#include "qt_includes.h"

class QTSequenceGrabber {
public:
	QTSequenceGrabber(const camera_settings&);
	virtual ~QTSequenceGrabber();
	
	bool initialized;
	SeqGrabComponent sequence_grabber;
	SGChannel video_channel;
};

#endif /* end of include guard: QT_SEQUENCE_GRABBER_H_GTC4G19G */
