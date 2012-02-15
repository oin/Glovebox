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

from .ShakeRecognizer import ShakeRecognizer
from ..tools.ObjectSprite import ObjectSprite
from ..tools import ObjectNodes
from cocos.actions import *
from cocos.director import director
from pyglet.gl import *
from ..tools import Graphics2d
from .. import libglovebox
import cocos
import math

class ShakeMenu(object):
	"""A shake menu.
	
	This is a variant of the display-referenced shake menu described in [1].
	
	[1] S. White, D. Feng, and S. Feiner. Interaction and presentation techniques for shake menus in tangible augmented reality. In Proc. IEEE ISMAR, pages 39–48, 2009."""
	
	def __init__(self, object, *items, **kwargs):
		super(ShakeMenu, self).__init__()
		self.object = object
		self.items = []
		self.default_items = []
		self.cancel_callback = kwargs.get("on_cancel", None)
		self.end_callback = kwargs.get("on_end", None)
		for item in items:
			self.items.append(item)
			self.default_items.append(item)
		self.state = None
		self.activation_position = None
		self.no_shake = kwargs.get("no_shake", False)
		self.wait_shake()
	
	def reset(self):
		self.items = []
		for item in self.default_items:
			self.items.append(item)
	
	def change_state(self, state):
		self.state = state(self)
	
	def wait_shake(self):
		if self.no_shake:
			self.show_menu()
		else:
			self.change_state(StateInitial)
	
	def show_menu(self):
		for item in self.items:
			item.menu = self
		screen_coords = self.object.screen_coords()
		self.activation_position = (screen_coords.x, screen_coords.y)
		self.change_state(StateMenuShown)
	
	def update(self):
		self.state.update()
	
	def draw_3d(self):
		self.state.draw_3d()
	
	def draw_background(self):
		self.state.draw_background()
	
	def draw_foreground(self):
		self.state.draw_foreground()
	
	def item_size(self):
		return director.app.options.setdefault('shake_menu_item_size', 32)

class ShakeMenuItem(object):
	"""A shake menu item, with a name and an action"""
	def __init__(self, title, action = None, *args, **kwargs):
		super(ShakeMenuItem, self).__init__()
		self.title = title
		self.menu = None
		self.action = action
		self.args = args
		self.description = kwargs.get('description', None)
	
	def on_hover(self):
		if self.description and director.app.options.setdefault('shake_menu_show_descriptions', True):
			director.app.play_scene.messages.show(self.description)
	
	def on_activate(self):	
		self.menu.wait_shake()
		if self.action:
			self.action(*self.args)
		else:
			self.menu.reset()
		if self.menu.end_callback:
			self.menu.end_callback()

class ShakeMenuState(object):
	def __init__(self, menu):
		super(ShakeMenuState, self).__init__()
		self.menu = menu
		self.object = self.menu.object
	def update(self):
		pass
	def draw_background(self):
		pass
	def draw_foreground(self):
		pass
	def draw_3d(self):
		pass

class StateInitial(ShakeMenuState):
	def __init__(self, menu):
		super(StateInitial, self).__init__(menu)
		self.shake = ShakeRecognizer()
		self.circle = ObjectNodes.CircleNode(self.object.color)
		self.circle.scale = 0
		self.shake_count = 0
	
	def update(self):
		if self.shake.update(self.object.raw_translation):
			self.menu.show_menu()
		
		if self.shake_count != self.shake.shake_count:
			ratio = 1.0 * self.shake.shake_count / self.shake.shake_limit
			director.app.play_scene.do(ScaleTo(ratio, duration=0.2), self.circle)
			self.shake_count = self.shake.shake_count
		
			
	def draw_3d(self):
		self.circle.opacity = self.object.alpha() * 0.5
		self.circle.draw()


class StateMenuShown(ShakeMenuState):
	def __init__(self, menu):
		super(StateMenuShown, self).__init__(menu)
		self.shake = ShakeRecognizer()
		self.pointer = cocos.sprite.Sprite("pointer.png")
		self.pointer.opacity = 0
		director.app.play_scene.do(FadeIn(0.5), self.pointer)
		self.items = []
		for m_item in self.menu.items:
			item = ShakeMenuItemNode(m_item, self.menu.item_size(), self.object.color)
			item.scale = 0
			director.app.play_scene.do(RandomDelay(0.0, 0.1) + ScaleTo(1, duration = 0.25), item)
			self.items.append(item)
		self.selected = None
		self.homing = director.app.time
		self.activated = False

	def homing_time(self):
		return director.app.options.setdefault('shake_menu_homing_time', 1.0)
	
	def update(self):
		# Cancel test
		if self.shake.update(self.object.raw_translation) and not self.selected and not self.menu.no_shake:
			self.menu.reset()
			self.menu.wait_shake()
			if self.menu.cancel_callback:
				self.menu.cancel_callback()
			if self.menu.end_callback:
				self.menu.end_callback()
		
		screen_coords = self.object.screen_coords()
		self.pointer.position = (screen_coords.x, screen_coords.y)
		# Hit test
		selected = None
		i = 0
		for item in self.items:
			coords = self.position_center_of(i)
			item_coords = libglovebox.Vec2f(coords[0] + self.menu.activation_position[0], coords[1] + self.menu.activation_position[1])
			if screen_coords.distance(item_coords) < self.menu.item_size():
				selected = item
				break
			i += 1
		if selected != self.selected:
			if selected:
				selected.item.on_hover()
				director.app.play_scene.do(AccelDeccel(ScaleTo(2.5, duration=self.homing_time())), selected)
				self.homing = director.app.time
			if self.selected:
				director.app.play_scene.do(ScaleTo(1, duration=self.homing_time()), self.selected)
			self.selected = selected
		# Check if a selection has been made
		if not self.activated and self.selected and director.app.time - self.homing > self.homing_time():
			sel = self.selected.item
			for item in self.items:
				director.app.play_scene.do(RandomDelay(0.0, 0.2) + ScaleTo(0, duration=0.25), item)
			def activate_and_exit():
				sel.on_activate()
				self.menu.reset()
			director.app.play_scene.do(Delay(0.4) + CallFunc(activate_and_exit))
			self.activated = True

	def draw_background(self):
		self.pointer.opacity = 255 * self.object.alpha()
		self.pointer.draw()
	
	def draw_foreground(self):
		i = 0
		glPushMatrix()
		coords = self.menu.activation_position + (0.0,)
		glTranslatef(*coords)
		for item in self.items:
			item.opacity = 255 * self.object.alpha() * 0.8
			glPushMatrix()
			coords = self.position_center_of(i) + (0.0,)
			glTranslatef(*coords)
			item.draw()
			glPopMatrix()
			i += 1
		glPopMatrix()
	
	def ideal_distance(self):
		if len(self.items) < 2:
			return 0
		angle = 2.0 * math.pi / len(self.items)
		sinA = math.sin(angle * 0.5)
		if sinA != 0:
			return max(self.menu.item_size() * 1.0 / sinA, self.menu.item_size() * 2)
		return 0

	def position_center_of(self, i):
		if len(self.items) < 2:
			return (0,0)
		angle = 2.0 * math.pi / len(self.items)
		d = self.ideal_distance()
		return (d * math.cos(angle * i), d * math.sin(angle * i))

class ShakeMenuItemNode(cocos.cocosnode.CocosNode):
	def __init__(self, item, radius, color = (1, 1, 1)):
		super(ShakeMenuItemNode, self).__init__()
		self.color = color
		self.item = item
		self.opacity = 255
		self.text = cocos.text.Label(item.title, font_name="Cabin Bold", font_size=10, color=(0, 0, 0, self.opacity), anchor_x = "center", anchor_y = "center")
		self.text.position = (0, 0)
		self.radius = radius

	def draw(self, *args, **kwargs):
		super(ShakeMenuItemNode, self).draw(args, kwargs)
		glPushMatrix()
		self.transform()
		color = self.color + (self.opacity * 1.0 / 255,)
		self.text.color = (0, 0, 0, self.opacity)
		Graphics2d.draw_circle(0, 0, self.radius, color)
		self.text.draw()
		glPopMatrix()