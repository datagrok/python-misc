"""Utilities for higher-order function composition.

Originally from _Text Processing in Python_, 'combinatorial.py'
by David Mertz
http://gnosis.cx/TPiP

"Combinatorial" functions as defined by Mertz take functions as arguments and
return compositions of functions.

Mertz's functions were originally written for Python 1.5. I've changed them a
bit to take advantage of features found in Python 2.3+, and have pulled in
similar tools from Python documentation.

The following have been removed:
    apply_each(fns, args) - use each(*fns)(*args) instead.
    bools - unneeded with builtins any() and all() instead.
    bool_each
    conjoin - use all() instead.
    both - use all() instead.
    all3 - use all() instead.
    and_ - use all() instead.
    disjoin - use any() instead.
    some - use any() instead.
    either - use any() instead.
    anyof3 - use any() instead.

"""
from __future__ import absolute_import
from functools import reduce

# TODO: explore 'functional' module as mentioned in Python docs; cull any
# duplicate functionality.

# combinatorial style for some builtins
def each(*fns):
    """Compose a list of functions into a single function that returns the list
    of results when its arguments are applied to every function.

    >>> many_increments = each(*[
    ... lambda x:x+1,
    ... lambda x:x+2,
    ... lambda x:x+3,
    ... ])
    >>> list(many_increments(4))
    [5, 6, 7]

    """
    return lambda *args: ((fn(*args) for fn in fns))


def any(*fns):
    """Return a function that returns True if any of fns are True when evaluated."""
    return lambda *args: __builtins__.any(each(fns)(*args))


def all(*fns):
    """Return a function that returns True if all of fns are True when evaluated."""
    return lambda *args: __builtins__.all(each(fns)(*args))

# Compose two functions.
_compose = lambda f, g: lambda *args: f(g(*args))

# The identity function.
def ident(x):
    """The identity function. ident(x) == x."""
    return x

# from http://mail.python.org/pipermail/python-list/2004-December/298060.html

def compose(*callables):
    """Compose a sequence of functions.
    
    compose(f,g,h)(x) == f(g(h(x)))

    >>> incrementer = lambda x: x+1
    >>> doubler = lambda x: x*2
    >>> compose(*[incrementer, doubler])(3)
    7
    
    """
    return reduce(_compose, callables, ident)


def pipeline(*callables):
    """Compose a sequence of functions in reverse order. Allows one to
    visualise the sequence as a pipeline, like when using the unix shell
    "pipe."
    
    pipeline(f,g,h)(x) == h(g(f(x)))
    (Think: "echo x | f | g | h")
    
    """
    callables = list(callables)
    callables.reverse()
    return compose(*callables)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
