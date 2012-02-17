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
from glovebox.tools.ObjectSprite import ObjectSprite
from cocos.director import director
from glovebox.play import DefaultBehavior

behavior_name = 'AudioIn'
behavior_description = "Represents an input channel of your audio device."
behavior_menu = ['Sources']

class AudioInBehavior(SourceBehavior):
	def __init__(self):
		super(AudioInBehavior, self).__init__("audio_in/audio_in.pd")
		global behavior_name
		self.display_name = behavior_name
		self.sprite = ObjectSprite("maracas.png")
		self.menu = None
		self.init_attribute('volume', 'Volume', (0.0, 10.0), 'audio_in_behavior_default_volume', 0.5)
	
	def has_just_attached(self, object):
		super(AudioInBehavior, self).has_just_attached(object)
		self.generate_audio_menu()
	
	def generate_audio_menu(self):
		items = []
		for i in range(0, director.app.audio.input_device.nb_input_channels):
			items.append(ShakeMenuItem("Input %d" % (i+1), self.audio_menu_select_input, i+1))
		if len(items) == 0:
			# Can't create any input, so go back to the default behavior
			director.app.play_scene.messages.show("No input device in your system.")
			self.object.attach_behavior(DefaultBehavior.DefaultBehavior())
		self.menu = ShakeMenu(self.object, *items, no_shake=True)
	
	def audio_menu_select_input(self, i):
		self.menu = None
		self.symbol_to_patch("input", "in%d" % i)
	
	def update(self):
		super(AudioInBehavior, self).update()
		if self.menu:
			self.menu.update()
	
	def draw_3d(self):
		super(AudioInBehavior, self).draw_3d()
		if self.menu:
			self.menu.draw_3d()
		else:
			self.sprite.opacity = self.object.alpha() * 255
			self.sprite.draw()
	
	def draw_background(self):
		super(AudioInBehavior, self).draw_background()
		if self.menu:
			self.menu.draw_background()
	
	def draw_foreground(self):
		super(AudioInBehavior, self).draw_foreground()
		if self.menu:
			self.menu.draw_foreground()