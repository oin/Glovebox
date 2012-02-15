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

"""The modular synthesis module.

Modular synthesis in Glovebox works as described in [1]. There are four kinds of behaviors :

sources -- Source behaviors generate sound and send it somewhere, by default to the audio output device.
fx -- Effect behaviors receive sound, transform it, then send it somewhere. Effects are kinds of sources.
ctrl -- Control behaviors do not generate nor transform sound but are permanently bound to a source (or effect) and modulate its parameters.
tool -- Tool behaviors are everything that doesn't fit within the former categories. They often offer temporary interaction with other tangible objects. Here, tool behaviors are just simple Behavior subclasses.

[1] J. Aceituno, J. Castet, M. Desainte-Catherine, and M. Hachet. Improvised interfaces for real-time musical applications. In Proceedings of the sixth international conference on tangible, embedded and embodied interaction (TEI), 2012."""

from . import Behavior
from cocos.director import director
from cocos.actions import *
from ..tools import ObjectNodes
import os
from ..shakemenus.ShakeMenu import *
import collections

class SourceBehavior(Behavior.Behavior):
	"""A source behavior generates sound via a Puredata patch."""
	def __init__(self, patch_path):
		"""Initialize a source behavior given a Puredata patch path relative to the `behaviors` directory."""
		super(SourceBehavior, self).__init__()
		self.redirect = None
		self.cached_attribute_values = collections.defaultdict(float)
		self.ring_action = None
		self.patch = director.app.audio.open_patch(os.path.join(director.app.audio_path, patch_path))
		self.association_name = "Redirect"
		self.init_attribute('volume', 'Volume', (0.0, 1.5), 'source_behavior_default_volume', 1)
	
	def number_to_patch(self, key, value):
		"""Send a float value to the Puredata patch, given a string key.
		
		For instance, with :
			b.number_to_patch("freq", 0.521)
		In its route part, the patch will catch the key and do something with the value."""
		director.app.audio.send_num_to_patch(self.patch, key, value)
	
	def symbol_to_patch(self, key, value):
		"""Send a string value to the Puredata patch, given a string key.
		
		For instance, with :
			b.symbol_to_patch("strategy", "greedy")
		In its route part, the patch will catch the key and do something with the value."""
		director.app.audio.send_sym_to_patch(self.patch, key, value)
	
	def turn_on(self):
		"""Turn the patch on."""
		director.app.audio.turn_on_patch(self.patch)
	
	def turn_off(self):
		"""Turn the patch off."""
		director.app.audio.turn_off_patch(self.patch)
	
	def associate(self, behavior):
		if not isinstance(behavior, FXBehavior):
			director.app.play_scene.messages.show("You can only redirect sound to effect behaviors.")
			return
		super(SourceBehavior, self).associate(behavior)
		self.redirect_audio_to_behavior(behavior)
		director.app.play_scene.messages.show("Redirecting audio.")
	
	def unassociate(self):
		super(SourceBehavior, self).unassociate()
		self.redirect_audio_to_master()
	
	def redirect_audio_to_master(self):
		"""Redirect the patch outgoing audio to the default output device."""
		if self.redirect:
			self.redirect.unregister_from("detached", self)
			self.redirect = None
		director.app.audio.redirect_patch_audio_to_master(self.patch)
		director.app.play_scene.messages.show("Stopped redirecting audio.")
	
	def redirect_audio_to_behavior(self, behavior):
		"""Redirect the patch outgoing audio to another behavior's input (if any)."""
		if self.redirect:
			self.redirect.unregister_from("detached", self)
		behavior.register_for("detached", self)
		self.redirect = behavior
		director.app.audio.redirect_patch_audio_to_patch(self.patch, behavior.patch)
	
	def has_just_attached(self, object):
		self.ring = ObjectNodes.RingNode(0.5, self.object.color)
		if not self.ring_action:
			self.ring_action = Repeat(ScaleTo(0.3, duration=0.5) + ScaleTo(0.5, duration=0.5))
		director.app.play_scene.do(self.ring_action, self.ring)
		self.turn_on()
	
	def has_just_detached(self):
		director.app.audio.close_patch(self.patch)
		self.patch = None
		self.ring_action.stop()
	
	def behavior_detached(self, sender, *args):
		super(SourceBehavior, self).behavior_detached(sender, *args)
		if self.redirect == sender:
			self.redirect = None
			self.redirect_audio_to_master()
	
	def draw_3d(self):
		super(SourceBehavior, self).draw_3d()
		self.ring.opacity = self.object.alpha() * 0.5
		self.ring.draw()
	
	def update(self):
		super(SourceBehavior, self).update()
		for attrkey in self.attributes:
			v = self.attributes[attrkey].value
			if v != self.cached_attribute_values[attrkey]:
				self.number_to_patch(attrkey, v)
				self.cached_attribute_values[attrkey] = v

class FXBehavior(SourceBehavior):
	"""An effect behavior manages an input channel and transforms its audio stream via a Puredata patch. Otherwise, it's like a source, you know."""
	def __init__(self, patch_path):
		"""Initialize an effect behavior given a Puredata patch path relative to the `behaviors` directory."""
		super(FXBehavior, self).__init__(patch_path)
		self.ring_action = Repeat(FadeOut(0.5) + FadeIn(0.5))

class CtrlBehavior(Behavior.Behavior):
	"""A control behavior manages one or more control parameters of its associated behavior."""
	def __init__(self):
		"""Initialize a control behavior."""
		super(CtrlBehavior, self).__init__()
		director.app.play_scene.messages.show("Please select an object to control, then shake the controller.")
		self.association_mode = True
		self.control_menu = None
		self.controlled_attribute = None
	
	def set_control_menu_mode(self):
		items = []
		for attrid in self.association.attributes:
			attr = self.association.attributes[attrid]
			items.append(ShakeMenuItem(attr.display_name, self.on_ctrl_menu_select_attribute, attr))
		if len(items) == 0:
			director.app.play_scene.messages.show("This behavior has no attribute to control.")
			self.unassociate()
			self.association_mode = True
			return
		self.control_menu = ShakeMenu(self.object, *items, no_shake=True)
	
	def on_ctrl_menu_select_attribute(self, attribute):
		self.control_menu = None
		self.controlled_attribute = attribute
	
	def unassociate(self):
		super(CtrlBehavior, self).unassociate()
		self.control_menu = None
		self.controlled_attribute = None
	
	def update(self):
		super(CtrlBehavior, self).update()
		if self.control_menu:
			self.control_menu.update()
	
	def draw_background(self):
		super(CtrlBehavior, self).draw_background()
		if self.control_menu:
			self.control_menu.draw_background()
	
	def draw_foreground(self):
		super(CtrlBehavior, self).draw_foreground()
		if self.control_menu:
			self.control_menu.draw_foreground()

	def draw_3d(self):
		super(CtrlBehavior, self).draw_3d()
		if self.control_menu:
			self.control_menu.draw_3d()