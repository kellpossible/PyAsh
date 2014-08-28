from pyash.utils.pool import Pool
import six

class ReflectionPool(Pool):
	"""Pool that creates new instances of a type using reflectino.
	type must have a zero argument constructor."""
	def __init__(self, obj_class, initial_capacity=16, max_capacity=six.MAXSIZE):
		super(ReflectionPool, self).__init__(initial_capacity, max_capacity)
		self.obj_class = obj_class

	def new_object(self):
		return self.obj_class()