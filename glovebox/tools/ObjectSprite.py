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

"""The object sprite module."""

from cocos.sprite import Sprite
from pyglet.gl import *

class ObjectSprite(Sprite):
	def __init__(self, image, position=(0,0), rotation=0, scale=1, opacity = 255, color=(255,255,255), anchor = None):
		super(ObjectSprite, self).__init__(image, position, rotation, scale, opacity, color, anchor)
		
	def draw(self):
		if self.opacity == 0:
			return
		glPushMatrix()
		glScalef(2 * 1.0 / self.image.width * self.scale, 2 * 1.0 / self.image.height * self.scale, 1)
		super(ObjectSprite, self).draw()
		glPopMatrix()