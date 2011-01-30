'''Manages a unix-filesystem-like heiarchy of objects.

Backed by a string-keyed dict, so you may persist using anydbm (if using string
values) or shelve (for object values).

    >>> x = FSTree()

The key '' refers to the root node.

You can ask about the parents of non-existent nodes:

    >>> x.parent('a/b/c/d/e/f')
    'a/b/c/d/e'
    >>> list(x.parents('a/b/c/d/e/f'))
    ['', 'a', 'a/b', 'a/b/c', 'a/b/c/d', 'a/b/c/d/e', 'a/b/c/d/e/f']

Parent nodes are implicitly instantiated to None:

    >>> x['a/b/a'] = "one"
    >>> x['a/b/b'] = "two"
    >>> x['a/b/c'] = "three"
    >>> x
    FSTree({
        '':                  None,
        'a':                 None,
        'a/b':               None,
        'a/b/a':             'one',
        'a/b/b':             'two',
        'a/b/c':             'three',
    })
    >>> list(x.children(''))
    ['a']
    >>> list(x.children('a/b'))
    ['a/b/b', 'a/b/c', 'a/b/a']
    >>> list(x.children('a/b/c'))
    []

Deleting a node recursively deletes its children:

    >>> del x['a/b']
    >>> x
    FSTree({
        '':                  None,
        'a':                 None,
    })

We do not yet support the "special" directories '.' or '..':

    >>> list(x.parents('a/b/./c'))
    Traceback (most recent call last):
        ...
    ValueError: No support for special path component '.'

Leading, trailing, and gratuitous inner separators are normalized:

    >>> x['a'] = "blah"
    >>> x['a'] == x['/a']
    True
    >>> x['a'] == x['a/']
    True
    >>> x['a'] == x['/a/']
    True
    >>> print x.repr_tree()
    FSTree:
        '':                  None
        'a':                 'blah'

'''

class FSTree(object):

    def __init__(self, tree=None):
        if tree is not None:
            self.tree = tree
        else:
            self.tree = dict()

    def norm_path(self, path):
        if not isinstance(path, str):
            if not all(isinstance(x, str) for x in path):
                raise TypeError('Got path %s, expected <type \'str\'>' % type(path))
        is_valid = self._validate_path_component
        return '/'.join([x for x in path.split('/') if is_valid(x)])

    def _validate_path_component(self, s):
        if s in ['.', '..']:
            raise ValueError('No support for special path component %s' % repr(s))
        return s

    def __getitem__(self, path):
        path = self.norm_path(path)
        return self.tree[path]

    def __setitem__(self, path, node):
        path = self.norm_path(path)
        for par in self.parents(path):
            if par not in self.tree:
                self.tree[par] = None
        self.tree[path] = node

    def __delitem__(self, path):
        path = self.norm_path(path)
        for p in self.tree.keys():
            if p.startswith(path):
                del self.tree[p]

    def __contains__(self, path):
        path = self.norm_path(path)
        return path in self.tree

    def __iter__(self):
        return iter(self.tree)

    def repr_keylist(self):
        ks = self.tree.items()
        ks.sort(key=lambda x: x[0].split('/'))
        if not ks:
            return self.__class__.__name__ + '({})'
        return self.__class__.__name__ + '({\n' + '\n'.join(["    %-20s %s," % (repr(path)+':', repr(page)) for path, page in ks]) + '\n})'

    def repr_tree(self):
        ks = self.tree.items()
        ks.sort(key=lambda x: x[0].split('/'))
        if not ks:
            return self.__class__.__name__ + '({})'
        def pathrepr(path):
            path = path.split('/')
            return '  ' * (len(path)-1) + repr(path[-1]) + ':'
        tr = '\n'.join(["    %-20s %s" % (pathrepr(path), repr(page)) for path, page in ks])
        return self.__class__.__name__ + ':\n' + tr

    __repr__ = repr_keylist

    def children(self, path):
        '''Return an iterable of paths of children of the specified path.

        This is currently NOT efficient, order of O(n), scanning the entire
        tree on each call.'''
        path = self.norm_path(path)
        #XXX FIXME not efficient
        valid_child = lambda x: x.startswith(path) \
                and x != path \
                and '/' not in x[len(path)+1:]
        #return (k for k in self.tree if valid_child(k)) # Py 2.5
        for k in self.tree:
            if valid_child(k):
                yield k

    def children_items(self, path):
        '''Return an iterable of children (path, value) of the specified path.
        O(n).'''
        for c in self.children(path):
            yield (c, self.tree.get(c))

    def parent(self, path):
        '''Return the path of immediate parent of given path, neither of which
        need exist.'''
        path = self.norm_path(path)
        path = path.split('/')
        return '/'.join(path[:-1])

    def parents(self, path):
        '''Return an iterable of paths of parents up to and including the given
        path, none of which need exist.'''
        path = self.norm_path(path)
        path = [p for p in path.split('/') if p]
        for p in range(len(path)+1):
            yield '/'.join(path[:p])

    def parents_items(self, path):
        '''Return an iterable of parents (path, value) of the specified path.

        This may yield some ancestors successfully before raising an exception
        for a non-existent path.'''
        for p in self.parents(path):
            yield (p, self.tree.get(p))

    def siblings(self, path):
        return self.children(self.parent(path))


#if __name__ == "__main__":
    #import shelve
    #s = shelve.open('/home/mike/tmp/siteblah.shelf')
    #x = Site(s)
    #for line in file('/home/mike/doc/projects/website-content/list.txt'):
    #   d, t = line.split(None, 1)
    #   x[d] = t.strip()
    #s.close()
    #
    #s = shelve.open('/home/mike/tmp/siteblah.shelf')
    #print s
