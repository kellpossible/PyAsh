from Vector import Vector3, Rotation
from kivy.app import App
from pyash.core.engine import Engine
from pyash.systems.iteratingsystem import IteratingSystem
from pyash.core.component import Component
from pyash.bits import Bits
from pyash.signals import Signal, Listener
from pyash.core.family import Family
from pyash.core.componenttype import ComponentType
from pyash.core.entity import Entity

import sys
sys.path.append('../..')

class VectorComponent(Component):
	def __init__(self, vec=Vector3()):
		self.vec = vec

	def reset(self):
		self.vec = Vector3()

class ConnectedParentComponent(Component):
	def __init__(self, parent=None):
		self.parent = parent

	def reset(self):
		self.parent = None

class DirectionComponent(Component):
	def __init__(self, angle=0):
		self.angle = angle

	def reset(self):
		self.angle = 0

class PositionComponent(VectorComponent):
	pass

class VelocityComponent(VectorComponent):
	pass


class ForceSum(Signal):
	def __call__(self, obj):
		f_sum = Vector3()
		for l in self:
			f_sum.add(l.receive(self, obj))

		return f

class ForceComponent(Component):
	def __init__(self):
		self.force = ForceSum()

class ParentComponent(Component):
	def __init__(self, parent):
		self.parent = parent

class ChildrenComponent(Component):
	def __init__(self, *children):
		self.children = children

class SailComponent(Component):
	def __init__(self):
		


class GraphicsComponent(Component):
	def __init__(self, *graphics_list):
		self.graphics_list = graphics_list

class ParentTransformComponent(Component):
	def __init__(self, parent_entity):
		self.parent_entity = parent_entity

class SailSystem(IteratingSystem):
	family = Family.get_for_classes(SailComponent)


class RenderingSystem(IteratingSystem):
	family = Family.get_for_classes(GraphicsComponent)
	def __init__(self):
		super(RenderingSystem, self).__init__(self.family)

	def process_entity(self, entity, deltatime):
		print(entity, deltatime)



if __name__ == '__main__':
	engine = Engine()
	e1 = Entity()
	engine.add_entity(e1)
	e1.add(GraphicsComponent())

	rs = RenderingSystem()
	engine.add_system(rs)

	engine.update(1.0)
