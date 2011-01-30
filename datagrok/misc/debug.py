'''Small hacks for printing debugging messages.

Python has a built-in __debug__ flag. It is usually set to 'true.' It is false
when run as python -O. Running as python -O also disables assertions.

I'm trying to take advantage of this feature in all my code. This lets me:

    - Bulk up on assertions that sanity-check function arguments for proper
      type, etc.
    
    - Leave debugging messages in code and let the __debug__ flag turn them
      off.

Let's say you want to put some debugging statements in your code:

    from datagrok.misc.debug import d_print, d_apply
    d_print('This code is running in debug mode.')

When launched with python -O, this will print nothing.

If you wish to call a particular function only when debugging:

    assert myfunc()

'''
from __future__ import absolute_import

# TODO: I can't put doctests here because they will be wrong depending on the
# value of -O. Figure out a workaround.


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


d_print.__doc__ = (
    '''Prints msg to standard error only when python is launched without -O.
    ''')

d_apply.__doc__ = ( 
    '''Deprecated. Calls fn with any additional arguments as parameters, but
    only when python is launched without -O. Also prints a note stating that
    the call is taking place.

    n.b. I don't remember for what purpose I created this, but I now feel it is
    redundant; one may simply use assert blah() instead.

    ''')
