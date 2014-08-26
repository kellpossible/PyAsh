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


	def assign(self, s, o):
		global SIGNAL_RECIEVED
		global OBJECT_RECIEVED
		SIGNAL_RECIEVED = s
		OBJECT_RECIEVED = o



if __name__ == '__main__':
	unittest.main()