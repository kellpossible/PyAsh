import unittest
from pyash.bits import Bits


class BitsTest(unittest.TestCase):
	def test_bits_capacity(self):
		b = Bits(8)
		self.assertEqual(b.to_bitstr(), "0"*63)
		b = Bits(1)
		self.assertEqual(b.to_bitstr(), "0"*63)
		b = Bits(63)
		self.assertEqual(b.to_bitstr(), "0"*63)
		b = Bits(64)
		self.assertEqual(b.to_bitstr(), "0"*126)

	def test_bits_set(self):
		b = Bits(64)
		b.set(0)
		self.assertEqual(b.to_bitstr(), "1" + "0"*125)
		b = Bits(1)
		b.set(62)
		self.assertEqual(b.to_bitstr(), "0"*62 + "1")
		b = Bits(1)
		b.set(63)
		self.assertEqual(b.to_bitstr(), "0"*63 + "1" + "0"*62)

	def test_bits_flip(self):
		b = Bits(63)
		b.set(0)
		b.set(2)
		b.flip(2)
		self.assertEqual(b.to_bitstr(), "1" + "0"*62)

	def test_bits_logic_and(self):
		pass

	def test_bits_logic_or(self):
		pass

	def test_bits_clear(self):
		pass

	def test_bits_next_set(self):
		pass

	def test_num_bits(self):
		pass

	def test_bits_length(self):
		pass





if __name__ == '__main__':
	unittest.main()