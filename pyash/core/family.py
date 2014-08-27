from pyash.signals import Signal, Listener
from pyash.bits import Bits
from pyash.core.componenttype import ComponentType

class Family(object):
	"""Represents a group of Components. It is used to describe what Entity objects
	an EntitySystem should process.

	Example: Family.get_for(PositionComponent, VelocityComponent)

	Families can't be instantiated directly, but must be accessed via Family.get_for(). This
	is to avoid duplicate families that describe the same components.
	"""

	next_index = 0

	#hashmap holding all the families
	families = {}
	def __init__(self, bits_all=Bits(), bits_one=Bits(), bits_exclude=Bits()):
		"""Private constructor, don't use this.
		Use Family.getFamilyFor() instead"""

		#must contain all the components in the set
		self.bits_all = bits_all

		#must contain at least one of the components in the set
		self.bits_one = bits_one

		#cannot contain any of the components in the set
		self.bits_exclude = bits_exclude

		#each family has a unique index used for bitmasking
		self.index = Family.next_index
		Family.next_index += 1


	def get_index(self):
		"""return this family's unique index"""
		return self.index


	def matches(self, entity):
		"""whether the entity matches the family requirements or not"""
		entity_component_bits = entity.get_component_bits()
		if entity_component_bits.is_empty():
			return False

		i = self.bits_all.next_set_bit(0)
		while i is not None:
			if not entity_component_bits.get(i):
				return False

			i = self.bits_all.next_set_bit(i+1)

		if (not self.bits_one.is_empty()) and (not self.bits_one.intersects(entity_component_bits)):
			return False

		if (not self.bits_exclude.is_empty()) and (self.bits_exclude.intersects(entity_component_bits)):
			return False

		return True

	@classmethod
	def get_for_classes(cls, *component_classes):
		"""returns a family with the passed Component classes as a descriptor.
		each set of component types will always return the same family instance."""

		return cls.get_for_bits(ComponentType.get_bits_for(*component_classes), Bits(), Bits())

	@classmethod
	def get_for_bits(cls, bits_all=Bits(), bits_one=Bits(), bits_exclude=Bits()):
		"""bits_all: all entities will have to contain all of the components in the set
		bits_one: entities will have to contain at least one of the components in the set
		bits_exclude: entities cannot contain nay of the components in the set"""

		family_hash = cls.get_family_hash(bits_all, bits_one, bits_exclude)
		if family_hash in cls.families:
			return cls.families[family_hash]
		else:
			family = cls(bits_all, bits_one, bits_exclude)
			cls.families[family_hash] = family
			return family

	@classmethod
	def get_family_hash(cls, bits_all, bits_one, bits_exclude):
		s = ""
		s += "all:"
		s += cls.get_bits_string(bits_all)
		s += ",one:"
		s += cls.get_bits_string(bits_one)
		s += ",exclude:"
		s += cls.get_bits_string(bits_exclude)
		return s


	@classmethod
	def get_bits_string(cls, bits):
		s = ""
		num_bits = len(bits)
		for i in range(num_bits):
			if bits.get(i):
				s += "1"
			else:
				s += "0"

		return s

	def __eq__(self, other):
		if self is other:
			return True

		if other is None:
			return False

		if not issubclass(other, Family):
			return False

		if self.bits_all is None:
			if not (other.bits_all is None):
				return False
		else:
			if not (self.bits_all == other.bits_all):
				return True

		if self.bits_one is None:
			if not (other.bits_one is None):
				return False
		else:
			if not (self.bits_one == other.bits_one):
				return True

		if self.bits_exclude is None:
			if not (other.bits_exclude is None):
				return False
		else:
			if not (self.bits_exclude == other.bits_exclude):
				return True

		return self.index == other.index

	def __ne__(self, other):
		return not self.__eq__(other)


	def __hash__(self):
		prime = 31
		result = 1
		hash_val = 0
		if self.bits_all is not None:
			hash_val = hash(self.bits_all)
		else:
			hash_val = 0
		result = prime * result + hash_val

		if self.bits_one is not None:
			hash_val = hash(self.bits_one)
		else:
			hash_val = 0

		result = prime * result + hash_val

		if self.bits_exclude is not None:
			hash_val = hash(self.bits_exclude)
		else:
			hash_val = 0

		result = prime * result + hash_val

		return result
