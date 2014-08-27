from pyash.signals import Signal, Listener
from pyash.bits import Bits


class ComponentType(object):
	"""Uniquely identifies a Component subclass.
	It assigns them an index which is used internally for fast comparison and retrieval.
	see Family and Entity.
	You cannot instantiate a component type. They can only be accessed via 
	getIndexFor(Component). Each component class will always return the same instance of
	ComponentType."""
	#hashmap to keep track of all Component subclasses hashed by their Class
	component_classes = {}
	next_index=0

	def __init__(self):
		self.index = ComponentType.next_index
		ComponentType.next_index += 1

	def get_index(self):
		"""return this ComponentTypes's unique index"""
		return self.index

	@classmethod
	def get_for(cls, component_class):
		if component_class in cls.component_classes:
			return cls.component_classes[component_class]
		else:
			ct = cls()
			cls.component_classes[component_class] = ct
			return ct

	@classmethod
	def get_index_for(cls, component_class):
		return cls.get_for(component_class).get_index()

	@classmethod
	def get_bits_for(cls, *component_classes):
		"""return bits representing the collection of components for quick
		comparison and matching. See Family get_for(bits, bits, bits)"""
		bits = Bits()
		type_classes_length = len(component_classes)
		for i in range(type_classes_length):
			bits.set(cls.get_index_for(component_classes[i]))

		return bits

	def hash_code(self):
		return self.index

	def __eq__(self, other):
		if self is obj:
			return True
		if obj == None:
			return False
		if not issubclass(other, ComponentType):
			return False

		return self.index == other.index

	def __ne__(self, other):
		return not self.__eq__(other)