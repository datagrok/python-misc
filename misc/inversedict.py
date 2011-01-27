def inverseDict(d):
    """Thinking of dict d as a function that maps a -> b, this function produces
    a new dict that maps b -> a.
    
    TODO: add a toggle argument which will restrict this function to operation
    on injective dicts, and maps to elements instead of single-valued lists of
    elements.

    We deal with non-injective dicts by mapping multi-valued elements to a list
    of their inverses. All values will be lists even if they happen to have only
    one mapping.

    TODO: add an option which will allow inverseDict(inverseDict(x)) == x for
    all dicts x, even if x is nonInjective.

    """
    d_ = {}
    for k, v in d.items():
        d_.setdefault(v, []).append(k)
    return d_

def inverseInjectiveDict(d):
	return dict([(v,k) for (k,v) in d.items()])
