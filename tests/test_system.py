import unittest
import time
from pyash.core.engine import Engine
from pyash.core.entity import Entity
from pyash.core.entitylistener import EntityListener
from pyash.signals import Listener
from pyash.core.component import Component
from pyash.core.componenttype import ComponentType
from pyash.core.family import Family
from pyash.bits import Bits
from pyash.systems.iteratingsystem import IteratingSystem
from pyash.core.componentmapper import ComponentMapper

class VelocityComponent(Component):
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def __repr__(self):
		return "Velocity (x:{0} y:{1} z:{2})".format(self.x, self.y, self.z)

class PositionComponent(Component):
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def __repr__(self):
		return "Position (x:{0} y:{1} z:{2})".format(self.x, self.y, self.z)

class TestIteratingSystem(IteratingSystem):
	def __init__(self):
		self.family = Family.get_for_classes(PositionComponent, VelocityComponent)
		super(TestIteratingSystem, self).__init__(self.family)
		self.pm = ComponentMapper.get_for(PositionComponent)
		self.vm = ComponentMapper.get_for(VelocityComponent)

	def process_entity(self, entity, deltatime):
		pos = self.pm.get(entity)
		vel = self.vm.get(entity)

		pos.x += vel.x * deltatime
		pos.y += vel.y * deltatime
		pos.z ++ vel.z * deltatime

class SystemTest(unittest.TestCase):
	def test_system(self):
		Engine.reset_indices()
		s = TestIteratingSystem()
		e1 = Entity()
		vel = VelocityComponent(1,0,0)
		pos = PositionComponent()
		e1.add(vel)
		e1.add(pos)
		engine = Engine()
		engine.add_entity(e1)
		engine.add_system(s)

		for i in range(10):
			engine.update(0.5)

		self.assertEqual(pos.x, 5.0)


if __name__ == '__main__':
	unittest.main()