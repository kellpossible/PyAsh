class EntityListener(object):
	"""gets notified of Entity related events."""

	def entity_added(self, entity):
		"""called whenever an Entity is added to Engine"""
		pass

	def entity_removed(self, entity):
		"""called whenever an Entity is removed from Engine"""
		pass