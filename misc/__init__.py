
'''Miscellaneous Python scripts and utilities

These are little code snippets I like to keep handy. Some are copied or
modified from other people or books, some are original by me.

They may be in various states of completion; some may be release quality, other
may be incomplete, even as little as unfinished stubs of ideas.

    Copyright 2010 Michael F. Lamb

    This program and the files distributed with it are free software: you
    can redistribute them and/or modify them under the terms of the GNU
    Affero General Public License as published by the Free Software
    Foundation, either version 3 of the License, or (at your option) any
    later version.

    These files are distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    Affero General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

Michael F. Lamb <mike@datagrok.org>
http://datagrok.org
'''

__author__ = 'Michael F. Lamb <mike@datagrok.org>'
__license__ = 'GNU AGPL v3'
__date__ = '2005-04-07 07:59:18 -0400'

def lin(p1, p2):
    """Return the linear function of the line intersecting two points.
    
    Example:
    >>> melt = (0, 32)
    >>> boil = (100, 212)
    >>> celsius_to_farenheit = lin(melt, boil)
    >>> celsius_to_farenheit(10)
    50
    """
    (x1,y1) = p1
    (x2,y2) = p2
    return lambda x: (x-x1)*(y2-y1)/(x2-x1)+y1


def ran(r1, r2):
    """Return the function mapping range r1 to range r2.

    Example:
    >>> cels_range = (0,100)
    >>> farn_range = (32,212)
    >>> celsius_to_farenheit = ran(cels_range, farn_range)
    >>> celsius_to_farenheit(10)
    50
    """
    return lin((r1[0],r2[0]),(r1[1],r2[1]))


def memoized(fn):
    """A memoizing decorator."""
    results = {}
    def _memoized_fn(*args):
        if args not in results:
            results[args] = fn(*args)
        return results[args]
    _memoized_fn.__doc__ = fn.__doc__.replace('Returns', 'A memoization of', 1)
    return _memoized_fn


def notifying(fn):
    """A decorator that prints a note when called."""
    import sys
    def _notify_fn(*args, **kw):
        print >>sys.stderr, 'calling %s(%s, %s)' % (fn.__name__, repr(args), repr(kw))
        return fn(*args, **kw)
    _notify_fn.__doc__ = fn.__doc__ + '\n\nThis function prints a note when called.'
    return _notify_fn


def pv(seq, length=None):
    """NEEDS IMPLEMENTATION
    
    Creates a status bar like 'pv' for the passed iterable. Assumes
    sys.stdout is attached to a terminal that can interpret escapes.
    
    If your iterable has no __len__ but you know its length, you can pass it as
    the second argument.

    total time [ rate ] [=====> ] pct% ETA time-remain

    """
    pass


def _test():
    import doctest, datagrok
    return doctest.testmod(datagrok)


if __name__ == "__main__":
    _test()
