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
from glovebox.shakemenus.ShakeMenu import *
from cocos.director import director
from glovebox.play import DefaultBehavior
import os

behavior_name = 'Looper'
behavior_description = "A loop player."
behavior_menu = ['Sources']

class LooperBehavior(SourceBehavior):
	def __init__(self):
		super(LooperBehavior, self).__init__("looper/looper.pd")
		global behavior_name
		self.display_name = behavior_name
		self.samples = []
		for file in os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), 'loops'))):
			if file.endswith(".wav"):
				self.samples.append(os.path.basename(file))
		self.time_last_impulse = 0
		self.needs_to_reappear = False
	
	def has_just_attached(self, object):
		super(LooperBehavior, self).has_just_attached(object)
		self.generate_audio_menu()

	def generate_audio_menu(self):
		items = []
		# print samples
		for sample in self.samples:
			samplename = os.path.splitext(sample)[0]
			items.append(ShakeMenuItem(samplename, self.audio_menu_select_sample, "loops/"+sample))
		if len(items) == 0:
			# Can't create any sample, so go back to the default behavior
			director.app.play_scene.messages.show("No loop in directory.")
			self.object.attach_behavior(DefaultBehavior.DefaultBehavior())
		self.menu = ShakeMenu(self.object, *items, no_shake=True)

	def audio_menu_select_sample(self, spl):
		self.menu = None
		self.symbol_to_patch("load", spl)
		self.bang()

	def update(self):
		super(LooperBehavior, self).update()
		if self.menu:
			self.menu.update()

	def draw_3d(self):
		super(LooperBehavior, self).draw_3d()
		if self.menu:
			self.menu.draw_3d()

	def draw_background(self):
		super(LooperBehavior, self).draw_background()
		if self.menu:
			self.menu.draw_background()

	def draw_foreground(self):
		super(LooperBehavior, self).draw_foreground()
		if self.menu:
			self.menu.draw_foreground()