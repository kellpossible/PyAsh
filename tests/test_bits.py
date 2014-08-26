import unittest
from pyash.bits import Bits


class BitsTest(unittest.TestCase):
	def test_bits_constructor(self):
		b = Bits(127, [0,1])
		self.assertEqual(b.to_bitstr(), "0"*63 + "1" + "0"*62)

	def test_bits_capacity(self):
		b = Bits(8)
		self.assertEqual(b.to_bitstr(), "0"*63)
		b = Bits(1)
		self.assertEqual(b.to_bitstr(), "0"*63)
		b = Bits(63)
		self.assertEqual(b.to_bitstr(), "0"*63)
		b = Bits(64)
		self.assertEqual(b.to_bitstr(), "0"*126)

	def test_bits_capacity_grow(self):
		b = Bits(1)
		b.set(64)
		self.assertEqual(b.to_bitstr(), "0"*63 + "01" + "0"*61)

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

	def test_bits_get(self):
		b = Bits(12)
		b.set(6)
		self.assertEqual(b.get(6), True)
		self.assertEqual(b.get(2), False)

	def test_bits_flip(self):
		b = Bits(63)
		b.set(0)
		b.set(2)
		b.flip(2)
		self.assertEqual(b.to_bitstr(), "1" + "0"*62)

		b = Bits(64)
		b.set(63)
		b.set(65)
		b.flip(63)
		self.assertEqual(b.to_bitstr(), "0"*63 + "0"*2 + "1" + "0"*60)

	def test_bits_logic_and(self):
		b1 = Bits(12)
		b2 = Bits(66)
		b1.set(0)
		b1.set(12)
		b2.set(12)
		b2.set(65)
		b3 = b1.logic_and(b2)
		self.assertEqual(b3.to_bitstr(), "0"*12 + "1" + "0"*50)
		b4 = b2.logic_and(b1)
		self.assertEqual(b4.to_bitstr(), "0"*12 + "1" + "0"*50 + "0"*2 + "1" + "0"*60)

	def test_bits_logic_or(self):
		b1 = Bits(12)
		b2 = Bits(66)
		b1.set(0)
		b1.set(12)
		b2.set(12)
		b2.set(65)
		b3 = b1.logic_or(b2)
		self.assertEqual(b3.to_bitstr(), "1" + "0"*11 + "1" + "0"*50)
		b4 = b2.logic_or(b1)
		self.assertEqual(b4.to_bitstr(), "1" + "0"*11 + "1" + "0"*50 + "0"*2 + "1" + "0"*60)

	def test_bits_clear(self):
		b = Bits(12)
		b.set(0)
		b.set(5)
		b.clear()
		self.assertEqual(b.to_bitstr(), "0"*63)
		b.set(1)
		b.set(2)
		b.clear(2)
		self.assertEqual(b.to_bitstr(), "01" + "0"*61)

	def test_bits_next_set(self):
		b = Bits(12)
		b.set(0)
		b.set(10)
		i = b.next_set_bit(2)
		self.assertEqual(i, 10)
		i = b.next_set_bit(12)
		self.assertEqual(i, None)
		b.set(67)
		i = b.next_set_bit(12)
		self.assertEqual(i, 67)
		b = Bits(12)
		b.set(170)
		i = b.next_set_bit(12)
		self.assertEqual(i, 170)

	def test_num_bits(self):
		b = Bits(12)
		self.assertEqual(b.num_bits(), 64)
		b.set(110)
		self.assertEqual(b.num_bits(), 128)

	def test_bits_length(self):
		b = Bits(12)
		b.set(5)
		length = b.length()
		self.assertEqual(length, 5)
		b.set(127)
		length = b.length()
		self.assertEqual(length, 127)
		b.clear()
		length = b.length()
		self.assertEqual(length, 0)


if __name__ == '__main__':
	unittest.main()