'''Small hacks for printing debugging messages.

Python has a built-in __debug__ flag. It is usually set to 'true.' It is false
when run as python -O. Running as python -O also disables assertions.

I'm trying to take advantage of this feature in all my code. This lets me:

    - Bulk up on assertions that sanity-check function arguments for proper
      type, etc.
    
    - Leave debugging messages in code and let the __debug__ flag turn them
      off.

Let's say you want to put some debugging statements in your code:

    from datagrok.misc.debug import debug, d_apply
    debug('This code is running in debug mode.')

When launched with python -O, this will print nothing.

If you wish to call a particular function only when debugging:

    assert myfunc()

'''
from __future__ import absolute_import

# TODO: I can't put doctests here because they will be wrong depending on the
# value of -O. Figure out a workaround.


if __debug__:
    import sys

    def debug(msg):
        print >> sys.stderr, msg

    def d_apply(fn, *args, **kw):
        debug('Calling: %s(%s, %s)' % (
            fn.__name__,
            ', '.join([repr(x) for x in args]),
            ', '.join(["%s=%s" % (k, repr(v)) for (k, v) in kw])))
        debug(fn(*args, **kw))

    def printcalls(fn):
        def _notify_fn(*args, **kw):
            debug('calling %s(%s, %s)' % (fn.__name__, repr(args), repr(kw)))
            return fn(*args, **kw)
        _notify_fn.__doc__ = fn.__doc__ + '\n\nThis function prints a note when called.'
        return _notify_fn

else:
    def debug(msg):
        pass

    def d_apply(fn, *args, **kw):
        pass

    def printcalls(fn):
        return fn


debug.__doc__ = (
    '''Prints msg to standard error only when python is launched without -O.
    ''')

d_apply.__doc__ = (
    '''Deprecated. Calls fn with any additional arguments as parameters, but
    only when python is launched without -O. Also prints a note stating that
    the call is taking place.

    n.b. I don't remember for what purpose I created this, but I now feel it is
    redundant; one may simply use assert blah() instead.

    ''')

printcalls.__doc__ = (
    '''A decorator that prints a note to standard error when its decorated
    function is called, but only when __debug__ is true.

    For a more robust solution, see 'trace' in the standard library.

    ''')
