from pyash.core.componenttype import ComponentType

#not really sure if I need this...

class ComponentMapper(object):
	"""Provides super fast Component retrieval from Entity objects"""
	def __init__(self, component_class):
		self.component_type = ComponentType.get_for(component_class)

	def get(self, entity):
		"""returns the Component of the specified class belonging to entity"""
		return entity.get_component(self.component_type)

	def has(self, entity):
		"""returns whether or not the entity has the component of the specified class"""
		return entity.has_component(self.component_type)

	@classmethod
	def get_for(cls, component_class):
		"""component_class: Component class to be retrieved by mapper.
		returns a new instance that provides fast access to the Component of the specified class"""
		return cls(component_class)

