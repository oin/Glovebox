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

"""The play scene module."""

import cocos
from cocos.director import director
from pyglet.window import key
from cocos.layer import *
from pyglet.gl import *
from cocos.sprite import Sprite
from cocos.actions import *
from ..tools import ObjectNodes
import pyglet

class PlayScene(cocos.scene.Scene):
	"""The play scene is where the improvised interaction occurs."""
	def __init__(self):
		"""Initialize a play scene."""
		super(PlayScene, self).__init__()
		layer = PlayLayer()
		self.add(layer)
		self.messages = layer.messages
		self.schedule(layer.update)

class MessageLayer(Layer):
	"""The message layer shows a one-line message that can disappear over time."""
	def __init__(self):
		"""Initialize a message layer."""
		super(MessageLayer, self).__init__()
		w, h = director.get_window_size()
		self.text = cocos.text.HTMLLabel('<font face="Cabin Regular" color="white">...</font>', anchor_x="center", anchor_y="center")
		self.text.scale = 0
		self.add(self.text)
	
	def show(self, text, duration=3):
		w, h = director.get_window_size()
		self.text.element.text = '<font face="Cabin Regular" color="white">%s</font>' % text
		self.text.position = (w * 0.5, 40)
		self.text.do(ScaleTo(1.5, duration=0.25) + ScaleTo(1, duration=0.25) + Delay(duration) + ScaleTo(0, duration=0.25))

class PlayLayer(Layer):
	"""The play layer handles the update and graphical output of the play scene."""
	is_event_handler = True
	
	def __init__(self):
		"""Initialize a play layer."""
		super(PlayLayer, self).__init__()
		self.messages = MessageLayer()
		self.add(self.messages)

	def on_key_press(self, k, m):
		"""Respond to a key press and, if needed, do something."""
		if k == key.ESCAPE:
			director.app.to_config()
			return True
		pass
	
	def draw(self):
		"""Draw the whole play layer.
		
		The play layer is composed of four different sub-layers. First, the camera image is drawn. Second, every tracked object draws its background. Third, every tracked object draws its 3D part. Finally, every tracked object draws its foreground."""
		director.app.frame += 1
		w, h = director.get_window_size()
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		self.transform()
		# Draw the camera image
		glColor4f(1.0, 1.0, 1.0, 1.0)
		director.app.tracker.draw_current_frame_gl(w, h)
		# Draw the background of the tracked objects
		director.app.object_manager.draw_background()
		glPopMatrix()
		# Then draw the 3D objects
		glMatrixMode(GL_PROJECTION)
		director.app.tracker.projection_matrix.load_gl()
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		director.app.object_manager.draw_3d()
		glMatrixMode(GL_MODELVIEW)
		glPopMatrix()
		# Finally draw the foregrounds
		glPushMatrix()
		director.set_projection()
		glPopMatrix()
		glPushMatrix()
		self.transform()
		director.app.object_manager.draw_foreground()
		glPopMatrix()
		# Draw the original contents also
		super(PlayLayer, self).draw()
	
	def update(self, scene):
		"""Update the tracking subsystem and the tracked objects."""
		director.app.time = director.app.frame * 1.0 / pyglet.clock.get_fps()
		something_new = director.app.tracker.update(director.app.frame)
		if something_new:
			director.app.object_manager.update_tracking()
		director.app.object_manager.update()
