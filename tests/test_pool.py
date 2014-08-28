import unittest
from pyash.utils.pool import Pool

class PoolableTest(object):
	def __init__(self):
		self.reset()

	def reset(self):
		self.x = 0

class TestingPool(Pool):
	def new_object(self):
		return PoolableTest()

class PoolTest(unittest.TestCase):
	def test_pool_basic(self):
		pool = TestingPool()

		pt_objs = []

		for i in range(10):
			pt = pool.obtain()
			pt.x = i
			pt_objs.append(pt)

		free_pt = pt_objs[2]
		self.assertEqual(free_pt.x, 2)
		pool.free(free_pt)
		self.assertEqual(free_pt.x, 0)
		del pt_objs[2]
		

		self.assertEqual(free_pt, pool.free_objects[0])
		self.assertEqual(pool.get_free(), 1)
		new_pt = pool.obtain()
		pt_objs.append(new_pt)
		self.assertEqual(pool.get_free(), 0)

		pool.free_all(pt_objs)
		self.assertEqual(pool.get_free(), 10)

		pool.clear()
		self.assertEqual(pool.get_free(), 0)



if __name__ == '__main__':
	unittest.main()