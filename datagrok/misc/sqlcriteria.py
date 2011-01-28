
'''An idea for a DSL implemented in Python for lazily constructing SQL queries.

    >>> e = CriteriaHaving()
    >>> print (e.kind == 'person') * (e.id > 100) * (e.id < 1000) * (e.color != 'blue')
    (((table_a.kind = 'person') and (table_a.id > 100)) and (table_a.id < 1000)) and (table_a.color != 'blue')

'''

# TODO: There are several very nice ORMs out there that may have solved this
# problem already. Investigate and cull if so.

class CriteriaHaving(object):
    def __getattr__(self, key):
        return Criteria('table_a.' + key)
    def __getitem__(self, key):
        return Criteria('table_b_%s' % key + '.value')

class Criteria(object):
    def __init__(self, key):
        self.key = key
        self.criteria = ''
    def __eq__(self, other):
        self.criteria = '%s = \'%s\'' % (self.key, other)
        return self
    def __ne__(self, other):
        self.criteria = '%s != \'%s\'' % (self.key, other)
        return self
    def __gt__(self, other):
        self.criteria = '%s > %s' % (self.key, other)
        return self
    def __lt__(self, other):
        self.criteria = '%s < %s' % (self.key, other)
        return self
    def __add__(self, other):
        self.criteria = '(%s) or (%s)' % (self.criteria, other.criteria)
        return self
    def __sub__(self, other):
        self.criteria = '(%s) and not (%s)' % (self.criteria, other.criteria)
        return self
    def __mul__(self, other):
        self.criteria = '(%s) and (%s)' % (self.criteria, other.criteria)
        return self
    def __str__(self):
        return self.criteria
