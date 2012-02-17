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
from cocos.director import director
from cocos.text import Label

behavior_name = 'GuitarPick'
behavior_description = "Sends an impulse to objects near it."
behavior_menu = []

class GuitarPickBehavior(Behavior):
	def __init__(self):
		super(GuitarPickBehavior, self).__init__()
		global behavior_name
		self.display_name = behavior_name
		self.init_attribute('pick_distance', 'PickDistance', (0,1000), 'pick_distance', 3.9)
		self.currently_picked = []
		
	def associate(self, behavior):
		return False
	
	def update(self):
		super(GuitarPickBehavior, self).update()
		for id in director.app.objects:
			current = director.app.objects[id]
			if not isinstance(current.behavior, SourceBehavior):
				continue
			if current == self.object:
				continue
			if current.is_zombie():
				continue
			distance = self.object.translation.distance(current.translation)
			if distance < self.attributes['pick_distance'].value:
				if not current in self.currently_picked:
					self.currently_picked.append(current)
					current.behavior.impulse(1)
			else:
				if current in self.currently_picked:
					self.currently_picked.remove(current)