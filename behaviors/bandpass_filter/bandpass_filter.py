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

behavior_name = 'Filter'
behavior_description = "A bandpass filter."
behavior_menu = ['FX']

class BandpassFilterBehavior(FXBehavior):
	def __init__(self):
		super(BandpassFilterBehavior, self).__init__("bandpass_filter/bandpass_filter.pd")
		global behavior_name
		self.display_name = behavior_name
		self.init_attribute('freq', 'Frequency', (10, 7500), 'bandpass_filter_default_freq', 1000, format_frequency)
		self.init_attribute('q', 'Q', (0.0, 10.0), 'bandpass_filter_default_q', 3.0)
