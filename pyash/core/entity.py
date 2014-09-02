from pyash.signals import Signal, Listener
from pyash.core.componenttype import ComponentType
from pyash.bits import Bits

class Entity(object):
	"""Simple containers of Components that give them "data". The component's data 
	is then processed by EntitySystem's"""
	#static
	next_index=0

	def __init__(self):
		"""Creates an empty Entity"""
		#collection that holds all the components indexed by their ComponentType index
		self.components = {}

		#auxiliary array for user access to all the components of an entity
		self.components_array = []

		#a flag that can be used to bit mask this entity (user managed)
		self.flags = 0

		#will dispatch an event when a component is added
		self.component_added = Signal()

		#will dispatch an event when a component is removed
		self.component_removed = Signal()

		#describing all the components in this entity for quick matching
		self.component_bits = Bits() 

		#describing all the systems this entity was matched with
		self.family_bits = Bits()

		self.index = Entity.next_index
		Entity.next_index += 1

	def get_component_by_class(self, component_class):
		return self.get_component(ComponentType.get_for(component_class))
	def get_components(self):
		return self.components_array

	def get_component_bits(self):
		"""This Entity's Component bits, describing all the Component's it contains"""
		return self.component_bits

	def get_family_bits(self):
		"""This Entity's Family bits, describing all the EntitySystem's it is currently
		being processed by"""
		return self.family_bits

	def get_component(self, component_type):
		"""return the Component object for the specified class. None if the Entity
		does not have any components for that class"""
		component_type_index = component_type.get_index()
		if component_type_index < len(self.components):
			return self.components[component_type.get_index()]
		else:
			return None

	def has_component(self, component_class):
		return self.component_bits.get(component_class.get_index())

	def get_index(self):
		"""return the Etity's unique index"""
		return self.index;

	def add(self, component):
		"""Adds a Component to this Entity. If a Component of the same type already exists,
		it will be replaced.
		Returns self for easy chaining"""
		component_class = component.__class__
		for c in self.components_array:
			if c.__class__ == component_class:
				del self.components_array[c]
				break

		component_class_index = ComponentType.get_index_for(component_class)
		self.components[component_class_index] = component
		self.components_array.append(component)

		self.component_bits.set(component_class_index)

		self.component_added(self)
		return self

	def remove(self, component_class):
		"""Removes the Componenet of the specified type. Since there is only
		ever one component of one type, we don't need an instance reference.
		returns the removed component"""
		component_class_index = ComponentType.get_index_for(component_class)
		remove_component = self.components[component_class_index]

		if remove_component != None:
			del self.components[component_class_index]
			self.components_array.remove(remove_component)
			self.component_bits.clear(index=component_class_index)

			self.component_removed(self)

	def remove_all(self):
		"""removes all the Components from an Entity"""
		while len(self.components_array) > 0:
			self.remove(self.components_array[0].__class__)

	def hash_code(self):
		return self.index

	def __eq__(self, other):
		if self is other:
			return True
		if other == None:
			return False
		if not issubclass(other.__class__, Entity):
			return False

		return self.index == other.index

	def __ne__(self, other):
		return not self.__eq__(other)