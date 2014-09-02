class SnapshotArray(list):
	"""Guarantees that array entries provided by begin()"""
	def __init__(self):
		list.__init__(self)
		self.recycled = None
		self.snapshot = None
		self.snapshots = 0

	def begin(self):
		"""Returns the backing array, which is guaranteed to  not be modified
		before end()"""
		self.modified()
		self.snapshot = self[:]
		self.snapshots += 1
		return self.snapshot

	def end(self):
		"""Releases the guarantee tha tth earray returned by begin()
		won't be modified"""
		self.snapshots = max(0, self.snapshots-1)
		if self.snapshot is None:
			return

		if self.snapshot != self and self.snapshots == 0:
			#the backing array was copied, keep around the old array
			self.recycled = self.snapshot[:]
			for i in range(len(self.recycled)):
				self.recycled[i] = None

			self.snapshot = None

	def modified(self):
		if ((self.snapshot is None) or (self.snapshot != self)):
			return
		#snapshot is in use, copy backing array to recycled array
		#or create a new backing array
		if (self.recycled is not None):
			self[:] = self.recycled[:]
			self.recycled = None


	def __setitem__(self, key, item):
		self.modified()
		list.__setitem__(self, key, item)

	def append(self, item):
		self.modified()
		list.append(self, item)


	def remove(self, item):
		self.modified()
		list.remove(self, item)

	def reverse(self):
		self.modified()
		list.reverse(self)

	def pop(self):
		self.modified()
		return list.pop(self)

	def sort(self, key=None):
		self.modified()
		list.sort(self, key)

	def __setslice__(self, i, j, seq):
		self.__setitem__(slice(i, j), seq)

