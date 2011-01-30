"""Various syntax sugars for use with mapping types.

This module began as an exploration of a mapping type that was convenient to
use with old-style format strings, to enable this sort of use case:

    >>> x = FormatStringDict({
    ...     'a':lambda:'callable',
    ...     'b':lambda:lambda:(x for x in ['lambda', ' and ', 'generator']),
    ...     'c':3,
    ...     'd':[1,2,3],
    ...     'e':lambda:range(4),
    ...     })
    >>> x.att=(('a', 'structure'), ('here'))
    >>> y = '%(a)s %(b)s %(c)s %(d)s %(e)s %(f)s'
    >>> y = y % x
    >>> print y
    callable lambda and generator 3 123 0123 %(f)s
    >>> x['f'] = 'foo'
    >>> print x['f']
    foo
    >>> print x.f
    Traceback (most recent call last):
        ...
    AttributeError: 'FormatStringDict' object has no attribute 'f'
    >>> print y % x
    callable lambda and generator 3 123 0123 foo
    >>> print 'structure:', x.att
    structure: (('a', 'structure'), 'here')
    >>> x['att']
    '%(att)s'
    >>> 'format string: %(att)s' % x
    'format string: %(att)s'

See also templates.TemplateStringHelper for something that might be a better
solution: An object wrapper (not a mixin) that translates subscript access to
attribute access.

"""

from __future__ import absolute_import
from datagrok.misc.flatten import flatten
import sys

#__all__ = ['FormatStringDict', 'LazyDict', 'LazyFormatStringDict']

# TODO: This module doesn't work very well, and datagrok.misc.templates solves
# the problem just fine. Remove from master branch until all the bugs are out,
# then place resultant ValueFlattener and FormatStringDefaults mixins in
# datagrok.misc.templates and AttAccessSubscripts mixin elsewhere.

# TODO: many of these are stubs or various attempts to do the same thing.
# Revisit and figure out which work and which don't, or if this is even needed
# after templates.TemplateStringHelper, which seems to work great.

# XXX TODO collections.defaultdict might be able to improve on many of these

# TODO: rename this module, as 'closuredict' is an obscure term that Mertz used
# only to describe a dict with '%(key)s' defaults. Maybe move these into a
# custom 'collections' module.


class FormatStringDict(dict):
    """This is a dictionary whose values are strings only, by calling callable
    values and flattening iterable values. It's good for sloppy string
    replacement with lazy evaluation. Does not generate keyerrors, instead
    returns "%(key)s".

    David Mertz in _Text Processing in Python_ calls a dictionary that gives
    "%(key)s" as a default a "closure dict," because it enables "partial
    interpolation" of a format string.

    """
    def __init__(self, initial={}):
        dict.__init__(self, initial)
    def __getitem__(self, key):
        item = super(FormatStringDict, self).get(key, '%('+key+')s')
        return ''.join([str(x) for x in flatten(item)])


class AttDict(dict):
    """This dictionary checks the object's attribute dictionary before the
    dictionary itself.
    
    """
    def __getitem__(self, key):
        print "attdict.get"
        if key in dir(self):
            return self.__dict__[key]
        return super(AttDict, self).__getitem__(key)


class FormatStringAttDict(AttDict):
    """Implements features of AttDict and FormatStringDict
    
    """
    # XXX FIXME Figure out how to do this as a mixin class!
    def __getitem__(self, key):
        item = AttDict.get(self, key, '%('+key+')s')
        return ''.join([str(x) for x in flatten(item)])


class LazyDict(dict):
    """Another attribute-access dictionary based on Storage, from web.py

    A LazyDict object is like a dictionary except that `obj.foo` can be used in
    addition to `obj['foo']` to access its values.
    
    """
    def __getattr__(self, key):
        if self.has_key(key):
            return self[key]
        raise AttributeError, repr(key)
    def __setattr__(self, key, value):
        self[key] = value
    def __repr__(self):
        return '<' + self.__class__.__name__ + dict.__repr__(self) + '>'


class AttAccessMapping(object):
    """A mixin which provides an attribute-based view into a mapping type.

    """
    # TODO: move this into a module named 'collections', make it work with
    # py2.6 collections.
    pass
