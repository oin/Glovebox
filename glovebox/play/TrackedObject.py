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

from .. import libglovebox
import cocos
from cocos.director import director
import pyglet
from pyglet.gl import *
from .Behavior import Behavior
import colorsys
import random
from ..tools import Graphics2d
from .DefaultBehavior import DefaultBehavior

"""The tracked object module."""

class TrackedObject(object):
	"""A tracked object is the representation of a physical object as viewed by the application through the tracking system.
	
	It can be dynamically attached to a behavior.
	
	To determine how successful the tracking system is to sense an object, two measures are introduced :
	absent -- When the object hasn't been seen anymore for a short time, it is marked as absent.
	zombie -- When the object hasn't been seen anymore for a longer time, it is marked as zombie."""
	def __init__(self, id):
		"""Initialize a tracked object given an identifier."""
		self.id = id
		self.frame_last_seen = 0
		self.translation = libglovebox.Vec3f(0, 0, 0)
		self.raw_translation = libglovebox.Vec3f(0, 0, 0)
		self.rotation = libglovebox.Quaternion(0, 0, 0, 0)
		self.raw_rotation = libglovebox.Quaternion(0, 0, 0, 0)
		self.model_view_matrix = libglovebox.TransformationMatrix()
		self.raw_model_view_matrix = libglovebox.TransformationMatrix()
		self.behavior = None
		self.filter = director.app.filter.copy()
		self.first_update = True
		self.time_to_live = 100
		self.time_to_be = 20
		self.color = colorsys.hsv_to_rgb(random.random(), 0.5, 1.0)
		self.attach_behavior(DefaultBehavior())
	
	def attach_behavior(self, behavior):
		"""Attach a given behavior."""
		if self.behavior:
			self.behavior.will_detach(self)
		self.behavior = behavior
		if self.behavior:
			self.behavior.did_attach(self)
	
	def update_tracking(self, info):
		"""Update the object properties given the raw tracking information."""
		self.tracker_info = info
		self.frame_last_seen = info.frame_last_seen
		self.raw_model_view_matrix = info.model_view_matrix
		# Decompose the matrix in order to filter
		coords = info.model_view_matrix.decomposed()
		self.raw_translation = coords.translation
		self.raw_rotation = coords.rotation
		
		# Call the current runner
		if self.behavior:
			self.behavior.update_tracking()
	
	def update_filter(self):
		"""Update the filtered coordinates of the object."""
		# Filter
		if self.first_update:
			self.filter.reset(self.raw_translation, self.raw_rotation)
			self.first_update = False
		
		self.filter.filter(self.raw_translation, self.raw_rotation)
		
		self.translation = self.filter.translation
		self.rotation = self.filter.rotation
		self.model_view_matrix.recompose(self.translation, self.rotation)
	
	def change_filter(self):
		"""Change the filter used with the application's default one."""
		self.filter = director.app.filter.copy()
		self.filter.reset(self.raw_translation, self.raw_rotation)
	
	def update(self):
		"""If any, tell the object's behavior to update."""
		if self.behavior:
			self.behavior.update()
	
	def draw_3d(self):
		"""If any, tell the object's behavior to draw its 3D part.
		
		The drawing coordinates are relative to the object's filtered position."""
		glMatrixMode(GL_MODELVIEW)
		self.model_view_matrix.load_gl()
		if self.behavior:
			self.behavior.draw_3d()
	
	def draw_background(self):
		"""Draw a rubber band between the physical and virtual part, then tell the object's behavior to draw its 2D background if any."""
		# Draw a rubber band
		color = self.color + (0.5 * self.alpha(),)
		scoords, rscoords = self.screen_coords(), self.raw_screen_coords()
		Graphics2d.draw_line(scoords.x, scoords.y, rscoords.x, rscoords.y, color, 4)
		Graphics2d.draw_ring(scoords.x, scoords.y, 2, 6, color)
		if self.behavior:
			self.behavior.draw_background()
	
	def draw_foreground(self):
		"""Tell the object's behavior to draw its 2D foreground if any."""
		if self.behavior:
			self.behavior.draw_foreground()
	
	def raw_screen_coords(self):
		"""Return the projected 2D unfiltered position in screen coordinates."""
		w, h = director.get_window_size()
		return (libglovebox.Vec2f(0, 1) - director.app.tracker.project_to_normalized_screen(self.raw_model_view_matrix)) * libglovebox.Vec2f(-w, h)

	def screen_coords(self):
		"""Return the projected 2D filtered position in screen coordinates."""
		w, h = director.get_window_size()
		return (libglovebox.Vec2f(0, 1) - director.app.tracker.project_to_normalized_screen(self.model_view_matrix)) * libglovebox.Vec2f(-w, h)
	
	def zombie_amount(self):
		"""Return how much zombie the object is."""
		return min(max(0, director.app.frame - self.frame_last_seen), self.time_to_live) * 1.0 / self.time_to_live
	
	def absent_amount(self):
		"""Return how much absent the object is."""
		return min(max(0, director.app.frame - self.frame_last_seen), self.time_to_be) * 1.0 / self.time_to_be
	
	def is_zombie(self):
		"""Return whether the object is zombie."""
		return self.zombie_amount() == 1.0
	
	def is_absent(self):
		"""Return whether the object is absent."""
		return self.absent_amount() == 1.0
	
	def alpha(self):
		"""Return the object's desired alpha color value."""
		return min(1, 1.1 * (1 - self.zombie_amount()))
	
	def color4(self):
		"""Return the object's desired RGBA color."""
		return self.color + (self.alpha(),)
	
	def color3(self):
		"""Return the object's desired RGB color."""
		return self.color
	
	