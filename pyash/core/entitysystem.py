

class EntitySystem(object):
	"""abstract class for processing sets of Entity objects"""

	def __init__(self, priority=0):
		"""Initialises the EntitySystem with the priority speecified.
		priority: the priority to execute this system with (lower means higher priority)."""
		self.priority = priority

	def added_to_engine(self, engine):
		"""called when this EntitySystem is added to an Engine.
		engine: the Engine that this system was added to."""
		pass


	def removed_from_engine(self, engine):
		"""called when this EntitySystem is removed from an Engine.
		engine: the Engine that this system was removed from."""
		pass

	def update(self, deltatime):
		"""update method called every tick.
		deltatime, time passed since last frame in seconds"""
		pass


	def check_processing(self):
		return True
