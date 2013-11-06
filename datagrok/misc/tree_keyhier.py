'''Idea: keys are a particular subclass with parent/child/sibling
relationships; values are a simple dict mapping keys to values.

Special mapping objects are provided to make interaction with the mapping more
straightforward, hiding instantiation of PathNodes from the user.

'''

class PathNode(object):
    '''Abstract superclass of all PathNodes.'''

    def __init__(self):
        self.parent = None # Default = root
        self.children = []

    @property
    def siblings(self):
        if parent:
            return parent.children
        return []

    @property
    def path(self):
        '''The sequence of all nodes in the hierarchy from the root to this
        node.
        
        '''
        for a in self.parent.path:
            yield a
        yield self

class PathNodeHeirarchicalContainer(dict):

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass
