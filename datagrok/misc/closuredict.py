
"""

FIXME: Why did I name this "closuredict" again?

A set of syntax sugar for interacting with mapping types.

See also templates.TemplateStringHelper for something that might be a better
solution.

"""

from __future__ import absolute_import
from datagrok.misc.flatten import flatten
import sys

#__all__ = ['FormatStringDict', 'LazyDict', 'LazyFormatStringDict']

# XXX TODO collections.defaultdict might be able to improve on many of these

class FormatStringDict(dict):
	"""This is a dictionary whose values are strings only, by calling callable
	values and flattening iterable values. It's good for sloppy string
	replacement with lazy evaluation. Does not generate keyerrors, instead
	returns "%(key)s".
	"""
	def __init__(self, initial={}):
		dict.__init__(self, initial)
	def __getitem__(self, key):
		item = super(FormatStringDict, self).get(key, '%('+key+')s')
		return ''.join([str(x) for x in flatten(item)])


class AttDict(dict):
	"""
	This dictionary checks the object's attribute dictionary before the
	dictionary itself.
	"""
	def __getitem__(self, key):
		print "attdict.get"
		if key in dir(self):
			return self.__dict__[key]
		return super(AttDict, self).__getitem__(key)


class FormatStringAttDict(AttDict):
	"""Implements features of AttDict and FormatStringDict"""
	# XXX FIXME Figure out how to do this as a mixin class!
	def __getitem__(self, key):
		print "formatstringattdict.get"
		item = AttDict.get(self, key, '%('+key+')s')
		return ''.join([str(x) for x in flatten(item)])


class LazyDict(dict):
	"""
	This is based off Storage, from web.py

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
	
	TODO: move this into a module named 'collections', make it work with py2.6
	collections.
	"""
	pass

def test():
	x = FormatStringAttDict({
		'a':lambda:"callable!",
		'b':lambda:lambda:"double lambda!",
		'c':3,
		'd':[1,2,3],
		'e':lambda:range(4),
		})
	x.att=(("a","structure"),("here"))
	y = "%(a)s %(b)s %(c)s %(d)s %(e)s %(f)s"
	y = y % x
	print y
	x['f'] = "wanker"
	print x['f']
	try:
		print x.f
	except:
		print "could not print x.f"
	print y % x
	print "structure:", x.att
	print "string:", x['att']
	print "format string: %(att)s" % x
	

if __name__=='__main__':
	test()
