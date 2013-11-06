"""Hierarchical mapping containers with a variety of flavors and toppings.

I wrote this because I wanted a hierarchically-structured container for
arbitrary objects, like a filesystem tree, which could:

    - store an object at any branch or leaf
    - access values (not sub-trees or node objects) using keyword (mapping)
    access with a path description, like tree[path] = "my data"; print
    tree[path]
    - given any path, enumerate its ancestors, siblings, and children.

But, as is my habit when hobby-coding, every time I had to make an
implementation decision, I went for abstraction to support as many use cases as
possible rather than make a decision that might special-case the design. It got
a little crazy...

As this variety of container assumes content at any node, it is applicable to
the url structure for a website, where requests for branch nodes (directories)
may themselves contain a value (content). 

(To accomplish this with a filesystem, many webservers silently redirect
requests for branches (directories) to a special child of that branch, a leaf
node (file), usually named 'index.html'.

# Move to "design defenses"
Best way to simultaneously store children and value?
    valueWithDictAttribute({children})   # val = T.children[path].children[path]
    tupleOrNamedTuple(value, {children}) # val = T.children[path].children[path].children[path].value
    dictWithValueAttribute({children})   # val = T[path][path][path].value

    easy-access:

    T[[path, path, path]] = value

NestedDictionaryTree is a base class which employs a similar scheme to store
its content. GeneralTreeNode instead maintains a 'value' in addition to its
dict of children within each node object so there are no naming exceptions.)

.flatten() a dict-of-dicts to a tuple-keyed single dict for storage in a shelf?
Implement as a dict-of-dict-like view on a flat dict, to back by a shelf? (All
keys would need to be read into heiarchy...)

Keys form a heiarchy, and the heiarchy (not the store, not the values) defines
parent/child/siblings.

... But my objects still want to know about their place in the heiarchy. Best
way to maintain a reference?

    >>> root = H()
    >>> root.add('blah')
    H('blah')

Some of the questions that one runs into, and which I have attempted to account
for, include:

    - When we ask for a node with tree[path], do we receive a node object or a value?
    - What storage mechanism should be used to contain the values?
    - What if the user wants to persist the structure to disk?
    - Basic building blocks: which of these should we employ? Are there other
    designs? What are the advantages of each?
        - A dict of nested dicts
        - A flat dict whose keys are all absolute paths
        - A node class that contains a value and a list of child nodes
    - 

As this variety of tree assumes content at any path, it is applicable to the
url structure for a website, where requests for branch nodes (directories) may
themselves return content.

(To accomplish this with a filesystem, many webservers silently redirect
requests for branches (directories) to a special child leaf node (file),
usually named 'index.html'. NestedDictionaryTree is a base class which employs
a similar scheme to store its content, and tries to prevent you from accessing
that "index" node directly. GeneralTreeNode instead maintains a 'value' in
addition to its dict of children within each node object so there are no naming
exceptions.)

    - A multi-level dict may contain data in the leaves only.
    - Elementtree enforces string keys and string values.

With some inspiration from ElementTree, but slightly more general to support
trees of objects. I hope to eventually make this easily compatible with
ElementTree, so your datagrok.Tree instances may easily be dumped to XML.

I assume that the most typical use is to hold the root and map paths to values.
In a general-purpose tree, paths are specified using a list of path elements.
As a convenience, string-based paths may be specified with '/' separators, as
in the UNIX filesystem.

    >>> T = Tree()

Build up some empty branches to hold leaf nodes. If you employ AutoCreateMixin,
these steps are unnecessary.

    >>> T['/'] = None
    >>> T['/people'] = None
    >>> T['/people/students/'] = None
    >>> T['/grades'] = None
    >>> T['/grades/math'] = None

    >>> T['/people/students/1'] = 'alice'

Any instance of a class may be stored in a Tree.

    >>> class Person:
    ...     def __init__(self, name):
    ...         self.name = name
    ...     def __str__(self):
    ...         return self.name

    >>> T['/people/students/2'] = Person('bob') # object value
    >>> T['/grades/math/1'] = 98                # int value
    >>> T['/grades/math/2'] = 97.5              # float value
    >>> T['x'] = 5                  # Not a path -> access to children
    >>> T['////x'] == T['//x//']    # path normalization
    True
    >>> T[['','','x','']] == T[['','x','','','']] # path normalization

Attribute access returns not a sub-tree but a value, so we need a method
to access the sub-tree object

    >>> S = T.node(['grades'])
    >>> S['math/1'] == 98
    True
    >>> S['math/2'] == 97.5
    True

Path elements need not be strings unless you're using StringPathsOnlyMixin. The
semantics are same as dict keys: any immutable object is fine.

    >>> a = 1           # an integer
    >>> b = 1.          # a float
    >>> c = ('a', 'b')  # a tuple
    >>> T[[a]] = None
    >>> T[[a,b]] = None
    >>> T[[a,b,a]] = "Example 1"
    >>> T[[a,b,b]] = "Example 2"
    >>> T[[a,b,c]] = "Example 3"
    >>> T[a,b,c] == "Example 3" # only if tuple_paths_ok
"""
from __future__ import absolute_import
import collections

# Design defenses:
#
# Paths are list-based: normal dicts do not allow immutable keys so having
# lists as a key makes it obious that something special is going on. Can't use
# just any sequence, like tuples, because immutable sequences are themselves
# valid path elements.

class HierarchicalMapping(collections.MutableMapping):
    """The base class for all hierarchical containers. Users may expect these
    methods to exist; varying implementations should subclass this class.

    hm = HeirarchicalMappingSubclass
    
    # Value access (semantics for 'path' may vary.)

    hm[path] = "my arbitrary data"
    print hm[path]

    # Traversal

    hm[hm.parent(path)] = "this is stored in the parent"

    for p in hm.ancestors(path):
        print hm[p]

    for p in hm.children(path):
        print hm[p]
    
    for p in hm.siblings(path):
        print hm[p]

    """

    def ancestors(self, path):
        """Generate a sequence of paths to each ancestor of 'path', starting
        with the root.

        This function may operate by only manipulating 'path' data; it does not
        necessarily attempt to verify that 'path' exists in the structure.

        """
        raise NotImplementedError()

    def parent(self, path):
        """Return a path corresponding to the parent of the node at 'path'.
        
        This function may operate only by manipulating 'path'; it does not
        necessarily attempt to verify that 'path' exists in the structure.

        """
        raise NotImplementedError()

    def siblings(self, path):
        """Generate a sequence of paths to each sibling of 'path', including
        itself.

        This function requires 'path' to exist in the structure.

        """
        raise NotImplementedError()

    def children(self, path):
        """Generate a sequence of paths to each child of 'path'.

        This function requires 'path' to exist in the structure.

        """
        raise NotImplementedError()

    def descendants(self, path):
        """Generate a sequence of paths to every descendent of 'path'.

        This function requires 'path' to exist in the structure.

        """
        raise NotImplementedError()

    def walk(self, path=[], callback=None, depth=False):
        """Walk the nodes in a HierarchicalMapping in breadth-first-search
        order. 

        This is like os.walk() in that your callback can modify its arguments
        to control the walking and pruning of branches. If you just want to do
        something on every leaf, .descendants() might be what you want instead. 

        """
        raise NotImplementedError()

        # XXX TODO FIXME
        if not isinstance(tree, HierarchicalMapping):
            raise RuntimeWarning("%s expects HierarchicalMapping, not %s." % (__name__, tree.__class__))
        yield (tree, path)
        for path_component, node in tree.children.items():
            for t, p in walk(node, path + [path_component]):
                yield (t, p)



class SimpleNestedDictTree(dict):
    """

        >>> t = SimpleNestedDict()
        >>> t['']['foo']['bar'] = "blah"


    """
    def __init__(self, value=None, d=None):
        self.children = dict()
        self.value = value


def NodeBackedHeirarchicalMapping(HierarchicalMapping):
    """The base class of all Heirarchical mappings whose values are wrapped in
    Nodes that may be used to traverse the tree.

    Enables:

        >>> tree[['path','to','node']] = "foo"
        >>> tree.node(['path','to','node']).siblings
        >>> tree.node(['path','to','node']).ancestors
        >>> tree.node(['path','to','node']).parent
        >>> tree.node(['path','to','node']).children
        >>> tree.node(['path','to','node']).value


    """


class GeneralTreeNode(HierarchicalMapping):

    def __init__(self):
        self.children = dict()
        self.value = None

    def node(self, path):
        if not isinstance(path, list):
            raise AttributeError("Not a list of path components: %s" % path)
        if len(path) == 0:
            return self
        return self.children[path.pop(0)].node(path)

    def norm_path(self, path):
        if not isinstance(path, list):
            raise AttributeError("Not a list of path components: %s" % path)
        return path

    def __getitem__(self, path):
        path = self.norm_path(path)
        return self.node(path).value

    def __setitem__(self, path, value):
        path = self.norm_path(path)
        if len(path) == 0:
            self.value = value
            return
        parent = self.node(path[:-1])
        if path[-1] not in parent.children:
            parent.children[path[-1]] = self.__class__()
        parent.children[path[-1]].value = value

    def __delitem__(self, path):
        path = self.norm_path(path)
        del self.node(path[:-1]).children[path[-1]]

    def __str__(self):
        return "\n".join(
                ["/%s\t%s\t%s" % ('/'.join([str(x) for x in p]), t.value, t.__class__.__name__) for t, p in walk(self)])


class FdTree(object):

    # XXX Abandoned: if we don't try to get all abstract and just assume the
    # pathnames are strings, we can use a shelve to store the data. So let's
    # make an object specific for the task. Site?

    """Flat Dictionary Hierarchical Mapping

    This class implements a basic hierarchical container, using a dict for
    storage. It does little more than add a parent/child management layer atop
    a regular dict. Requesting a branch returns the data stored at that branch.

    It is expensive (and presently unimplemented) to request a sub-tree
    rooted at a particular branch.

    As with dict objects, keys must be immutable, but need not be strings.
    """

    def __init__(self, tree=None):
        self.tree = tree or dict()

    def norm_path(self, path):
        if not isinstance(path, tuple):
            raise AttributeError("Not a tuple of path components: %s" % path)
        return path

    def __getitem__(self, path):
        path = self.norm_path(path)
        return self.tree(path)

    def __setitem__(self, path, value):
        path = self.norm_path(path)
        self.tree[path] = value

    def __delitem__(self, path):
        path = self.norm_path(path)
        del self.node(path[:-1]).children[path[-1]]

    def is_branch(self, node):
        """True if the node contains children"""
        pass

    def children_keys(self, path):
        """Return an iterable of paths of children of the specified path."""
        pass

    def children_items(self, path):
        """Return an iterable of children (path, value) of the specified
        path. (Imagine a call to itervalues() filtered to children of
        path.)"""
        pass

    def parents_keys(self, path):
        """Return an iterable of paths of parents of the specified path."""
        path = self.norm_path(path)
        if path not in self.tree:
            raise KeyError()
            return self.context(path)

    def parents_items(self, path):
        """Return an iterable of children (path, value) of the specified
        path. (Imagine a call to itervalues() filtered to children of
        path.)"""


    @classmethod
    def context(self, path):
        """Return an iterable of path components up to and including given
        path.

        context(tuple("abcd"))
        """
        # return (path[:n] for n in range(len(path))) # py 2.5
        for n in range(len(path)):
            yield path[:n]


class NdloTree(object):
    """Nested Dictionary Leafs-Only Hierarchical Container

    This class implements a basic hierarchical container, using nested dicts
    for storage. Requesting a branch returns a new NdloTree object rooted at
    that branch.
    """
    # XXX FIXME unfinished

    def __init__(self, tree=None):
        self.tree = tree or dict()

    def is_branch(self, node):
        """True if the node is a dict containing the special index_node_key."""
        return isinstance(node, dict) and self.index_node_key in node

    def is_branch(self, node):
        return isinstance(node, dict)

    def children(self, path):
        """List the children of a particular path"""
        node = self[path]
        if self.is_branch(node):
            return node.keys()
        return []

    def norm_path(self, path):
        if not isinstance(path, list):
            raise AttributeError("Not a list of path components: %s" % path)
        return path

    def __getitem__(self, path):
        path = self.norm_path(path)
        node = self.tree
        for p in path:
            node = node[p]
        if self.is_branch(node):
            return self.__class__(node)
        return node

    def __setitem__(self, path, value):
        path = self.norm_path(path)
        node = self.tree
        for p in path[:-1]:
            node = node[p]
        if self.is_branch(node) and len(node) > 0:
            raise AttributeError("Path is a branch with children; delete children or path first.")
        if len(path) == 0:
            self.tree = value
        else:
            node[path[-1]] = value

    def __delitem__(self, path):
        path = self.norm_path(path)
        for p in path[:-1]:
            node = node[p]
        del node[path[-1]]

    def __str__(self):
        return "\n".join(
                ["/%s\t%s\t%s" % ('/'.join([str(x) for x in p]), t.value, t.__class__.__name__) for t, p in walk(self)])


class NestedDictionaryTree(object):
    """Nested Dictionary Hierarchical Container

    This class implements the basic hierarchical Container,
    but unlike GeneralTreeNode it does not instantiate a tree
    object for every node in the tree. Instead, it
    "manages" a structure of nested dicts, and relies upon
    a "special key" per dict to contain branch nodes'
    "value."
    """

    # XXX FIXME unfinished.

    def __init__(self, tree=None, index_node_key='index'):
        self.tree = tree or dict()
        self.index_node_key = index_node_key
        if self.index_node_key not in self.tree:
            self.tree[self.index_node_key] = None

    def is_branch(self, node):
        """True if the node is a dict containing the special index_node_key."""
        return isinstance(node, dict) and self.index_node_key in node

    def children(self, path):
        """List the children of a particular path"""
        node = self[path]
        if self.is_branch(node):
            return node.keys()
        return []

    def norm_path(self, path):
        if not isinstance(path, list):
            raise AttributeError("Not a list of path components: %s" % path)
        return path

    def __getitem__(self, path):
        path = self.norm_path(path)
        node = self.tree
        for p in path:
            node = node[p]
        if self.is_branch(node):
            return node[self.index_node_key]
        return node

    def __setitem__(self, path, value):
        path = self.norm_path(path)
        node = self.tree
        if len(path) == 0:
            node[self.index_node_key] = value
            return
        for p in path[:-1]:
            if not self.is_branch(node[p]):
                node[p] = { self.index_node_key: node[p] }
            node = node[p]
        for p in path[-1:]:
            if self.is_branch(node):
                node[p][self.index_node_key] = value
            else:
                node[p] = value

    def __delitem__(self, path):
        path = self.norm_path(path)
        del self.node(path[:-1]).children[path[-1]]

    def __str__(self):
        return "\n".join(
                ["/%s\t%s\t%s" % ('/'.join([str(x) for x in p]), t.value, t.__class__.__name__) for t, p in walk(self)])


class StringSplitMixin(object):
    """Allows keys to resemble UNIX-style '/'-separated
    filesystem path strings. Paths with empty elements are
    normalized so that T['///x//y/'] == T['/x/y'] ==
    T[['x','y']]. Special paths like '.' and '..' are not
    (yet) supported.

    Allows this sort of Tree usage:
    T[['a','b','c']] == T['a/b/c']

    If used together, this mixin should probably precede
    OneLevelMixin.
    """
    def norm_path(self, path):
        if isinstance(path, str):
            path = [x for x in path.split('/') if x]
        return super(StringSplitMixin, self).norm_path(path)


class TuplePathsMixin(object):
    """If path access is specified without double-brackets, the path is
    represented by a tuple instead. This causes the tree to correctly interpret
    this.

    If used together, this mixin must precede StringPathsOnlyMixin.

    If used together, this mixin should probably precede OneLevelMixin.

    T[['a','b','c']] == T[('a','b','c')] == T['a','b','c']
    """
    def norm_path(self, path):
        if isinstance(path, tuple):
            path = list(path)
        return super(TuplePathsMixin, self).norm_path(path)


class OneLevelMixin(object):
    """Causes a tree to assume that a non-list key is not
    necessarily an error but instead refers to one of the
    toplevel children.

    Enables this sort of Tree usage:
    T[['a']] == T['a']
    """
    def norm_path(self, path):
        if not isinstance(path, list):
            path = [path]
        return super(OneLevelMixin, self).norm_path(path)


class AutoCreateMixin(object):
    """Setting a value at a path whose parents have not yet
    been created normally throws an exception. This mixin
    populates all necessary parent nodes with None values. 

    Enables this sort of usage of a Tree:
    T[['a','b','c']] = "something"
    T[['a','b']] == None
    T[['a']] == None
    T[[]] == None
    """
    pass


class NodeAccessMixin(object):
    """Enables this sort of usage of a Tree:
    print T[['a','b','c']].value
    print T[['a','b','c']].children

    By default, tree access assumes you want the value
    stored at a particular path, not the handle of a
    sub-tree rooted there. This overrides that default and
    instead returns a Tree object. Use .value to access
    stored values there.
    """
    pass


class StringPathsOnlyMixin(object):
    """Causes an exception to be raised if any non-string
    is used as a path (key) component.

    Most filesystems' paths have no notion of type; they
    are effectively always strings. Unambiguous
    representation of this structure with a tree that
    differentiates between the keys int(1) and str(1) is
    problematic.

    T[['1']] == "Example"
    T[[1]] # Exception thrown here
    """
    def norm_path(self, path):
        for p in path:
            if not isinstance(p, str):
                raise KeyError("Invalid key, must be a string: %s" % repr(p))
        return super(StringPathsOnlyMixin, self).norm_path(path)


class Tree(StringSplitMixin, TuplePathsMixin, OneLevelMixin, GeneralTreeNode):
    """A fairly useful and convenient tree, formed by
    combining a GeneralTreeNode with a bunch of useful mixin
    classes.
    """
    pass


class StringPathsTree(StringSplitMixin, TuplePathsMixin, OneLevelMixin,
                      StringPathsOnlyMixin, GeneralTreeNode):
    """A fairly useful and convenient tree, formed by
    combining a GeneralTreeNode with a bunch of useful mixin
    classes.
    """
    pass


if __name__ == "__main__":
    T = Tree()
    T[[]]        = "Example 0 (/)"
    T[['a']]     = "Example 1 (/a)"
    T[[2]]       = "Example 2 (/2)"
    T[['a',1]]   = "Example 3 (/a/1)"
    T[[2,'b']] = "Example 4 (/2/b)"
    T['/a'] = "String Split Test"
    T['/a/b'] = "String Split Test"
    T['/a/b/c'] = "String Split Test"
    T['/////a//////b//////d/////////'] = "String Split Test"
    T['a','b','e'] = "Tuple Paths Test"
    T['d'] = "One Level Test"
    print T

    print T.node(['a'])
    #print T.node(['a']).value    == T.value(['a'])    == T[['a']]
    #print T.node(['a']).children == T.children(['a'])
    #print T.node(['a']).siblings == T.siblings(['a'])

    T[['a']] = "blah"
