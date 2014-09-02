import unittest
from pyash.signals import Signal, Listener

SIGNAL_RECIEVED = None
OBJECT_RECIEVED = None

def reset_recieved():
	global SIGNAL_RECIEVED
	global OBJECT_RECIEVED
	SIGNAL_RECIEVED = None
	OBJECT_RECIEVED = None

class TestListener(Listener):
	def __init__(self):
		super(TestListener, self).__init__()

	def receive(self, signal, obj):
		global SIGNAL_RECIEVED
		global OBJECT_RECIEVED
		SIGNAL_RECIEVED = signal
		OBJECT_RECIEVED = obj

class RemoveWhileDispatchListenerMock(Listener):
	def __init__(self):
		super(RemoveWhileDispatchListenerMock, self).__init__()
		self.count = 0

	def receive(self, signal, obj):
		self.count += 1
		signal.remove(self)


class ListenerMock(Listener):
	def __init__(self):
		super(ListenerMock, self).__init__()
		self.count = 0

	def receive(self, signal, obj):
		self.count += 1

		if signal is None:
			raise Error()

		if obj is None:
			raise Error()

class Dummy(object):
	pass

class SignalsTest(unittest.TestCase):
	def test_signal_class(self):
		global SIGNAL_RECIEVED
		global OBJECT_RECIEVED
	
		s = Signal()
		l = TestListener()
		s.append(l)
		s(10)
		self.assertEqual(SIGNAL_RECIEVED, s)
		self.assertEqual(OBJECT_RECIEVED, 10)
	
		reset_recieved()
		s.remove(l)
		s(10)
		self.assertEqual(SIGNAL_RECIEVED, None)
		self.assertEqual(OBJECT_RECIEVED, None)

		reset_recieved()

	def test_signal_lambda(self):
		global SIGNAL_RECIEVED
		global OBJECT_RECIEVED

		s = Signal()
		l = Listener(lambda s, o: self.assign(s, o))

		s.append(l)
		s(10)
		self.assertEqual(SIGNAL_RECIEVED, s)
		self.assertEqual(OBJECT_RECIEVED, 10)

		reset_recieved()

	def test_signal_remove_while_dispatch(self):
		signal = Signal()
		dummy = Dummy()
		listenerA = RemoveWhileDispatchListenerMock()
		listenerB = ListenerMock()

		signal.append(listenerA)
		signal.append(listenerB)
		
		signal(dummy)

		self.assertEqual(listenerA.count, 1)
		self.assertEqual(listenerB.count, 1)


	def assign(self, s, o):
		global SIGNAL_RECIEVED
		global OBJECT_RECIEVED
		SIGNAL_RECIEVED = s
		OBJECT_RECIEVED = o



if __name__ == '__main__':
	unittest.main()