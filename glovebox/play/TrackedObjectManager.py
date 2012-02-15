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

"""The tracked object manager module."""

import cocos
from cocos.director import director
from .TrackedObject import TrackedObject

class TrackedObjectManager(object):
	"""A tracked object manager is responsible for updating every tracked object according to the tracking subsystem state."""
	
	def update_tracking(self):
		"""Update every tracked object according to the tracking subsystem."""
		for keyvalue in director.app.tracker.objects:
			object = keyvalue.data()
			id = object.id
			is_new = False
			if not director.app.objects.has_key(id):
				director.app.objects[id] = TrackedObject(id)
				is_new = True
			director.app.objects[id].update_tracking(object)
			if is_new:
				director.app.on_new_object_appears(director.app.objects[id])
	
	def update(self):
		"""Update every tracked object."""
		for id in director.app.objects:
			if not director.app.uses_filter_thread():
				director.app.objects[id].update_filter()
			director.app.objects[id].update()
	
	def draw_background(self):
		"""Draw the 2D background of every tracked object."""
		for id in director.app.objects:
			director.app.objects[id].draw_background()
	
	def draw_3d(self):
		"""Draw the 3D part of every tracked object."""
		for id in director.app.objects:
			director.app.objects[id].draw_3d()
	
	def draw_foreground(self):
		"""Draw the 2D foreground of every tracked object."""
		for id in director.app.objects:
			director.app.objects[id].draw_foreground()
	
	def change_filter(self):
		"""Change the filtering method for every tracked object."""
		for id in director.app.objects:
			director.app.objects[id].change_filter()