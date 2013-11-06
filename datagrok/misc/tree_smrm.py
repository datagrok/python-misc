import collections

class HierarchicalMapping(HierarchcalMappingMixin, dict):
    '''A HierarchicalMapping is a mapping whose keys form a tree-like
    hierarchy. Keys may have parent and child keys and there is always a single
    root key.

    The data format for keys depends on various mixins.
    
    '''
    pass

class PathTransformerMixin(HierarchicalMappingMixin):
    '''Abstract superclass for all mixins that perform some preliminary
    translation of paths used when accessing this HierarchicalMapping.
    
    '''
    def transform_path(self, path):
        return path

class HierarchicalMappingMixin(object):
    '''
    >>> class MyDict(HierarchicalMappingMixin, dict):
    ...     pass
    >>> x = MyDict()
    >>> list(x.ancestors(('a', 'b', 'c', 'd')))
    [(), ('a',), ('a', 'b'), ('a', 'b', 'c')]
    >>> list(x.ancestors('abcd'))
    ['', 'a', 'ab', 'abc']

    >>> class MyDict(SlashSeparatedMappingMixin, HierarchicalMappingMixin, dict):
    ...     pass
    >>> x = MyDict()
    >>> list(x.ancestors('/a/b/c/d/e/'))
    ['', 'a', 'a/b', 'a/b/c', 'a/b/c/d']


    '''

    def ancestors(self, path):
        return (path[:n] for n in range(len(path)))

class SlashSeparatedMappingMixin(PathTransformerMixin, HierarchicalMappingMixin, dict):
    '''

    >>> class MyDict(SlashSeparatedMappingMixin, HierarchicalMappingMixin, dict):
    ...     pass
    >>> x = MyDict()
    >>> x[('a', 'b')] = 'first'
    >>> x['/a/b/c'] = 'second'
    >>> x
    {('a', 'b'): 'first', ('a', 'b', 'c'): 'second'}
    >>> x['/a/b/']
    'first'
    '''

    def transform_path(self, path):
        path = super(SlashSeparatedMappingMixin, self).transform_path(path)
        if isinstance(path, (str, unicode)):
            path = tuple(path.strip('/').split('/'))
        return path

    def __getitem__(self, path):
        path = self.transform_path(path)
        return super(SlashSeparatedMappingMixin, self).__getitem__(path)

    def __setitem__(self, path, value):
        path = self.transform_path(path)
        return super(SlashSeparatedMappingMixin, self).__setitem__(path, value)

    def ancestors(self, path):
        path = self.transform_path(path)
        return ['/'.join(x) for x in super(SlashSeparatedMappingMixin, self).ancestors(path)]

class SubMappingResolverMixin(HierarchicalMappingMixin):
    '''This will cause failed lookups to also walk up the path looking for a
    mapping type that it can delegate the rest of the path to.
    
    >>> class MyMapping(\
                SlashSeparatedMappingMixin,\
                SubMappingResolverMixin,\
                HierarchicalMappingMixin,\
                dict):
    ...     pass
    >>> data = MyMapping()
    >>> subdata = MyMapping()
    >>> data['/a/b/c'] = subdata
    >>> subdata['/d/e/f'] = 'value'
    >>> data['/a/b/c/d/e/f/']
    'value'

    '''
    def __getitem__(self, path):
        supr = super(SubMappingResolverMixin, self)
        try:
            return supr.__getitem__(path)
        except KeyError, e:
            for ancestor in reversed(list(supr.ancestors(path))):
                try:
                    return supr.__getitem__(ancestor)[path[len(ancestor):]]
                except KeyError:
                    continue
            else:
                raise e
