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

from glovebox.play.Behavior import *
from glovebox.play.DefaultBehavior import DefaultBehavior
from glovebox.shakemenus.ShakeMenu import *
from glovebox.shakemenus.ShakeRecognizer import *
from cocos.director import director

behavior_name = 'AlphaObject'
behavior_description = "Handy tool to control behaviors and properties."
behavior_menu = []

class AlphaObjectBehavior(Behavior):
	def __init__(self):
		super(AlphaObjectBehavior, self).__init__()
		global behavior_name
		self.display_name = behavior_name
		self.menu = None
		self.target = None
		self.target_mode = True
		self.lock = False
		self.lock_cancel_callback = None
		self.shaker = ShakeRecognizer()
		self.target_association_selection_shaker = ShakeRecognizer()
		self.target_association_mode = False
		self.target_association_selection = None
	
	def has_just_attached(self, object):
		super(AlphaObjectBehavior, self).has_just_attached(object)
	
	def update(self):
		super(AlphaObjectBehavior, self).update()
		if self.target_mode:
			# Must select a target
			new_target = None
			min_distance = sys.float_info.max
			for id in director.app.objects:
				current = director.app.objects[id]
				dist = current.translation.distance(self.object.translation)
				if current != self.object and not current.is_zombie() and dist < min_distance:
					min_distance = dist
					new_target = current
			if self.target != new_target:
				# The target has changed.
				self.target = new_target
				self.shaker.reset()
			else:
				if self.target and self.shaker.update(self.object.raw_translation):
					self.show_menu()
		else:
			if not self.lock and self.menu:
				self.menu.update()
			if self.target_association_mode:
				new_selection = None
				min_distance = sys.float_info.max
				for id in director.app.objects:
					current = director.app.objects[id]
					dist = current.translation.distance(self.object.translation)
					if current != self.object and current != self.target and not current.is_zombie() and dist < min_distance:
						min_distance = dist
						new_selection = current
				if self.target_association_selection != new_selection:
					# The selection has changed.
					self.target_association_selection = new_selection
					self.target_association_selection_shaker.reset()
				else:
					if self.target_association_selection and self.target_association_selection_shaker.update(self.object.raw_translation):
						# Associate the selection
						self.target_association_mode = False
						
						self.target.behavior.associate(self.target_association_selection.behavior)
						self.target_association_selection = None
						self.lock = False
						self.menu_cancelled()
						director.app.play_scene.messages.show("Behaviors associated.")
	
	def show_menu(self):
		self.target_mode = False
		items = []
		if not isinstance(self.target.behavior, DefaultBehavior):
			items.append(ShakeMenuItem("Detach", self.on_detach_target, description="Detaches the selected behavior from its object."))
			if self.target.behavior.association:
				items.append(ShakeMenuItem("Un%s" % self.target.behavior.association_name, self.on_unassociate_target, description=''))
			else:
				items.append(ShakeMenuItem(self.target.behavior.association_name, self.on_associate_target, self.target, description=''))
		else:
			items.append(ShakeMenuItem("Attach", self.on_attach_target, description="Attaches a behavior to the selected object."))	
		items.append(ShakeMenuItem("Inspect", self.on_inspect_target, description="Inspects the attributes of the selected behavior."))
		self.menu = ShakeMenu(self.object, *items, no_shake=True, on_cancel=self.menu_cancelled)
		# Still allow the user to cancel
		self.menu.no_shake = False
	
	def menu_cancelled(self):
		self.target_mode = True
		self.target = None
		self.menu = None
	
	def on_detach_target(self):
		self.target.attach_behavior(DefaultBehavior())
		self.menu_cancelled()
		director.app.play_scene.messages.show("Behavior detached.")
	
	def on_attach_target(self):
		self.target.behavior.menu.object = self.object
		self.lock_end_callback = self.target.behavior.menu.end_callback
		self.target.behavior.menu.end_callback = self.target_menu_end_callback
		self.target.behavior.menu.show_menu()
		self.lock = True
		director.app.play_scene.messages.show("Please select a behavior type to attach the object to.")
	
	def target_menu_end_callback(self):
		self.target.behavior.menu.object = self.target
		self.target.behavior.menu.end_callback = self.lock_end_callback
		self.lock_end_callback = None
		self.lock = False
		self.menu_cancelled()
		director.app.play_scene.messages.show("Behavior attached.")
	
	def on_inspect_target(self):
		items = []
		for attrid in self.target.behavior.attributes:
			attr = self.target.behavior.attributes[attrid]
			items.append(ShakeMenuItem("%s: %s" % (attr.display_name, attr.to_string())))
		if len(items) == 0:
			director.app.play_scene.messages.show("This behavior has no attribute to inspect.")
			self.menu_cancelled()
			return
		self.menu.items = items
		self.menu.show_menu()
	
	def on_associate_target(self, target):
		self.target = target
		self.target_mode = False
		self.target_association_mode = True
		self.target_association_selection = None
		self.lock = True
		self.target_association_selection_shaker.reset()
		director.app.play_scene.messages.show("Please place the alpha object near the desired behavior and shake it.")
	
	def on_unassociate_target(self):
		self.target.behavior.unassociate()
		self.menu_cancelled()
		director.app.play_scene.messages.show("Behavior unassociated.")
	
	def draw_background(self):
		super(AlphaObjectBehavior, self).draw_background()
		if not self.lock and self.menu:
			self.menu.draw_background();

	def draw_foreground(self):
		super(AlphaObjectBehavior, self).draw_foreground()
		if not self.lock and self.menu:
			self.menu.draw_foreground();
			
	def draw_3d(self):
		super(AlphaObjectBehavior, self).draw_3d()
		if self.target and not self.target_association_mode:
			self.target.model_view_matrix.load_gl()
			Graphics2d.draw_rect(-1.5, -1.5, 3, 3, (0.0, 0.0, 0.0, self.object.alpha()), filled=False, line_width=2)
			Graphics2d.draw_rect(-1.5, -1.5, 3, 3, self.object.color +  (self.object.alpha() * 0.4,), filled=True)
			self.object.model_view_matrix.load_gl()
		if self.target_association_selection:
			self.target_association_selection.model_view_matrix.load_gl()
			Graphics2d.draw_rect(-1.5, -1.5, 3, 3, (0.0, 0.0, 0.0, self.object.alpha()), filled=False, line_width=2)
			Graphics2d.draw_rect(-1.5, -1.5, 3, 3, self.object.color +  (self.object.alpha() * 0.4,), filled=True)
			self.object.model_view_matrix.load_gl()
		if self.lock:
			return
		if self.menu:
			self.menu.draw_3d()