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

"""The default behavior module."""

from . import Behavior
from cocos.director import director
from cocos.actions import *
from ..tools import ObjectNodes
from ..shakemenus.ShakeMenu import *
from ..app import BehaviorLoader

FirstHint = True

class DefaultBehavior(Behavior.Behavior):
	"""A default behavior is what the application decides to attach to every new tracked object.
	
	The default behavior provides a shake menu that can be used to attach a more specific behavior to the tracked object."""
	def __init__(self):
		"""Initialize the default behavior."""
		super(DefaultBehavior, self).__init__()
		self.menu = None
	
	def has_just_attached(self, object):
		global FirstHint
		super(DefaultBehavior, self).has_just_attached(object)
		self.menu = self.generate_menu(director.app.behavior_loader)
		if FirstHint:
			director.app.play_scene.messages.show('<font size="-1"><b>Hint: </b>You can shake any object that has just been detected and attach a behavior to it.</font>', 6)
			FirstHint = False
	
	def generate_menu(self, loader):
		"""Generate the contents of the shake menu from the application's list of all known behaviors."""
		# Fill a nested structure from every menu description
		self.structure = AutoVivification()
		for modulename in loader.behaviors:
			module = loader.behaviors[modulename]
			path = module.menu
			walk = self.structure
			for item in path:
				walk = walk[item]
			walk[module.name] = module
		# Generate the first level of the menu
		items = []
		for item in self.structure:
			if isinstance(self.structure[item], BehaviorLoader.BehaviorModule):
				b = self.structure[item]
				sitem = ShakeMenuItem(b.display_name, self.instantiate_behavior, b, description=b.description)
				sitem.description = b.description
				items.append(sitem)
			else:
				items.append(ShakeMenuItem(item, self.show_submenu, self.structure[item]))
		return ShakeMenu(self.object, *items)
	
	def instantiate_behavior(self, module):
		"""Instantiate a given behavior module that will replace this behavior for the current tracked object."""
		self.menu.reset()
		self.object.attach_behavior(module.class_obj())
	
	def show_submenu(self, structure):
		"""Show a part of the previously generated menu contents with the shake menu."""
		# Generate this level of the menu
		items = []
		for item in structure:
			if isinstance(structure[item], BehaviorLoader.BehaviorModule):
				b = structure[item]
				sitem = ShakeMenuItem(b.display_name, self.instantiate_behavior, b, description=b.description)
				sitem.description = b.description
				items.append(sitem)
			else:
				items.append(ShakeMenuItem(item, self.show_submenu, structure[item]))
		self.menu.items = items
		self.menu.show_menu()

	def draw_3d(self):
		super(DefaultBehavior, self).draw_3d()
		if self.menu:
			self.menu.draw_3d()
	
	def draw_background(self):
		super(DefaultBehavior, self).draw_background()
		if self.menu:
			self.menu.draw_background()

	def draw_foreground(self):
		super(DefaultBehavior, self).draw_foreground()
		if self.menu:
			self.menu.draw_foreground()
	
	def update(self):
		super(DefaultBehavior, self).update()
		if self.menu:
			self.menu.update()


# http://stackoverflow.com/a/652284/1012567
class AutoVivification(dict):
	"""Implementation of perl's autovivification feature."""
	def __getitem__(self, item):
		try:
			return dict.__getitem__(self, item)
		except KeyError:
			value = self[item] = type(self)()
			return value