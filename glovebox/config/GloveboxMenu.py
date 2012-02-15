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

"""The Glovebox menu module."""

import cocos
from .. import libglovebox
from cocos.menu import *
from cocos.director import director
from cocos.actions import *

class GloveboxMenu(Menu):
	"""A Glovebox menu is a menu with some default appearance settings."""
	def __init__(self, title):
		"""Initialize a menu with a nice appearance."""
		super(GloveboxMenu, self).__init__(title)
		self.transition = Jump(10, 0, 1, 0.2)
		self.font_title['font_name'] = 'Cabin Bold'
		self.font_title['color'] = (255, 255, 255, 164)
		self.font_item['font_name'] = 'Cabin Medium'
		self.font_item_selected['font_name'] = 'Cabin Medium'
		self.font_item['font_size'] = 26
		self.font_item_selected['font_size'] = 26
		self.font_item['color'] = (255, 255, 255, 192)
		self.font_item_selected['color'] = (255, 255, 255, 255)