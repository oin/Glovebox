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

"""The help screen module."""

import cocos
from cocos.layer import *
from cocos.director import director
from cocos.actions import *
from cocos.text import *
from cocos.menu import *
from .GloveboxMenu import *

class Help(MultiplexLayer):
	"""A main help layer can show either the help menu or a help screen."""
	def __init__(self):
		"""Initialize a main help layer."""
		super(Help, self).__init__(HelpMenu(), WhatIsIt(), KeyboardShortcuts())

class HelpMenu(GloveboxMenu):
	"""A help menu allows to switch between various help screens."""
	def __init__(self):
		"""Initialize a help menu."""
		super(HelpMenu, self).__init__('Help')
		items = []
		items.append(MenuItem('What is it ?', self.on_what_is_it))
		items.append(MenuItem('Keyboard shortcuts', self.on_shortcuts))
		items.append(MenuItem('Return', self.on_quit))
		self.create_menu(items, self.transition)
	
	def on_what_is_it(self):
		"""Switch to a particular help screen."""
		self.parent.switch_to(1)
	
	def on_shortcuts(self):
		"""Switch to a particular help screen."""
		self.parent.switch_to(2)
	
	def on_quit(self):
		"""Switch to a particular help screen."""
		self.parent.parent.switch_to(0)

class HelpLayer(Layer):
	"""A help layer handles the presentational and behavioral aspects a help screen.
	
	A help screen is made of several horizontal-centered text lines. Hitting any key allows to switch back to the help menu."""
	is_event_handler = True
	
	def __init__(self):
		"""Initialize a help layer."""
		super(HelpLayer, self).__init__()
		self.win_width, self.win_height = director.get_window_size()
		self.height_total = 0.0
		self.items = []
		
	def on_key_press(self, k, m):
		"""Respond to a key press by going back to the help menu."""
		self.parent.switch_to(0)
		return True
	
	def add_line(self, line, height=0.05):
		"""Append a text line to the help menu."""
		self.height_total += height
		lbl = HTMLLabel(line, anchor_x="center", anchor_y="center")
		lbl.position = self.win_width * 0.5, self.win_height * (1.0 - self.height_total)
		self.add(lbl)

class WhatIsIt(HelpLayer):
	"""A help layer explaining what Glovebox is."""
	def __init__(self):
		"""Initialize the help layer."""
		super(WhatIsIt, self).__init__()
		w, h = director.get_window_size()
		self.add_line('<font face="Cabin Regular" color="white"><b>Glovebox</b> is an experimental improvised interface for real-time musical applications.</font>', 0.1)
		self.add_line('<font face="Cabin Regular" color="#CCCCCC">It allows you to blabla</font>')


class KeyboardShortcuts(HelpLayer):
	"""A help layer listing the important keyboard shortcuts."""
	def __init__(self):
		"""Initialize the help layer."""
		super(KeyboardShortcuts, self).__init__()
		self.add_line('<font face="Cabin Bold" size="+2" color="white">Keyboard shortcuts</font>')
		self.add_line('<font face="Cabin Italic" size="-1" color="#AAAAAA">On Macintosh, replace CTRL with CMD.</font>', 0.1)
		self.add_line('<font face="Cabin Regular" color="white"><b>CTRL+Q</b> Quit Glovebox</font>')
		self.add_line('<font face="Cabin Regular" color="white"><b>CTRL+F</b> Toggle fullscreen</font>')
		self.add_line('<font face="Cabin Regular" color="white"><b>CTRL+I</b> Show the Python interpreter</font>')
		self.add_line('<font face="Cabin Regular" color="white"><b>CTRL+P</b> Pause Glovebox</font>')
		self.add_line('<font face="Cabin Regular" color="white"><b>CTRL+X</b> Show the framerate counter</font>')