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
from glovebox.shakemenus.ShakeRecognizer import ShakeRecognizer
from glovebox import libglovebox
from glovebox.filter import Filter
from glovebox.tools.ObjectSprite import ObjectSprite
from glovebox.play.Behavior import *

behavior_name = 'Maracas'
behavior_description = "A maracas."
behavior_menu = ['Sources']

class MaracasBehavior(SourceBehavior):
	def __init__(self):
		super(MaracasBehavior, self).__init__("maracas/maracas.pd")
		global behavior_name
		self.display_name = behavior_name
		self.last_position = libglovebox.Vec3f(0,0,0)
		self.last_speed = 0
		self.hysteresis = False
		self.last_ok_speed = 0
		self.speed_limit = 0.53
		self.speed_limit2 = 2.25
		self.speed_max = 2.3
		self.filter = Filter.SimpleInterpolator(0.8, 0)
		self.sprite = ObjectSprite("maracas.png")
		
		self.init_attribute('attack', 'AttackTime', (0,200), 'maracas_behavior_attack_time', 50, format_time_ms)
		self.init_attribute('sustain', 'SustainTime', (0,2000), 'maracas_behavior_sustain_time', 50, format_time_ms)
		self.init_attribute('release', 'ReleaseTime', (0,2000), 'maracas_behavior_release_time', 50, format_time_ms)
	
	def has_just_attached(self, object):
		super(MaracasBehavior, self).has_just_attached(object)
		self.last_position = object.raw_translation
	
	def update(self):
		super(MaracasBehavior, self).update()
		self.filter.filter(self.object.raw_translation, libglovebox.Quaternion(0, 0, 0, 0))
		
		speed = self.filter.translation.distance(self.last_position)
		self.last_position = libglovebox.Vec3f(self.filter.translation.x, self.filter.translation.y, self.filter.translation.z)
		self.last_speed = speed
		
		force = min(self.speed_max, speed - self.speed_limit) / self.speed_max
		
		if speed < self.speed_limit2 and self.hysteresis:
			self.hysteresis = False
		
		if force > 0 and not self.hysteresis:
			self.number_to_patch('impulse', force)
			self.hysteresis = True
	
	def draw_3d(self):
		super(MaracasBehavior, self).draw_3d()
		self.sprite.opacity = self.object.alpha() * 255
		self.sprite.draw()