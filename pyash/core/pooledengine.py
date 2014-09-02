from pyash.core.entity import Entity
from pyash.utils.reflectionpool import ReflectionPool
from pyash.utils.pool import Pool
from pyash.core.engine import Engine
import six

class ComponentPools(object):
	def __init__(self, initial_size=15, max_size=six.MAXSIZE):
		self.pools = {}
		self.initial_size = initial_size
		self.max_size = max_size

	def obtain(self, component_class):
		pool = None
		if component_class not in self.pools:
			pool = ReflectionPool(component_class, self.initial_size, self.max_size)
			self.pools[component_class] = pool
		else:
			pool = self.pools[component_class]

		return pool.obtain()

	def free(self, obj):
		if obj.__class__ not in self.pools:
			return

		pool = self.pools[obj.__class__]
		pool.free(obj)

	def free_all(self, objs):
		for obj in objs:
			if obj is None:
				continue
			self.free(obj)

class PooledEntity(Entity):
	def __init__(self, component_pools):
		super(PooledEntity, self).__init__()
		self.component_pools = component_pools

	def remove(self, component_type):
		component = super(PooledEntity, self).remove(component_type)
		self.component_pools.free(component)
		return component
	def reset():
		self.remove_all()
		self.flags = 0

class EntityPool(Pool):
	def __init__(self, component_pools, 
		initial_capacity=16, 
		max_capacity=six.MAXSIZE):
		super(EntityPool, self).__init__(initial_capacity, max_capacity)
		self.component_pools = component_pools

	def new_object(self):
		return PooledEntity(self.component_pools)


class PooledEngine(Engine):
	def __init__(self, entity_pool_initial_size=10,
		entity_pool_max_size=100,
		component_pool_initial_size=10,
		component_pool_max_size=100):
		super(PooledEngine, self).__init__()

		self.component_pools = ComponentPools(component_pool_initial_size,
			component_pool_max_size)

		self.entity_pool = EntityPool(
			self.component_pools,
			entity_pool_initial_size, 
			entity_pool_max_size)

		def clear_pools(self):
			self.entity_pool.clear()
			self.component_pools.clear()


		def create_entity(self):
			"""return clean entity from the engine pool.
			In order to add it to the Engine, use add_entity()"""
			self.entity_pool.obtain()

		def remove_entity(self, entity):
			super(PooledEngine, self).remove_entity(entity)
			self.entity_pool.free(entity)

		def create_component(self, component_class):
			"""Retrieves a new Component from the Engine pool.
			It will be placed back in the pool whenever it's removed from an Entity or the
			Entity itself is removed."""
			return self.component_pools.obtain(component_class)



