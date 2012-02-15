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

#include "qt_sequence_grabber.h"

QTSequenceGrabber::QTSequenceGrabber(const camera_settings& s) : initialized(false) {
	OSErr err = noErr;
	
	ComponentDescription component_desc;
	Component component_id;
	component_desc.componentType = SeqGrabComponentType;
	component_desc.componentSubType = NULL;
	component_desc.componentManufacturer = 'appl';
	component_desc.componentFlags = NULL;
	component_desc.componentFlagsMask = NULL;
	component_id = FindNextComponent(NULL, &component_desc);
	
	if(component_id == NULL) return;
	
	sequence_grabber = OpenComponent(component_id);
	
	err = GetMoviesError();	
	if(sequence_grabber == NULL || err) return;
	
	err = SGInitialize(sequence_grabber);
	if(err != noErr) return;
	
	err = SGSetDataRef(sequence_grabber, 0, 0, seqGrabDontMakeMovie);
	if(err != noErr) return;
	
	err = SGSetGWorld(sequence_grabber, 0, 0);
	if(err != noErr) return;
	
	err = SGNewChannel(sequence_grabber, VideoMediaType, &video_channel);
	if(err != noErr) return;
	
	initialized = true;
	return;
}

QTSequenceGrabber::~QTSequenceGrabber() {
	if(sequence_grabber != NULL) {
		SGStop(sequence_grabber);
		CloseComponent(sequence_grabber);
	}
}