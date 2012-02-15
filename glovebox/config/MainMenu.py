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

"""The main menu module."""

from .GloveboxMenu import GloveboxMenu
from cocos.menu import *
import pyglet
from cocos.director import director
from ..play.Behavior import Behavior

class MainMenu(GloveboxMenu):
	"""A main menu is the main interface to navigate to the different parts of Glovebox."""
	def __init__(self):
		"""Initialize a main menu."""
		super(MainMenu, self).__init__('Glovebox')
		items = []
		
		items.append(MenuItem('Use Glovebox', self.on_play))
		items.append(MenuItem('Configuration', self.on_configuration))
		items.append(MenuItem('Edit Behaviors', self.on_open_behaviors_folder))
		items.append(MenuItem('Reset', self.on_reset))
		items.append(MenuItem('Help', self.on_help))
		items.append(MenuItem('Quit', self.on_quit))
		
		self.create_menu(items, self.transition)
	
	def on_play(self):
		"""Go to the play scene."""
		director.app.to_play()
	
	def on_quit(self):
		"""Quit the application."""
		pyglet.app.exit()
	
	def on_configuration(self):
		"""Switch to the configuration menu."""
		self.parent.switch_to(1)
	
	def on_help(self):
		"""Switch to the help menu."""
		self.parent.switch_to(2)
	
	def on_open_behaviors_folder(self):
		"""Open the behaviors folder."""
		director.app.behavior_loader.open_behavior_directory()
	
	def on_reset(self):
		for id in director.app.objects:
			obj = director.app.objects[id]
			obj.attach_behavior(Behavior())
		director.app.objects.clear()