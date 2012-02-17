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
from glovebox.play.Behavior import BehaviorAttribute
from cocos.director import director
from cocos.text import Label

behavior_name = 'Generic'
behavior_description = "A generic controller."
behavior_menu = ['Controllers']

class GenericControllerBehavior(CtrlBehavior):
	def __init__(self):
		super(GenericControllerBehavior, self).__init__()
		global behavior_name
		self.display_name = behavior_name
		self.label = Label("", font_size=9, font_name="Cabin Regular", anchor_x="center", anchor_y="top", color=(255, 255, 255, 255))
		self.init_attribute('control_distance', 'ControlDistance', (0,1000), 'generic_controller_default_control_distance', 10)
		
	def associate(self, behavior):
		super(GenericControllerBehavior, self).associate(behavior)
		self.set_control_menu_mode()
	
	def update(self):
		super(GenericControllerBehavior, self).update()
		if self.controlled_attribute:
			distance = self.object.translation.distance(self.association.object.translation)
			distance_ratio = max(0, min(1.3, distance * 1.0 / self.attributes['control_distance'].value) - 0.3)
			value = self.controlled_attribute.range[0] + (distance_ratio * (self.controlled_attribute.range[1] - self.controlled_attribute.range[0]))
			self.controlled_attribute.set(value)
	
	def draw_foreground(self):
		super(GenericControllerBehavior, self).draw_foreground()
		if self.controlled_attribute:
			coords = self.object.screen_coords()
			self.label.position = coords.x, coords.y - 10
			self.label.element.text = "%s: %s" % (self.controlled_attribute.display_name, self.controlled_attribute.to_string())
			self.label.element.color = (255, 255, 255, int(self.object.alpha() * 255))
			self.label.draw()
