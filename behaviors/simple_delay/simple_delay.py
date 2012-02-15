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

behavior_name = 'SimpleDelay'
behavior_description = "A simple delay."
behavior_menu = ['FX']

class SimpleDelayBehavior(FXBehavior):
	def __init__(self):
		super(SimpleDelayBehavior, self).__init__("simple_delay/simple_delay.pd")
		global behavior_name
		self.display_name = behavior_name
		self.display_name = "SimpleDelay"
		self.init_attribute('delay', 'DelayTime', (1.0, 1000), 'simple_delay_default_delay_time', 150, format_time_ms)
		self.init_attribute('feedback', 'Feedback', (0.0, 1.0), 'simple_delay_default_feedback', 0.4)
		self.init_attribute('wet', 'Dry/Wet', (0.0, 1.0), 'simple_delay_default_dry_wet', 0.5)
