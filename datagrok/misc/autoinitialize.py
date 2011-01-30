'''A mixin that causes an object to automatically populate instance attributes
according to the keywords passed to its constructor.

    >>> class Foo(AutoInitialize):
    ...     pass
    ...
    >>> x = Foo(foo="bar", baz=2, quux=range(3))
    >>> x.foo
    'bar'
    >>> x.baz
    2
    >>> x.quux
    [0, 1, 2]

    >>> class Blah(AutoInitializeSlots):
    ...     __slots__=['a','b','c']
    ...
    >>> x = Blah()
    >>> x.a = 3
    >>> x.d = 3
    Traceback (most recent call last):
        ...
    AttributeError: 'Blah' object has no attribute 'd'
    >>> x = Blah(a=1)
    >>> x = Blah(b=2)
    >>> x = Blah(a=1, b=2, c=3)
    >>> x = Blah(1, 2, 3)
    >>> x.a
    1
    >>> x.c
    3
    >>> x = Blah(a=1, b=2, c=3, d=3)
    Traceback (most recent call last):
        ...
    TypeError: 'Blah' does not take 'd' as an argument.

'''

from __future__ import absolute_import
import sys


class AutoInitialize(object):
    def __init__(self, **kw):
        self.__dict__.update(locals())
        del self.self
        self.__dict__.update(kw)


class AutoInitializeSlots(object):
    __slots__=[]
    def __init__(self, *args, **kw):
        if len(args) > len(self.__slots__):
            raise TypeError, "%s takes exactly %s arguments" % (__name__, len(self.__slots__)), sys.exc_info()[2]
        for key, value in zip(self.__slots__, args):
            setattr(self, key, value)
        try:
            for key in kw:
                setattr(self, key, kw[key])
        except AttributeError:
            raise TypeError, "%s does not take %s as an argument." % (repr(self.__class__.__name__), repr(key)), sys.exc_info()[2]

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__,
                ', '.join(["%s=%s" % (k, getattr(self, k))\
                    for k in self.__slots__ \
                    if getattr(self, k, None)]))
