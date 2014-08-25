from pyash.core.EntitySystem import EntitySystem

class IteratingSystem(EntitySystem):
	"""A simple EntitySystem that iterates over each entity and calls process_entity()
	for each entity every time the EntitySystem is updated. This is really just a 
	convenience class as most systems iterate over a list of entities."""

	def __init__(self, family, priority=0):
		"""Instantiates a system that will iterate over the entities described by the Family,
		with a specific priority.
		family: the family of entities iterated over in this system
		priority: the priority to execute this system with (lower means higher priority)"""
		super(IteratingSystem, self).__init__(priority)

		#the family describing this systems entities
		self.family = family

		#entities used by this system
		self.entities = []

		def added_to_engine(self, engine):
			self.entities = engine.get_entities_for(self.family)


		def removed_from_engine(self):
			self.entities[:] = []


		def update(self, deltatime):
			i = 0
			while i < len(self.entities):
				self.process_entity(self.entities[i], deltatime)
				i+=1


		def process_entity(self, entity, deltatime):
			"""This method is called on every entity on every update call of the EntitySystem.
			Override this to implement your system's specific processing.
			entity: the current entity being processed.
			delstatime: the delta time between the last and current frame"""
			pass