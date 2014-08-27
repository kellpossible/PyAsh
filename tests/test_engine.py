import unittest
from pyash.core.engine import Engine
from pyash.core.entity import Entity
from pyash.core.entitylistener import EntityListener
from pyash.signals import Listener
from pyash.core.component import Component
from pyash.core.componenttype import ComponentType
from pyash.core.family import Family
from pyash.bits import Bits

ENTITY_ADDED = None
ENTITY_REMOVED = None
COMPONENT_ADDED = None
COMPONENT_REMOVED = None


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

class StaticComponent(Component):
	pass

def reset_component_listener_test():
	global COMPONENT_REMOVED
	global COMPONENT_ADDED
	COMPONENT_ADDED = None
	COMPONENT_REMOVED = None

def reset_entity_listener_test():
	global ENTITY_ADDED
	global ENTITY_REMOVED
	ENTITY_ADDED = None
	ENTITY_REMOVED = None

class TestComponentAddedListener(Listener):
	def receive(self, signal, obj):
		global COMPONENT_ADDED
		COMPONENT_ADDED = obj

class TestComponentRemovedListener(Listener):
	def receive(self, signal, obj):
		global COMPONENT_REMOVED
		COMPONENT_REMOVED = obj

class TestEntityListener(EntityListener):
	def entity_added(self, entity):
		global ENTITY_ADDED
		ENTITY_ADDED = entity

	def entity_removed(self, entity):
		global ENTITY_REMOVED
		ENTITY_REMOVED = entity

class EngineTest(unittest.TestCase):
	def test_add_entity(self):
		global ENTITY_ADDED
		global ENTITY_REMOVED

		Engine.reset_indices()
		engine = Engine()
		engine.add_entity_listener(TestEntityListener())
		e1 = Entity()
		engine.add_entity(e1)
		entities = engine.get_entities()
		self.assertEqual(e1, entities[0])
		self.assertTrue(e1.component_added[0] is engine.component_added_listener)
		self.assertTrue(e1.component_removed[0] is engine.component_removed_listener)

		self.assertEqual(ENTITY_ADDED, e1)
		reset_entity_listener_test()

	def test_remove_entity(self):
		global ENTITY_ADDED
		global ENTITY_REMOVED

		Engine.reset_indices()
		engine = Engine()
		engine.add_entity_listener(TestEntityListener())
		e1 = Entity()
		engine.add_entity(e1)
		engine.remove_entity(e1)
		entities = engine.get_entities()
		self.assertEqual(len(entities), 0)
		self.assertEqual(len(e1.component_added), 0)
		self.assertEqual(len(e1.component_removed), 0)
		self.assertEqual(ENTITY_REMOVED, e1)
		reset_entity_listener_test()

		e2 = Entity()
		engine.add_entity(e1)
		engine.add_entity(e1)
		engine.remove_all_entities()
		entities = engine.get_entities()
		self.assertEqual(len(entities), 0)


	def test_component(self):
		global COMPONENT_REMOVED
		global COMPONENT_ADDED

		Engine.reset_indices()
		engine = Engine()
		e1 = Entity()
		c = VelocityComponent()
		e1.component_added.append(TestComponentAddedListener())
		e1.component_removed.append(TestComponentRemovedListener())
		engine.add_entity(e1)
		e1.add(c)
		self.assertEqual(COMPONENT_ADDED, e1)
		reset_component_listener_test()

		family = Family.get_for_bits(ComponentType.get_bits_for(VelocityComponent))
		entities = engine.get_entities_for(family)
		self.assertEqual(entities[0], e1)

		e1.remove(VelocityComponent)
		self.assertEqual(COMPONENT_REMOVED, e1)
		reset_component_listener_test()

if __name__ == '__main__':
	unittest.main()