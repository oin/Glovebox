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

"""The main filtering module."""

from .. import libglovebox

class Filter(object):
	"""A filter affects an object's position and rotation in 3D space.
	
	This filter does nothing."""
	def __init__(self):
		"""Initialize a filter."""
		self.translation = libglovebox.Vec3f(0, 0, 0)
		self.rotation = libglovebox.Quaternion(0, 0, 0, 0)
	
	def reset(self, t, r):
		"""Reset the filter to given values."""
		self.translation = t
		self.rotation = r
	
	def filter(self, t, r):
		"""Calculate a step given new values."""
		self.translation = t
		self.rotation = r
	
	def copy(self):
		"""Return a filter with the same characteristics."""
		new = self.__class__()
		return new


class SimpleInterpolator(Filter):
	"""A simple exponential smoothing filter."""
	def __init__(self, q_t = 0.5, q_r = 0.5):
		"""Initialize a filter given a smoothing factor for translation and one for rotation."""
		super(SimpleInterpolator, self).__init__()
		self.coef_translation = q_t
		self.coef_rotation = q_r
	
	def filter(self, t, r):
		"""Smooth the new values.
		
		The translation part is effectively using a simple exponential smoothing algorithm, while the rotation part is using a quaternion slerp."""
		new_rotation = libglovebox.Quaternion(0, 0, 0, 0)
		new_rotation.slerp(self.coef_rotation, self.rotation, r)
		self.rotation = new_rotation
		self.translation = (1 - self.coef_translation) * self.translation + self.coef_translation * t
	
	def copy(self):
		"""Return a filter with the same characteristics."""
		new = super(SimpleInterpolator, self).copy()
		new.coef_translation = self.coef_translation
		new.coef_rotation = self.coef_rotation
		return new

class VirtualCoupling(Filter):
	"""An implementation of virtual coupling.
	
	Virtual coupling in improvised interfaces is detailed in [1]. The position of the virtual part of a tracked object, ie. of a behavior, is determined by a viscoelastic bound between a simulated point particle at the tracked object's coordinates and another point particle (at the filtered coordinates). The latter point particle represents a kind of ghost that seems to follow the physical object as if they were attached with by a spring. The filtering algorithm is then a simple physical model simulation.
	
	To summarize, the idea behind this virtual coupling is that jitter can be attenuated by conventional filters, but trying to keep a minimal latency doesn't work well with cameras, as the random capture conditions (luminosity, motion blur...). Even if latency is high, musical interaction is better when jitter is low, we could aim at increasing the latency and to make virtual coupling embody this latency as an observable process. We supposed that giving this kind of real-world feeling calls for a more controllable and more enjoyable interaction.
	
	[1] J. Aceituno, J. Castet, M. Desainte-Catherine, and M. Hachet. Improvised interfaces for real-time musical applications. In Proceedings of the sixth international conference on tangible, embedded and embodied interaction (TEI), 2012."""
	def __init__(self, k = 0.08, z = 0.05, q = 0.25):
		"""Initialize a virtual coupling, given a stiffness coefficient, a damping coefficient, and a smoothing factor for rotations."""
		super(VirtualCoupling, self).__init__()
		self.stiffness = k
		self.damping = z
		self.global_damping = 0.1
		self.mass = 1
		self.former_distance = 0
		self.former_position = libglovebox.Vec3f(0, 0, 0)
		self.raw_position = libglovebox.Vec3f(0, 0, 0)
		self.force = libglovebox.Vec3f(0, 0, 0)
		self.coef_rotation = q
	
	def reset(self, t, r):
		"""Reset the filter to the given values."""
		super(VirtualCoupling, self).reset(t, r)
		self.former_distance = 0
		self.former_position = t
		self.raw_position = t
		self.force = libglovebox.Vec3f(0, 0, 0)

	def filter(self, t, r):
		"""Calculate the next step of the simulation given new values."""
		# Update rotation with a slerp
		new_rotation = libglovebox.Quaternion(0, 0, 0, 0)
		new_rotation.slerp(self.coef_rotation, self.rotation, r)
		self.rotation = new_rotation
		# Update the translation with a physical model
		self.raw_position = libglovebox.Vec3f(t.x, t.y, t.z)
		self.update_position()
		self.update_force()
	
	def update_position(self):
		"""Update the virtual point particle position from the velocity and previously calculated forces.
		
		A discrete-time version of the second law of Newton is used to derive the position."""
		velocity = self.translation - self.former_position
		self.former_position = libglovebox.Vec3f(self.translation.x, self.translation.y, self.translation.z)
		self.translation += velocity - self.mass * (self.global_damping * velocity - self.force)
		self.force = libglovebox.Vec3f(0, 0, 0)
	
	def update_force(self):
		"""Update the force applied to the virtual point particle from the previously calculated particle positions.
		
		The forces are calculated using Hooke's law and taking damping into account."""
		difference = self.translation - self.raw_position
		distance = difference.length()
		
		f = self.stiffness * distance + self.damping * (distance - self.former_distance)
		self.former_distance = distance
		if distance != 0:
			self.force -= f / distance * difference

	def copy(self):
		"""Return a filter with the same characteristics."""
		new = super(VirtualCoupling, self).copy()
		new.stiffness = self.stiffness
		new.damping = self.damping
		new.global_damping = self.global_damping
		new.mass = self.mass
		new.coef_rotation = self.coef_rotation
		return new
