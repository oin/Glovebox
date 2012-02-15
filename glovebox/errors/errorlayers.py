#!/usr/bin/env python
# encoding: utf-8

# GloveBox. An experimental improvised music environment.
# Copyright (C) 2012 Jonathan Aceituno
# http://glovebox.oin.name
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The error layers module."""

import cocos
from cocos.layer import Layer
from cocos.text import Label
from cocos.director import director
from cocos.actions import *

class ErrorLayer(Layer):
	"""An error layer specifies the appearance of a generic fatal error screen."""
	def __init__(self, message):
		"""Initialize an error layer."""
		super(ErrorLayer, self).__init__()
		w, h = director.get_window_size()
		
		lbl_title = Label("Fatal Error", bold=True, font_size=64, anchor_x="center", anchor_y="center", color=(255,255,255,0))
		lbl_title.position = w * 0.5, h * 0.75
		lbl_title.do(FadeIn(1))
		self.add(lbl_title)
		
		lbl_message = Label(message, anchor_x="center", anchor_y="center", font_size=12, color=(255,255,255,0))
		lbl_message.position = w * 0.5, h * 0.5
		lbl_message.do(FadeIn(1))
		self.add(lbl_message)
		
		lbl_advice = Label("Please restart the application once you have fixed the problem.", font_size=10, anchor_x="center", anchor_y="center", color=(255,255,255,0))
		lbl_advice.position = w * 0.5, h * 0.25
		lbl_advice.do(Accelerate(FadeIn(3), 2))
		self.add(lbl_advice)

class ErrorLayerAudio(ErrorLayer):
	"""An audio error layer shows an error message in case of a fatal error in the audio subsystem."""
	def __init__(self):
		"""Initialize a layer"""
		super(ErrorLayerAudio, self).__init__("Failed to get sound working. Is your sound card OK ?")

class ErrorLayerTracker(ErrorLayer):
	"""A tracker error layer shows an error message in case of a fatal error in the tracking subsystem."""
	def __init__(self):
		"""Initialize a layer"""
		super(ErrorLayerTracker, self).__init__("Failed to get tracking working. Do you have a webcam ? Is the calibration file OK ?")