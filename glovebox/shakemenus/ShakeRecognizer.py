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

"""The shake gesture recognizer module."""

from .. import libglovebox
from cocos.director import director

class ShakeRecognizer(object):
	"""A shake gesture recognizer recognizes a shake gesture given a series of positions in 3D space.
	
	It does recognize a series of shakes in a short time."""
	def __init__(self, shake_limit = 4, frame_limit = 100):
		"""Initialize a shake gesture recognizer given an optional maximum number of shakes."""
		self.start_frame = director.app.frame
		self.frame_limit = frame_limit
		self.speed_limit = 0.25
		self.last_frame = 0
		self.frame_skip = 4
		self.former_sign = 0
		self.shake_count = 0
		self.shake_limit = shake_limit
		self.former_position = libglovebox.Vec3f(0,0,0)
		self.former_velocity = libglovebox.Vec3f(0,0,0)
	
	def reset(self):
		"""Reset the shake gesture recognizer state."""
		self.start_frame = director.app.frame
		self.former_position = libglovebox.Vec3f(0,0,0)
		self.former_velocity = libglovebox.Vec3f(0,0,0)
		self.shake_count = 0
		self.former_sign = 0
		self.last_frame = 0
	
	def update(self, position):
		"""Update the shake gesture recognizer with a new position. Return True if a shake gesture has been recognized."""
		frame = director.app.frame
		if frame - self.last_frame <= self.frame_skip:
			return False
		velocity = position - self.former_position
		speed = velocity.length()
		
		shaken = (self.shake_count > self.shake_limit)
		
		if shaken or frame - self.start_frame > self.frame_limit:
			self.reset()
			return shaken
		
		if speed > self.speed_limit:
			dot = velocity.dot(self.former_velocity)
			sign = (dot > 0) - (dot < 0) # may change in the future
			if sign != self.former_sign:
				self.shake_count += 1
			self.former_sign = sign
		
		self.last_frame = frame
		self.former_position = libglovebox.Vec3f(position.x, position.y, position.z)
		self.former_velocity = velocity
		
		return shaken

