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

"""The behavior loading module."""

import os
import sys
import inspect
from cocos.director import director
import imp
import subprocess

def glovebox_path():
	"""Return the path of the glovebox application, one level to the top of the glovebox package."""
	return os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe() ))[0], "..", ".."))

def behavior_path():
	"""Return the absolute path for behaviors."""
	return os.path.abspath(os.path.join(glovebox_path(), "behaviors"))

class BehaviorLoader(object):
	"""A behavior loader scans the `behaviors` directory and loads any well-formed behavior.
	
	A behavior is well-formed when it is put in a certain way in the `behaviors` directory. To be well-formed, a behavior called 'hello_world' must be defined as a subclass of Behavior with the name HelloWorldBehavior, in the module `hello_world.py`, in a directory `hello_world`, somewhere in the `behaviors` directory. Moreover, the module must exhibit three global variables :
	behavior_name -- A string specifying the name that will be shown in the application.
	behavior_description -- A string specifying a short description of the behavior.
	behavior_menu -- A list of strings specifying the path to get to this behavior on the default behavior menu."""
	def __init__(self):
		"""Initialize the loader and add the glovebox path to the execution path."""
		super(BehaviorLoader, self).__init__()
		# Adds the glovebox/ root to the path
		if glovebox_path() not in sys.path:
			sys.path.insert(0, glovebox_path())
		# Define a dictionary for module loading
		self.behaviors = {}
		# Walk the behaviors directory and load everything we can !
		self.walk_and_load()
	
	def open_behavior_directory(self):
		"""Open the behavior folder with the default GUI browser."""
		if sys.platform == "win32":
			subprocess.Popen(['start', behavior_path()], shell=True)
		elif sys.platform == "darwin":
			subprocess.Popen(['open', behavior_path()])
		else:
			try:
				subprocess.Popen(['xdg-open', behavior_path()])
			except OSError:
				pass
	
	def walk_and_load(self):
		"""Traverse the behavior directory to list and load any well-formed behavior."""
		for path, dirs, files in os.walk(behavior_path()):
			if os.path.basename(path) == '_lib':
				continue
			for file in files:
				name, extension = os.path.splitext(file)
				if name and name == os.path.basename(path) and extension == '.py':
					full_module = os.path.join(path, file)
					try:
						self.behaviors[name] = BehaviorModule(name, full_module)
					except:
						print "Incorrect behavior: %s" % full_module
						pass

class BehaviorModule(object):
	"""A behavior module represents the available information about a behavior.
	
	This information includes its name, its path and how to instantiate it."""
	def __init__(self, name, fullpath):
		"""Initialize the behavior module and load the corresponding Python module."""
		super(BehaviorModule, self).__init__()
		self.name = name
		self.fullpath = fullpath
		self.module = imp.load_source(name, fullpath)
		self.class_obj = getattr(self.module, ''.join([x.title() for x in name.split('_')]) + 'Behavior') # audio_in => AudioInBehavior
		self.description = getattr(self.module, 'behavior_description')
		self.menu = getattr(self.module, 'behavior_menu')
		self.display_name = getattr(self.module, 'behavior_name')
	
	def create_instance(self):
		"""Create an instance of the represented behavior."""
		return self.class_obj()