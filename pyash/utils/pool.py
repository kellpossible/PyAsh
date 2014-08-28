import six

class Pool(object):
	"""a pool of objects that can be reused to avoid allocation.
	Objects used in this pool need to implement a reset method,
	to reset the object for reuse. This should set the object refs
	to None, and fields to default values."""
	def __init__(self, initial_capacity=16, max_capacity=six.MAXSIZE):
		self.free_objects = []

		#maximum number of objects that will be pooled
		self.max_capacity = max_capacity
		self.initial_capacity = initial_capacity

		#highest number of free objects. This can be
		#reset at any time.
		self.peak = 0


	def new_object(self):
		"""override this to implement getting a new object for the pool"""
		pass

	def obtain(self):
		"""Returns an object from this pool. The object may be new (from new_object) or
		reused (previously free(obj) freed)"""
		if len(self.free_objects) == 0:
			return self.new_object()
		else:
			return self.free_objects.pop()


	def free(self, obj):
		"""Puts the specified object in the pool, making it eligible 
		to be returned by obtain(). If the pool already has max_capacity 
		free objects, the specified object is reset, but not added to the pool."""
		free_objects_size = len(self.free_objects)
		if free_objects_size < self.max_capacity:
			self.free_objects.append(obj)
			self.peak = max(self.peak, len(self.free_objects))

		obj.reset()

	def free_all(self, objs):
		"""puts the specified array of objects in the pool. None objects within the array
		are silently ignored."""
		max_capacity = self.max_capacity
		free_objects_size = len(self.free_objects)
		for obj in objs:
			if obj is None:
				continue

			if free_objects_size < self.max_capacity:
				self.free_objects.append(obj)
				obj.reset()

			self.peak = max(self.peak, len(self.free_objects))


	def clear(self):
		"""removes all free objects from this pool"""
		self.free_objects[:] = []

	def get_free(self):
		"""the number of obejcts available to be obtained"""
		return len(self.free_objects)