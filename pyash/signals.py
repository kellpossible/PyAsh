from types import FunctionType, LambdaType

class Signal(list):
    """Event subscription.

    A list of callable objects. Calling an instance of this will cause a
    call to each item in the list in ascending order by index.

    Example Usage:
    >>> def f(x):
    ...     print 'f(%s)' % x
    >>> def g(x):
    ...     print 'g(%s)' % x
    >>> e = Signal()
    >>> e()
    >>> e.append(f)
    >>> e(123)
    f(123)
    >>> e.remove(f)
    >>> e()
    >>> e += (f, g)
    >>> e(10)
    f(10)
    g(10)
    >>> del e[0]
    >>> e(2)
    g(2)

    """
    def __call__(self, obj):
        for l in self:
            l.receive(self, obj)

    def __repr__(self):
        return "Event({0})".format(list.__repr__(self))

class Listener(object):
    """a simple listener interface used to listen to a Signal"""
    def __init__(self, receive_method=None):
        """It's possible to override the recieve method by passing
        a lambda through the recieve_method variable"""
        if receive_method is not None:
            if receive_method.__class__ == LambdaType or recieve_method.__class__ == FunctionType:
                self.receive = receive_method

    def receive(self, signal, obj):
        """signal: the signal that triggered the event.
        object: the object passed on dispatch"""
        pass