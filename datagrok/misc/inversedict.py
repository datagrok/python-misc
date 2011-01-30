'''Invert dictionaries. (keys->values and values->keys)

    >>> d = {
    ...     'a': 1,
    ...     'b': 2,
    ...     'c': 3,
    ... }
    >>> di = inverseInjectiveDict(d)
    >>> di
    {1: 'a', 2: 'b', 3: 'c'}
    >>> all([di[d[x]] == x for x in d])
    True

This is a simple enough idea, however things get complex when one has a
dictionary that is not injective; that is one that maps multiple different keys
to the same value. What should occur when this dictionary is inverted?

    >>> d = {
    ...     'a': 1,
    ...     'b': 1,
    ... }

I've elected to handle this by merging multi-valued keys into a list:

    >>> di = inverseDict(d)
    >>> di
    {1: ['a', 'b']}

But with this, the f^-1(f(x)) == f(f^-1(x)) == x invariant that one expects of
an inversed relationship no longer holds true.

    >>> all([di[d[x]] == x for x in d])
    False

We also run into an issue when values are mutable and thus not suitable for use
as dictionary keys. I have not yet implemented a way to deal with this
gracefully.

'''

# TODO: instead of multiple functions, add a toggle argument (or even a
# injective dictionary detection heuristic) which will cause inverseDict to
# behave like inverseInjectiveDict.

# TODO: add an option which will allow inverseDict(inverseDict(x)) == x for all
# dicts x, even if x is nonInjective.

# TODO: determine an appropriate action or approach to inverting a dictionary
# that contains mutable values.

def inverseDict(d):
    '''Thinking of dict d as a function that maps a -> b, this function produces
    a new dict that maps b -> a.
    
    We deal with non-injective dicts by mapping multi-valued elements to a list
    of their inverses. All values will be lists even if they happen to have only
    one mapping.

    >>> d = {
    ...     'a': 1,
    ...     'b': 2,
    ...     'c': 3,
    ... }
    >>> inverseDict(d)
    {1: ['a'], 2: ['b'], 3: ['c']}

    '''
    d_ = {}
    for k, v in d.items():
        d_.setdefault(v, []).append(k)
    return d_

def inverseInjectiveDict(d):
    '''

    >>> d = {
    ...     'a': 1,
    ...     'b': 2,
    ...     'c': 3,
    ... }
    >>> inverseInjectiveDict(d)
    {1: 'a', 2: 'b', 3: 'c'}


    '''
    return dict([(v,k) for (k,v) in d.items()])
