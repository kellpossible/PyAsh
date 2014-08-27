import copy

class Bits(object):
	"""a bitset, without size limitation, allows comparison via bitwise
	to other bitfields"""

	def __init__(self, nbits=None, bits=None):
		if bits == None:
			self.bits = [0]
		else:
			self.bits = bits
		self.word_size = 6
		self.n_bits_mask = 2**self.word_size - 1

		if nbits != None:
			self.check_capacity((nbits >> self.word_size) + 1)

	def check_capacity(self, length):
		if (length >= len(self.bits)):
			diff = length - len(self.bits)
			for i in range(diff): #need to check this is working right
				self.bits.append(0)

	def get_word_indices(self, index):
		i1 = (index + 1) >> self.word_size
		i2 = index - i1 * self.n_bits_mask
		return i1, i2

	def get(self, index):
		"""index of the bit
		returns whether or not the bit is set"""
		word, local_index = self.get_word_indices(index)
		if word >= len(self.bits):
			return False
		return (self.bits[word] & (1 << (local_index & self.n_bits_mask))) != 0

	

	def getAndClear(self, index):
		"""index of the bit
		returns whether or not the bit is set
		also clears the bit"""
		word, local_index = self.get_word_indices(index)
		if word >= len(self.bits):
			return False
		
		old_bits = self.bits[word]
		self.bits[word] &= ~(1 << (local_index & self.n_bits_mask))
		return self.bits[word] != old_bits

	def getAndSet(self, index):
		word, local_index = self.get_word_indices(index)
		self.check_capacity(word + 1)
		old_bits = self.bits[word]
		self.bits[word] |= 1 << (local_index & self.n_bits_mask)
		return self.bits[word] == old_bits

	def set(self, index):
		word, local_index = self.get_word_indices(index)
		self.check_capacity(word + 1)
		self.bits[word] |= 1 << (local_index & self.n_bits_mask)

	def flip(self, index):
		word, local_index = self.get_word_indices(index)
		self.check_capacity(word)
		self.bits[word] ^= 1 << (local_index & self.n_bits_mask)

	def clear(self, index=None):
		""" if index==None, clears the entire bitset
		otherwise clear a particular index"""
		if index == None:
			length = len(self.bits)

			for i in range(length):
				self.bits[i] = 0
		else:
			word, local_index = self.get_word_indices(index)
			if word >= len(self.bits):
				return

			self.bits[word] &= ~(1 << (local_index & self.n_bits_mask))


	def next_set_bit(self, from_index):
		"""returns the index of the first bit that is set to True that occurs
		on or after the specified starting index. if it doesn't exist, it returns
		None"""
		word, local_index = self.get_word_indices(from_index)
		bits_length = len(self.bits)
		if word >= bits_length:
			return None

		bits_at_word = self.bits[word]
		if bits_at_word != 0:
			for i in range(from_index & self.n_bits_mask, self.n_bits_mask+1):
				if (bits_at_word & (1 << (i & self.n_bits_mask))) != 0:
					return (word << self.word_size) + i

		word += 1
		while word < bits_length:
			bits_at_word = self.bits[word]

			if bits_at_word != 0:
				for i in range(self.n_bits_mask+1):
					if (bits_at_word & (1 << (i & self.n_bits_mask))) != 0:
						return (word << self.word_size) + i - word
			
			word += 1
		
		return None



	def num_bits(self):
		"""returns the number of bits currently stored (not the highest set bit)"""
		return len(self.bits) << 6


	def length(self):
		"""returns the "logical size" of this bitset: the index of the highest set
		bit in the bitset plus one. Returns zero when the bitset contains no set bits"""
		length = len(self.bits)
		word = length - 1
		while word >= 0:
			bits_at_word = self.bits[word]
			if bits_at_word != 0:
				bit = self.n_bits_mask
				while bit >= 0:
					if (bits_at_word & (1 << (bit & self.n_bits_mask))) != 0:
						return (word << self.word_size) + bit - word

					bit -= 1
			word -= 1

		return 0

	def __len__(self):
		return self.length()

	def is_empty(self):
		"""returns True if this bitset contains no bits that are set to True"""
		length = len(self.bits)
		for i in range(length):
			if self.bits[i] != 0:
				return False

		return True

	def logic_and(self, other):
		"""performs a logical & between the bit sets"""
		i = 0
		j = len(self.bits)
		k = len(other.bits)
		bits = copy.copy(self.bits)
		while (i<j) and (i<k):
			bits[i] &= other.bits[i]
			i+=1

		return Bits(bits=bits)


	def logic_nand(self, other):
		"""clears all of the bits in this bit set whose corresponding
		bit is set in the other bit set"""
		i = 0
		j = len(self.bits)
		k = len(other.bits)
		bits = copy.copy(self.bits)
		while (i<j) and (i<k):
			bits[i] &= ~other.bits[i]
			i+=1

		return Bits(bits=bits)

	def logic_or(self, other):
		"""performs a logical OR of this bitset and the other bitset."""
		i = 0
		j = len(self.bits)
		k = len(other.bits)
		bits = copy.copy(self.bits)
		while (i<j) and (i<k):
			bits[i] |= other.bits[i]
			i+=1

		return Bits(bits=bits)


	def logic_xor(self, other):
		"""performs a logical XOR of this bitset and the other bitset."""
		i = 0
		j = len(self.bits)
		k = len(other.bits)
		bits = copy.copy(self.bits)
		while (i<j) and (i<k):
			bits[i] ^= other.bits[i]
			i+=1

		return Bits(bits=bits)

	def intersects(self, other):
		"""Returns true if the specified bit set has any bits set to true that are
		also set to true in this bit set"""

		i = min(len(self.bits), len(other.bits)) - 1
		while i >= 0:
			if (self.bits[i] & other.bits[i]) != 0:
				return True
			i-=1

	def __eq__(self, other):
		if self is other:
			return True
		if other == None:
			return False
		if not issubclass(other, Bits):
			return False

		compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
		return compare(self.bits, other.bits)

	def __ne__(self, other):
		return not self.__eq__(other)

	def __repr__(self):
		s = "Bits: "
		s += self.to_bitstr(True)
		return s

	def int_to_bitstr(self, n):
		s = ""
		for i in range(self.n_bits_mask):
			if (n & (1 << (i & self.n_bits_mask))) != 0:
				s += "1"
			else:
				s += "0"
		return s

	def to_bitstr(self, word_break=False):
		s = ""
		for word in self.bits:
			s += self.int_to_bitstr(word)
			if word_break:
				s += " "
		return s


	def __hash__(self):
		return hash(tuple(self.bits))