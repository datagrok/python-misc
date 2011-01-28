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
			raise TypeError, "'%s()' does not take '%s' as an argument." % (self.__class__.__name__, key), sys.exc_info()[2]

	def __str__(self):
		return '%s(%s)' % (self.__class__.__name__,
				', '.join(["%s=%s" % (k, getattr(self, k))\
					for k in self.__slots__ \
					if getattr(self, k, None)]))

def test():
	class Blah(AutoInitSlots):
		__slots__=['a','b','c']
	
	try:
		x = Blah()
		x.r = 3
		print "fail"
	except:
		print "ok"

	x = Blah(a=1)
	x = Blah(b=2)
	x = Blah(a=1,b=2,c=3)
	try:
		x = Blah(a=1,b=2,c=3,d=3)
		print "fail"
	except:
		print "ok"

