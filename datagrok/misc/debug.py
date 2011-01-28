from __future__ import absolute_import

if __debug__:
	import sys

	def d_print(msg):
		print >> sys.stderr, msg

	def d_apply(fn, *args, **kw):
		d_print('Calling: %s(%s, %s)' % (
			fn.__name__,
			', '.join([repr(x) for x in args]),
			', '.join(["%s=%s" % (k, repr(v)) for (k, v) in kw])))
		d_print(fn(*args, **kw))

else:
	def d_print(msg):
		pass

	def d_apply(fn, *args, **kw):
		pass
