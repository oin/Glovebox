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

"""The object node module."""

from . import Graphics2d
import cocos
from pyglet.gl import *

class CircleNode(cocos.cocosnode.CocosNode):
	def __init__(self, color = (1, 1, 1)):
		super(CircleNode, self).__init__()
		self.color = color
	
	def draw(self, *args, **kwargs):
		super(CircleNode, self).draw(args, kwargs)
		glPushMatrix()
		self.transform()
		color = self.color + (self.opacity,)
		Graphics2d.draw_circle(0, 0, 1, color)
		glPopMatrix()

class RectNode(cocos.cocosnode.CocosNode):
	def __init__(self, width, height, color = (1, 1, 1)):
		super(RectNode, self).__init__()
		self.color = color
		self.width = width
		self.height = height

	def draw(self, *args, **kwargs):
		super(RectNode, self).draw(args, kwargs)
		glPushMatrix()
		self.transform()
		color = self.color + (self.opacity,)
		Graphics2d.draw_rect(0, 0, self.width, self.height, color)
		glPopMatrix()

class RingNode(cocos.cocosnode.CocosNode):
	def __init__(self, inner = 0.5, color = (1, 1, 1)):
		super(RingNode, self).__init__()
		self.inner = inner
		self.color = color

	def draw(self, *args, **kwargs):
		super(RingNode, self).draw(args, kwargs)
		glPushMatrix()
		self.transform()
		color = self.color + (self.opacity,)
		Graphics2d.draw_ring(0, 0, self.inner, 1, color)
		glPopMatrix()