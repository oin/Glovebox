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

"""The main application module."""

import sys
import os
import inspect

import cocos
from ..libglovebox import *
from ..errors.errorlayers import *
from .ConfigScene import *
from .PlayScene import *
import pyglet
from pyglet import font
from cocos.director import director
from cocos.scenes.transitions import *
from ..filter import Filter
from ..play.TrackedObjectManager import *
from ..filter import FilterThread
from . import BehaviorLoader
from .. import *

class Application(pyglet.event.EventDispatcher):
	"""The whole application is managed here.
	
	The Glovebox application flow consists on two game-like screens called scenes, in cocos parlance. The play scene is the most interesting one, as it is where the whole improvised interaction occurs. The config scene is a keyboard-and-mouse based menu making it easy to configure application parameters. Both scenes have a dedicated package : play and config."""
	def __init__(self, **kwargs):
		"""Initialize the application.
		
		Keyword arguments:
		width -- the width of the application window
		height -- the height of the application window
		
		"""
		super(Application, self).__init__()
		
		w = kwargs.pop('width', 640)
		h = kwargs.pop('height', 480)
		# pyglet
		pyglet.resource.path.append('data')
		pyglet.resource.reindex()
		font.add_directory('data')
		# libglovebox subsystems
		self.tracker = WebcamTracker()
		self.audio = AudioEngine()
		self.audio_config = AudioSettings()
		self.audio_config.sample_rate = kwargs.pop('audio_sample_rate', 44100)
		self.audio_config.buffer_size = kwargs.pop('audio_buffer_size', 256)
		sysaudio = SystemAudio()
		self.audio_config.input_device = sysaudio.default_input_device()
		self.audio_config.output_device = sysaudio.default_output_device()
		self.camera_config = CameraSettings()
		cam_w, cam_h = kwargs.pop('camera_image_size', (640,480))
		self.camera_config.image_width = cam_w
		self.camera_config.image_width = cam_h
		self.camera_config.calibration_file = 'camera.cal'
		self.camera_config.desired_framerate = kwargs.pop('camera_fps', 60)
		# cocos2d and scenes
		director.init(caption='Glovebox', width=w, height=h, audio=None, resizable=True, )
		self.config_scene = ConfigScene()
		self.play_scene = PlayScene()
		self.in_play = False
		self.frame = 0
		self.time = 0
		# Fill the interpreter locals
		director.interpreter_locals['application'] = self
		director.interpreter_locals['Filter'] = Filter
		# Set the path for audio things
		self.audio_path = os.path.join(BehaviorLoader.glovebox_path(), "behaviors")
		self.audio.add_to_patch_search_path(os.path.join(BehaviorLoader.glovebox_path(), "behaviors"))
		# Make sure anyone can access us
		director.app = self
		self.options = {}
		# Tracked objects
		self.objects = {}
		self.filter = Filter.SimpleInterpolator()
		self.object_manager = TrackedObjectManager()
		self.filter_thread = None
		self.behavior_loader = None
	
	def run(self):
		"""Start the audio and tracking subsystems, then run the application and return once everything is shut down."""
		if not self.audio.open(self.audio_config):
			director.run(cocos.scene.Scene(ErrorLayerAudio()))
		if not self.tracker.open(self.camera_config):
			director.run(cocos.scene.Scene(ErrorLayerTracker()))
		# director.set_depth_test()
		self.behavior_loader = BehaviorLoader.BehaviorLoader()
		# Some more locals
		director.interpreter_locals['objects'] = self.objects
		director.interpreter_locals['options'] = self.options
		director.interpreter_locals['loaded_behaviors'] = self.behavior_loader.behaviors
		director.interpreter_locals['app'] = app
		director.interpreter_locals['config'] = config
		director.interpreter_locals['errors'] = errors
		director.interpreter_locals['filter'] = filter
		director.interpreter_locals['play'] = play
		director.interpreter_locals['shakemenus'] = shakemenus
		director.interpreter_locals['tools'] = tools
		
		pyglet.clock.set_fps_limit(60)
		director.run(self.config_scene)
	
	def is_in_play(self):
		"""Tell if the application is in the play scene."""
		return self.in_play
	
	def is_in_config(self):
		"""Tell if the application is in the configuration scene."""
		return not self.in_play
	
	def to_play(self):
		"""Go to the play scene."""
		self.tracker.start()
		self.audio.start()
		director.replace(FadeTransition(self.play_scene, duration=0.25))
		self.in_play = True
	
	def to_config(self):
		"""Go to the configuration scene."""
		self.tracker.stop()
		self.audio.stop()
		director.replace(FadeTransition(self.config_scene, duration=0.25))
		self.in_play = False
	
	def change_filter(self, filter):
		"""Change the filtering method currently used by the one specified (as an instance of a filter)."""
		self.filter = filter
		self.object_manager.change_filter()
	
	def uses_filter_thread(self):
		"""Tell if the application runs a separate thread for filtering operations."""
		return self.filter_thread != None
	
	def toggle_filter_thread(self):
		"""Toggle the usage of a separate thread for filtering operations."""
		if self.uses_filter_thread():
			self.filter_thread = FilterThread.run_filter_thread()
		else:
			self.filter_thread = None
	
	def on_new_object_appears(self, object):
		"""Dispatch a 'on_new_object' event."""
		self.dispatch_event('on_new_object', object)

Application.register_event_type('on_new_object')