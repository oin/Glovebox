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

"""The configuration menu module."""

import cocos
from .. import libglovebox
from cocos.menu import *
from cocos.director import director
from cocos.actions import *
from .GloveboxMenu import *
from ..filter import Filter

class ConfigMenu(GloveboxMenu):
	"""A configuration menu is the most direct way to tweak some parameters of the application.
	
	From the configuration menu, the user can access to various configuration options."""
	def __init__(self):
		"""Initialize a configuration menu."""
		super(ConfigMenu, self).__init__('Configuration')
		items = []
		items.append(MenuItem('Camera configuration', self.on_configure_camera))
		items.append(MenuItem('Filtering configuration', self.on_filters))
		items.append(MenuItem('Return', self.on_quit))
		self.create_menu(items, self.transition)
	
	def on_quit(self):
		"""Switch to the main menu."""
		self.parent.switch_to(0)
	
	def on_configure_camera(self):
		"""Show a modal webcam configuration window."""
		director.app.tracker.show_configuration_window()
	
	def on_filters(self):
		"""Switch to the filtering configuration menu."""
		self.parent.switch_to(3)

class FilterConfigMenu(GloveboxMenu):
	"""A filtering configuration menu provides access to filter and filter thread parameters."""
	def __init__(self):
		"""Initialize a filter configuration menu."""
		super(FilterConfigMenu, self).__init__('Filter configuration')
		items = []
		self.filters = ['NONE', 'INTERPOLATOR', 'VIRTUAL COUPLING']
		items.append(ToggleMenuItem('Filter thread: ', self.on_filter_thread))
		items.append(MultipleMenuItem('Filter: ', self.on_filter, self.filters, 2))
		items.append(MenuItem('Return', self.on_quit))
		self.create_menu(items, self.transition)

	def on_quit(self):
		"""Switch to the main configuration menu."""
		self.parent.switch_to(1)

	def on_filter(self, f):
		"""Change the filtering method for the whole application."""
		if f == 0:
			director.app.change_filter(Filter.Filter())
		elif f == 1:
			director.app.change_filter(Filter.SimpleInterpolator())
		elif f == 2:
			director.app.change_filter(Filter.VirtualCoupling())

	def on_filter_thread(self, value):
		"""Toggle the use of a separate thread for filtering."""
		director.app.toggle_filter_thread()
