from pyash.signals import Listener, Signal
import six

class Engine(object):
	"""The heart of the Entity framework. It is responsible for keeping track of Entity
	and managing EntitySystem objecs. The engine should be updated every tick via the update()
	method.

	With the engine you can:
	- add/remove Entity objects
	- add/remove EntitySystems
	- obtain a list of entities for a specific Family
	- update the main loop
	- register/unregister EntityListener objects
	"""

	def __init__(self):
		#an unordered array that holds all the entities in the Engine
		self.entities = []

		#an unordered list of EntitySystem
		self.systems = []

		#a hashmap that organises EntitySystem's by class for easy retrieval
		self.systems_by_class = {}

		#a hashmap that organises all entities into family buckets
		self.families = {}

		#a collection of entity added/removed event entity listeners
		self.entity_listeners = []

		#EntityListeners that await removal
		self.removal_pending_listeners = []

		#whether of not the entity listeners are being notified of an event
		self.notifying = False

		#a listener for the engine that's called every time a component is added
		self.component_added_listener = Listener(lambda signal, obj: self.component_added(obj))

		#a listener for the engine that's called every time a component is removed
		self.component_removed_listener = Listener(lambda signal, obj: self.component_removed(obj))

	def get_entities(self):
		return self.entities

	def add_entity(self, entity):
		self.entities.append(entity)

		for family, family_entities in six.iteritems(self.families):
			if family.matches(entity):
				family_entities.append(entity)
				entity.get_family_bits().set(family.get_index())

		entity.component_added.append(self.component_added_listener)
		entity.component_removed.append(self.component_removed_listener)

		self.notifying = True
		for entity_listener in self.entity_listeners:
			entity_listener.entity_added(entity)
		self.notifying = False
		self.remove_pending_listeners()

	def remove_entity(self, entity):
		self.entities.remove(entity)

		if not entity.get_family_bits().is_empty():
			for family, family_entites in six.iteritems(self.families):
				if family.matches(entity):
					family_entries.remove(entity)
					entity.get_family_bits().clear(family.get_index())


		entity.component_added.remove(self.component_added_listener)
		entity.component_removed.remove(self.component_removed_listener)

		self.notifying = True
		for entity_listener in self.entity_listeners:
			entity_listener.entity_removed(entity)

		self.notifying = False
		self.remove_pending_listeners()

	def remove_all_entities(self):
		while len(self.entities) > 0:
			self.remove_entity(self.entities[0])

	def add_system(self, system):
		system_class = system.__class__
		if not (system_class in self.systems_by_class):
			self.systems.add(system)
			self.systems_by_class[system_class] = system
			system.added_to_engine(self)
			#self.systems.sort(comparator)

	def remove_system(self, system):
		if system in self.systems:
			self.systems.remove(system)
			self.systems_by_class.remove(system.__class__)
			self.system.reomve_from_engine(self)

	def get_system(self, system_class):
		return self.systems_by_class[system_class]

	def get_entities_for(self, family):
		"""returns a collection of entities for the specified Family.
		will return the same instance every time"""

		entities = self.families[family]

		if entities is None:
			entities = []
			for entity in self.entities:
				if family.matches(entity):
					entities.append(entity)
					entity.get_family_bits().set(family.get_index())

			self.families[family] = entities

		return entities


	def add_entity_listener(self, entity_listener):
		"""adds an EntityListener"""
		self.entity_listeners.append(entity_listener)


	def remove_entity_listener(self, entity_listener):
		"""Removes an EntityListener"""
		if self.notifying:
			self.removal_pending_listeners.add(entity_listener)
		else:
			listeners.remove(entity_listener)

	def update(self, deltatime):
		"""updates all the systems in this engine.
		deltatime: time passed since last frame."""

		for i in range(len(systems)):
			if systems[i].check_processing():
				systems[i].update(deltatime)

	def component_added(self, entity):
		for family, family_entites in self.families.iteritems():
			if not (entity.get_family_bits().get(family.get_index())):
				if family.matches(entity):
					family_entites.append(entity)
					entity.get_family_bits().set(family.get_index())

	def component_removed(self, entity):
		for family, family_entites in self.families.iteritems():
			if entity.get_family_bits().get(family.get_index()):
				if not family.matches(entity):
					family_entites.remove(entity)
					entity.get_family_bits().clear(family.get_index())


	def remove_pending_listeners(self):
		for listener in self.removal_pending_listeners:
			self.listeners.remove(listener)

		#clear the list
		self.removal_pending_listeners[:] = []