"""Tools for working with iterators.

    Warning: this module overlaps the name of a built-in module. If you're a
    sensible and pragmatic developer who obeys the recommendations in the
    Python documentation, you may wish to rename this module before use.

Many of these have been taken from or inspired by the documentation for the
builtin itertools module. See http://docs.python.org/library/itertools.html

These have been removed:
    any(seq, pred=bool) - Unnecessary; use any((pred(x) for x in seq))
    iall(seq, pred=bool) - Unnecessary; use all((pred(x) for x in seq))
    no(seq, pred=bool) - Unnecessary; use not any((pred(x) for x in seq))

"""

from __future__ import absolute_import
from itertools import islice, imap, count
from operator import add
import collections

# For employing "yield" for a similar purpose as "print"
def withnewlines(iterable):
    """Convert each item in iterable to a string with newline"""
    return ('%s\n' % i for i in iterable)

def genfile(filename, iterable):
    """Write each item in iterable as a line to file specified by filename"""
    open(filename, 'w').writelines(withnewlines(iterable))

def accumulate(iterable, key_func=lambda x:x, op=add):
    '''Given an iterable, generate pairs of (running_total, item), where
    running_total accumulates (with oper.add) the items.

    If key_func is supplied, running_total instead accumulates the result of
    calling key_func with the current item passed as an argument.

    # get a running total along with the current item
    >>> list(accumulate(range(8)))
    [(0, 0), (1, 1), (3, 2), (6, 3), (10, 4), (15, 5), (21, 6), (28, 7)]

    # generate chunks of a string given chunk sizes
    >>> s = 'abcdefghijklmn'
    >>> chunksizes = [2,3,2,1,3]
    >>> [s[pos-l:pos] for pos, l in accumulate(chunksizes)]
    ['ab', 'cde', 'fg', 'h', 'ijk']

    '''
    total = None
    for i in iterable:
        if total is None:
            total = key_func(i)
        else:
            total = op(total, key_func(i))
        yield total, i

def periodically(iterable, callback, every=1, total=None):
    """Periodically call a callback function while iterating.

    Useful for e.g. displaying progress information.

    'callback' is called with arguments: current, total, item. 'current' is the
    current number of objects processed, 'total' is the total number to be
    processed, and 'item' is the item for that iteration through the loop. If
    'total' is unavailable it will be None.

    'every' is either an integer value of how often to call the callback, or a
    string value like '10%' that will call the callback every 10% of the way
    through the elements. If 'total' is None and an iterable with no __len__ is
    passed and 'every' is a percentage string, 'every' will fall back to '1'.

    If you don't know if your iterable will have a '__len__' and you can't pass
    a 'total' argument, you may instead provide a pair of callbacks as a tuple
    to the 'callback' argument: the first will be used if there is a total,
    the second otherwise. Example:

    >>> import sys
    >>> def log(s):
    ...    print s

    >>> callbacks=(
    ...     # Display a percentage when the total is available,
    ...     lambda c, t, i: log('%d%% complete' % (c*100/t)),
    ...     # Display the count if the total is unknown.
    ...     lambda c, t, i: log('%d items complete' % c))
    ...
    >>> for x in periodically(range(76543), callbacks, every=10000):
    ...     pass
    13% complete
    26% complete
    39% complete
    52% complete
    65% complete
    78% complete
    91% complete
    100% complete

    >>> for x in periodically(iter(xrange(76543)), callbacks, every=10000):
    ...     pass
    10000 items complete
    20000 items complete
    30000 items complete
    40000 items complete
    50000 items complete
    60000 items complete
    70000 items complete

    """
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            # This is an iterator without a __len__; leave total = None
            total = None

    if isinstance(callback, tuple):
        callback = callback[0 if total else 1]

    if isinstance(every, str) and every.endswith('%'):
        if total:
            every = int(float(every[:-1]) * total / 100)
        else:
            every = 1

    for n, item in enumerate(iterable, start=1):
        yield item
        if n % every == 0 or (total and n == total):
            callback(n, total, item)

# Verbatim from itertools docs. http://docs.python.org/library/itertools.html

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def tabulate(function, start=0):
    "Return function(0), function(1), ..."
    return imap(function, count(start))

def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

def quantify(iterable, pred=bool):
    "Count how many times the predicate is true"
    return sum(imap(pred, iterable))

def padnone(iterable):
    """Returns the sequence elements and then returns None indefinitely.

    Useful for emulating the behavior of the built-in map() function.
    """
    return chain(iterable, repeat(None))

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(tuple(iterable), n))

def dotproduct(vec1, vec2):
    return sum(imap(operator.mul, vec1, vec2))

def flatten(iterable_of_lists):
    '''Flatten one level of nesting.

    See datagrok.flatten for a recursive, featureful, efficient iterator
    flattener.

    '''
    return chain.from_iterable(iterable_of_lists)

def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.

    Example:  repeatfunc(random.random)
    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def unique_justseen(iterable, key=None):
    """List unique elements, preserving order. Remember only the element just
    seen.
    """
    # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
    # unique_justseen('ABBCcAD', str.lower) --> A B C A D
    return imap(next, imap(itemgetter(1), groupby(iterable, key)))

def iter_except(func, exception, first=None):
    """ Call a function repeatedly until an exception is raised.

    Converts a call-until-exception interface to an iterator interface.
    Like __builtin__.iter(func, sentinel) but uses an exception instead
    of a sentinel to end the loop.

    Examples:
        bsddbiter = iter_except(db.next, bsddb.error, db.first)
        heapiter = iter_except(functools.partial(heappop, h), IndexError)
        dictiter = iter_except(d.popitem, KeyError)
        dequeiter = iter_except(d.popleft, IndexError)
        queueiter = iter_except(q.get_nowait, Queue.Empty)
        setiter = iter_except(s.pop, KeyError)

    """
    try:
        if first is not None:
            yield first()
        while 1:
            yield func()
    except exception:
        pass

def random_product(*args, **kwds):
    "Random selection from itertools.product(*args, **kwds)"
    pools = map(tuple, args) * kwds.get('repeat', 1)
    return tuple(random.choice(pool) for pool in pools)

def random_permutation(iterable, r=None):
    "Random selection from itertools.permutations(iterable, r)"
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))

def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(xrange(n), r))
    return tuple(pool[i] for i in indices)

def random_combination_with_replacement(iterable, r):
    "Random selection from itertools.combinations_with_replacement(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.randrange(n) for i in xrange(r))
    return tuple(pool[i] for i in indices)



def window(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ... """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def tee(iterable):
    "Return two independent iterators from a single iterable"
    def gen(next, data={}, cnt=[0]):
        dpop = data.pop
        for i in count():
            if i == cnt[0]:
                item = data[i] = next()
                cnt[0] += 1
            else:
                item = dpop(i)
            yield item
    next = iter(iterable).next
    return (gen(next), gen(next))

