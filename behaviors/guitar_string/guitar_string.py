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

from glovebox.play.ModularSynthesis import *
from glovebox.play.Behavior import *

behavior_name = 'GuitarString'
behavior_description = "A guitar string."
behavior_menu = ['Sources']

class GuitarStringBehavior(SourceBehavior):
	def __init__(self):
		super(GuitarStringBehavior, self).__init__("guitar_string/guitar_string.pd")
		global behavior_name
		self.display_name = behavior_name
		self.init_attribute('freq', 'Frequency', (1, 1000), 'guitar_string_default_freq', 440, format_frequency)
		self.init_attribute('note', 'Note', (4, 90), 'guitar_string_default_note', 69)
		self.init_attribute('damping', 'Damping', (0.0, 1.0), 'guitar_string_default_damping', 0.1)