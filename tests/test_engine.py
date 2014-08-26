import unittest
from pyash.core.engine import Engine
from pyash.core.entity import Entity
from pyash.core.entitylistener import EntityListener

ENTITY_ADDED = None
ENTITY_REMOVED = None

def reset_entity_listener_test():
	global ENTITY_ADDED
	global ENTITY_REMOVED
	ENTITY_ADDED = None
	ENTITY_REMOVED = None

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


if __name__ == '__main__':
	unittest.main()