"""Miscellaneous Python scripts and utilities

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

"""
from __future__ import absolute_import

__author__ = 'Michael F. Lamb <mike@datagrok.org>'
__license__ = 'GNU AGPL v3'
__date__ = '2005-04-07 07:59:18 -0400'


def memoized(fn):
    """A memoizing decorator.
    
    Note: Python 3.2 includes a possibly more robust 'functools.lrucache'.

    """
    # TODO: create my own 'functools' and move this there?
    results = {}
    def _memoized_fn(*args):
        if args not in results:
            results[args] = fn(*args)
        return results[args]
    _memoized_fn.__doc__ = fn.__doc__.replace('Returns', 'A memoization of', 1)
    _memoized_fn.__memo__ = results
    return _memoized_fn

def hbar(pct, width=80, chars=[
        u'', u'\u258f', u'\u258e', u'\u258d', u'\u258c', u'\u258b', u'\u258a',
        u'\u2589', u'\u2588']):
    '''Returns a string of unicode "Block Elements" characters appropriate for
    drawing a single bar in a horizontal bar chart.
    '''
    nchars = pct * width
    remainder = nchars - int(nchars)
    return chars[8] * int(nchars) + chars[int(remainder*8)]
