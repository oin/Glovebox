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

"""The main behavior module."""

import collections
from pyglet.gl import *
import sys
from cocos.director import director
from ..tools import Graphics2d
from ..shakemenus import ShakeRecognizer
from cocos.text import Label

def format_default(value):
	return "%1.2f" % value

def format_frequency(value):
	return "%dHz" % value

def format_time_ms(value):
	return "%1.2fms" % value

class BehaviorAttribute(object):
	"""A behavior attribute has a display name, a value, and a range."""
	def __init__(self):
		self.value = 0
		self.range = (0, 1)
		self.display_name = "Untitled"
		self.formatter = format_default
	
	def to_string(self):
		"""Return the attribute value as a string."""
		return self.formatter(self.value)
	
	def set(self, value):
		self.value = min(self.range[1], max(self.range[0], value))

class Behavior(object):
	"""A behavior defines the virtual part of a tracked object.
	
	A behavior can interact with its environment through 5 entry points that can be overridden :
	update_tracking -- New data arrives from the tracking subsystem.
	update -- Update the internal state.
	draw_background -- Draw the background part in 2D.
	draw_3d -- Draw the 3D part.
	draw_foreground -- Draw the foreground part in 2D."""
	def __init__(self):
		"""Initialize an empty behavior."""
		super(Behavior, self).__init__
		self.display_name = None
		self.display_name_cached = None
		self.display_name_label = Label("", font_size=8, font_name="Cabin Bold", anchor_x="center", anchor_y="bottom", color=(255, 255, 255, 255))
		self.object = None
		self.observers = collections.defaultdict(list)
		self.attributes = collections.defaultdict(BehaviorAttribute)
		self.association = None
		self.association_selection = None
		self.association_selection_shaker = ShakeRecognizer.ShakeRecognizer()
		self.association_name = "Associate"
		self.association_mode = False
	
	def init_attribute(self, name, display_name, range, option_name, default_value, formatter = None):
		self.attributes[name].display_name = display_name
		self.attributes[name].range = range
		if formatter:
			self.attributes[name].formatter = formatter
		self.attributes[name].set(director.app.options.setdefault(option_name, default_value))
	
	def max_association_selection_time(self):
		return director.app.options.setdefault('max_association_selection_time', 2)
	
	def register_for(self, notification, observer):
		"""Register for a notification type as an observer."""
		if not observer in self.observers[notification]:
			self.observers[notification].append(observer)

	def unregister_from(self, notification, observer):
		"""Stop observing a notification type."""
		try:
			self.observers[notification].remove(observer)
		except ValueError:
			pass
	
	def notify_for(self, notification, *args):
		"""Notify observers for something."""
		for observer in self.observers[notification]:
			observer.notification_arrived_for(notification, self, *args)
	
	def notification_arrived_for(self, notification, sender, *args):
		"""Handle new notifications."""
		if notification == "detached":
			self.behavior_detached(sender, *args)
	
	def behavior_detached(self, sender, *args):
		"""Handle a 'detached' notification."""
		if self.association == sender:
			self.unassociate()
	
	def will_detach(self, object):
		self.object = None
		self.notify_for("detached")
		self.has_just_detached()
		
	def did_attach(self, object):
		self.object = object
		self.has_just_attached(object)
	
	def associate(self, behavior):
		"""Start an unilateral association from this behavior to a specified behavior."""
		if self.association:
			unassociate()
		self.association = behavior
		behavior.register_for("detached", self)
		return True
	
	def unassociate(self):
		"""Stop being associated with the current associated behavior, if any."""
		if not self.association:
			return
		self.association.unregister_from("detached", self)
		self.association = None
		
	def has_just_attached(self, object):
		"""Do something when the behavior will cease to be attached to a tracked object."""
		pass
	
	def has_just_detached(self):
		"""Do something when the behavior will attach to a tracked object."""
		pass
	
	def has_object(self):
		"""Tell if the behavior is attached to a tracked object."""
		return self.object != None
		
	def draw_association(self):
		"""Draw a line between the associated behavior's object and this behavior's object."""
		if not self.association:
			return
		me_color = self.object.color + (0.5 * self.object.alpha(),)
		ass_color = self.association.object.color + (0.5 * self.association.object.alpha(),)
		mecoords, asscoords = self.object.screen_coords(), self.association.object.screen_coords()
		glLineWidth(3)
		glBegin(GL_LINES)
		glColor4f(*me_color)
		glVertex2f(mecoords.x, mecoords.y)
		glColor4f(*ass_color)
		glVertex2f(asscoords.x, asscoords.y)
		glEnd()
		glLineWidth(1)
	
	def update_tracking(self):
		pass
	
	def update(self):
		if not self.association_mode:
			return
		new_selection = None
		min_distance = sys.float_info.max
		for id in director.app.objects:
			current = director.app.objects[id]
			dist = current.translation.distance(self.object.translation)
			if current != self.object and not current.is_zombie() and dist < min_distance:
				min_distance = dist
				new_selection = current
		if self.association_selection != new_selection:
			# The selection has changed.
			self.association_selection = new_selection
			self.association_selection_shaker.reset()
		else:
			if self.association_selection and self.association_selection_shaker.update(self.object.raw_translation):
				# Associate the selection
				self.association_mode = False
				self.associate(self.association_selection.behavior)
				self.association_selection = None
	
	def draw_background(self):
		self.draw_association()
		if self.display_name != self.display_name_cached:
			self.display_name_label.element.text = self.display_name
			self.display_name_cached = self.display_name
		if self.display_name:	
			self.display_name_label.element.color = (255, 255, 255, int(self.object.alpha() * 255))
			coords = self.object.screen_coords()
			self.display_name_label.position = coords.x, coords.y + 10
			self.display_name_label.draw()
	
	def draw_3d(self):
		if self.association_mode and self.association_selection:
			self.association_selection.model_view_matrix.load_gl()
			Graphics2d.draw_rect(-1.5, -1.5, 3, 3, (0.0, 0.0, 0.0, self.object.alpha()), filled=False, line_width=2)
			Graphics2d.draw_rect(-1.5, -1.5, 3, 3, self.object.color +  (self.object.alpha() * 0.4,), filled=True)
			self.object.model_view_matrix.load_gl()
	
	def draw_foreground(self):
		pass