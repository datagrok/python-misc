#!/usr/bin/python

"""A mapping type which presents a unioned view of multiple other mapping
objects.

"""

from UserDict import DictMixin

# TODO: templates.TemplateStringHelper does something similar, try to decouple.

# FIXME: Should this module perhaps should be renamed 'collections' for
# consistency with python2.6+ ?

# TODO: "Starting with Python version 2.6, it is recommended to use
# collections.MutableMapping instead of DictMixin."

class MappingUnion(DictMixin):
    """A mapping object which presents a unioned view of multiple other mapping
    objects.

    To oversimplify, one might say that a MappingUnion is to a sequence of
    dict-like objects what UnionFS is to a list of filesystems.

    I wrote this because I use mapping types to map paths to nodes for my
    website, and I have multiple flavors of services that I want to smush
    together. So, I have a dict mapping paths to content objects, a dict-like
    object mapping date-like paths to content retrieved from a database, etc.

    """

    dicts = []

    def __init__(self, d, *args):
        self.dicts = [d] + list(args)

    def __getitem__(self, k):
        for d in self.dicts:
            try:
                return d[k]
            except KeyError:
                continue
        raise KeyError()

    #def __setitem__(self, k, v):
    #   pass

    # optionally define for pop() and popitem()
    #def __delitem__():
    #   pass

    def keys(self):
        # XXX FIXME: This might not have stable order across multiple calls
        s = set()
        for d in self.dicts:
            s.update(d.keys())
        return s

    # optionally define for efficiency
    #def __contains__():
    #   ...

    # optionally define for efficiency
    #def __iter__():
    #   ...

    # optionally define for efficiency
    #def __iteritems__():
    #   ...
        

if __name__=='__main__':
    import pprint
    a = dict(zip(range(4), range(4)))
    b = dict(zip(range(8), "abcdefgh"))
    x = MappingUnion(a, b)
    pprint.pprint(x)
    assert x[3] == 3
    assert x[6] == 'g'
    assert 15 not in a
    x = MappingUnion({
        (): a,
        ('x',): b
        }.items())
