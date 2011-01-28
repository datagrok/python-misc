"""Flatten an arbitrarily nested iterable structure down to a single iterable.

>>> list(flatten([1, 2, [3, 4, [5, 6], 7], 8]))
[1, 2, 3, 4, 5, 6, 7, 8]

>>> c = lambda: lambda: lambda: lambda: lambda: ["callable!", 1, 2, 3]
>>> Q = [1, c, 3]
>>> list(flatten(Q, {
...     ''.__class__:False,
...     u''.__class__:False,
...     (lambda: None).__class__:True
...     }))
[1, 'callable!', 1, 2, 3, 3]

>>> Q = [1, 2, [1, 2, 3, [2, 3, c, {3:4,4:5,5:6}, "foo", "bar"]]]
>>> list(flatten(Q))
[1, 2, 1, 2, 3, 2, 3, 'callable!', 1, 2, 3, 3, 4, 5, 'foo', 'bar']

The naive idea is pretty simple. But the code gets a bit hairy if we want to
throw in some features:

    - Laziness: iterate through the structure, don't pre-generate the whole
      thing.

    - Don't iterate through strings: strings are iterable by default. Since I'm using
      this to flatten a nested sequence of strings, I want to end up with a flat
      iterable of strings, not a flat iterable of characters.

    - Assume strings: Since I'm using this to flatten a nested sequence of
      strings, assume any non-iterable, non-callable objects encountered should
      have their __str__ method called.

    - Extra laziness: assume functions in the structure are like thunks; they
      should be called and will return more interable structure.

    - Control: Each feature above should be able to be disabled to support other
      use cases.

    - Speed.

So, I capture that messy complexity in this module. Most of the code is cribbed
from a message posted to the python-list:

    Author:  Francis Avila <francisgavila@yahoo.com>
    To:      python-list
    Date:    Sun Nov 2 03:59:56 EST 2003
    Subject: flatten() time trial mystery. (or, 101 ways to flatten a nested list using generators)

I'm using this flattener to accomplish something like the following: start with
a pile of functions that call around to each other, occasionally printing stuff.

    def page(title, content):
        print '<html>'
        print head(title)
        print body(content)
        print '</html>'

    def head(title):
        print '<head>'
        print '<title>%s</title>' % title
        print '</head>'

    def body(content):
        print '<body>'
        print '<p>%s</p>' % content
        print '</body>'

Now, I don't want to print, but instead return all that data. I think a nice way
to do that is to simply replace every print statement with a yield, making those
functions into generators. But, I don't want to sprinkle "for x in
subfunction(): yield x" every time I call a subfunction, so instead I want to
iterate (lazily) through the the resulting (lazily generated) tree-like
structure.

See datagrok.itertools for a function that writes out generated strings to
files, and other iterator-related tools.

Yes, I know a simpler way to go about this example would be to redefine
sys.stdout for the duration of the initial call, capturing the printed output to
a StringIO buffer or something. But for whatever reason, I don't want to do
that.

"""

from __future__ import absolute_import
from __future__ import generators

# __all__=['flatten']

def flatten_fastdictdef(iterable, get_iterbility=None):
    if get_iterbility is None:
        get_iterbility = {''.__class__:False, u''.__class__:False}
    try:
        iterbility = get_iterbility[iterable.__class__]
    except KeyError:
        t = iterable.__class__
        try:
            iterable = iter(iterable)
        except TypeError:
            iterbility = get_iterbility[t] = False
        else:
            iterbility = get_iterbility[t] = True

    if callable(iterbility):
        iterbility, iterable = iterbility(iterable)

    if not iterbility:
        yield iterable
    else:
        for elem in iterable:
            for subelem in flatten_fastdictdef(elem, get_iterbility):
                yield subelem

def flatten_fastdictdef_callfuncs(iterable, get_iterbility=None):
    """A modification of Francis Avila's
    flatten_fastdictdef() which also calls functions, for
    lazy expansion."""
    if get_iterbility is None:
        get_iterbility = {''.__class__:False, u''.__class__:False}
    while callable(iterable):
        iterable = iterable()
    try:
        iterbility = get_iterbility[iterable.__class__]
    except KeyError:
        t = iterable.__class__
        try:
            iterable = iter(iterable)
        except TypeError:
            iterbility = get_iterbility[t] = False
        else:
            iterbility = get_iterbility[t] = True

    if callable(iterbility):
        iterbility, iterable = iterbility(iterable)

    if not iterbility:
        yield iterable
    else:
        for elem in iterable:
            for subelem in flatten_fastdictdef_callfuncs(elem, get_iterbility):
                yield subelem

flatten = flatten_fastdictdef_callfuncs
