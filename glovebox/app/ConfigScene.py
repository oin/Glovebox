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

"""The configuration scene module."""

import cocos
from .. import libglovebox
from ..config.ConfigMenu import *
from ..config.MainMenu import *
from ..config.Help import *
from cocos.layer import *

class ConfigScene(cocos.scene.Scene):
	"""The configuration scene consists of several layers (in cocos parlance) where each is a screen of the application menu."""
	def __init__(self):
		"""Initialize a configuration scene."""
		super(ConfigScene, self).__init__()
		self.add(MultiplexLayer(
			MainMenu(), ConfigMenu(), Help(), FilterConfigMenu()
		))