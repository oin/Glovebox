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

"""The filter thread module."""

import threading
import time as tm
from cocos.director import director

def filter_thread_func():
	"""Update every tracked object's associated filter at a rate of 100Hz."""
	while director.app.uses_filter_thread():
		if director.app.is_in_play():
			for id in director.app.objects:
				director.app.objects[id].update_filter()
			tm.sleep(1.0 / 100)
		else:
			tm.sleep(1.0 / 5)

def run_filter_thread():
	"""Start a separate thread devoted to updating every tracked object's associated filter."""
	filter_thread = threading.Thread(None, filter_thread_func)
	filter_thread.start()
	return filter_thread