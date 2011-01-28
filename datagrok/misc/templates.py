"""Utilities for templating.

TemplateStringHelper is a wrapper object that adapts objects for use with
python's format strings and template strings, for doing simple template
replacement with simple data objects.

    >>> class example(object):
    ...     a_string = "foo"
    ...     another_string = "bar"
    ...     an_iterable = xrange(3)
    ...     def a_method(self):
    ...         return "baz"
    ...     def a_generator(self):
    ...         yield '<ul>'
    ...         for x in range(3):
    ...             yield '<li>%d</li>' % x
    ...         yield '</ul>'
    ...
    >>> o = example()
    >>> TSH = TemplateStringHelper

Various format string mapping syntaxes may be used. Examples:

- "Old-style" string formatting (my favorite, sadly deprecated):
  (see http://docs.python.org/library/stdtypes.html#string-formatting)

    >>> '%(a_string)s, %(another_string)s' % TSH(o)
    'foo, bar'

- "Template string" formatting:
  (see http://docs.python.org/library/string.html#template-strings)

    >>> from string import Template
    >>> Template('$a_string, $another_string').substitute(TSH(o))
    'foo, bar'

- "New-style" string formatting:
  (see http://docs.python.org/library/string.html#string-formatting)

    >>> '{a_string}, {another_string}'.format(**TSH(o))
    'foo, bar'
    >>> '{0[a_string]}, {0[another_string]}'.format(TSH(o))
    'foo, bar'

Note: the new-style string formatting is probably the least elegant to use with
this helper; on the other hand its syntax supports attribute access, so if
you're using it this helper may be completely unnecessary anyway:

    >>> # Note no TemplateStringHelper is used here.
    >>> '{0.a_string}, {0.another_string}'.format(o)
    'foo, bar'

If the format string references a callable, it will be called, except for
__class__.

    >>> '%(a_method)s, %(__class__)s' % TSH(o)
    "baz, <class '__main__.example'>"

If the format string references any iterable other than a string object, it
will be newline-joined. This enables the pattern of using 'yield' as one would
use 'print'.

    >>> print '%(an_iterable)s' % TSH(o)
    0
    1
    2
    >>> print '%(a_generator)s' % TSH(o)
    <ul>
    <li>0</li>
    <li>1</li>
    <li>2</li>
    </ul>

If the format string references a nonexistent key, an exception will be raised.

    >>> '%(nonexistent)s' % TSH(o)
    Traceback (most recent call last):
        ...
    AttributeError: 'nonexistent' is neither attribute nor key

As a convenience, if replace_missing is True, a nonexistent key will be
replaced by an "old-style" format string reference to that key like '%(key)s'.
This behaviour is not very intelligent; it will not work for anything other
than string (%s) replacements, field widths are discarded, and it won't do the
right thing with "new-style" template strings. (Though with template strings,
you can use .safe_substitute() to achieve the same.)

    >>> '%(nonexistent)s %(a_string)s' % TSH(o, replace_missing=True)
    '%(nonexistent)s foo'
    >>> print '%(nonexistent)2.8d' % TSH(o, replace_missing=True)
    Traceback (most recent call last):
        ...
    TypeError: %d format: a number is required, not str

If the object is a mapping type, the map is searched before the object's
attribute dictionary.

    >>> a_dict = {
    ...     'a string': 'here is a string from a_dict',
    ...     'a no-argument function': lambda: 'a string from a callable',
    ...     'a number': 3.14159,
    ...     'a callable line generator': lambda: ('line %d' % x for x in range(1,4)),
    ... }
    >>> print '''
    ... %(a string)s
    ... %(a no-argument function)s
    ... %(a number)s
    ... %(a number)d
    ... %(a number)2.1f
    ... %(a callable line generator)s
    ... %(__class__)s
    ... %(__len__)04x
    ... '''.strip() % TSH(a_dict)
    here is a string from a_dict
    a string from a callable
    3.14159
    3
    3.1
    line 1
    line 2
    line 3
    <type 'dict'>
    0004

If multiple objects are presented to the TemplateStringHelper, they are
searched in the order that they are presented.

    >>> b_dict = {
    ...     'a string': 'a string from second dict',
    ...     'another string': 'another string from second dict',
    ... }
    >>> print '''
    ... %(a string)s
    ... %(another string)s
    ... '''.strip() % TSH(a_dict, b_dict)
    here is a string from a_dict
    another string from second dict

"""

from collections import Mapping

class TemplateStringHelper(Mapping):
    """A wrapper object which provides dict-style access to some objects'
    attributes and methods.

    This is designed to wrap arbitrary objects to make them easy to use with
    Format strings and Template strings.

    See the module-level docstring for examples of use.

    """

    def __init__(self, *objects, **kw):
        """Wrap objects with a TemplateStringHelper.
        
        If replace_missing=True is given as a keyword argument, then any
        requests for missing keys will return '%(key)s'. Otherwise, KeyError
        will be raised.

        """
        self.obs = objects
        self.replace_missing = kw.get('replace_missing', False)

    def __len__(self):
        return len(iter(self))

    def __iter__(self):
        seen = set()
        for ob in self.obs:
            for k in getattr(ob, 'keys', lambda: [])() + dir(ob):
                if k not in seen:
                    seen.add(k)
                    yield k

    def __getitem__(self, key):
        if not self.obs:
            return AttributeError('%s has no source objects.' % repr(self))

        # __class__ is a callable that will instantiate an object; we don't
        # want that behavior. Special-case it to return str(__class__)
        if key == '__class__':
            return str(self.obs[0].__class__)

        # TODO: These two special cases are necessary to support new-style
        # format strings like "...".format(**TSH(ob1, ob2)). I'm not sure what
        # effect doing this has, or possible bugs that could arise.
        # Investigate.
        if key == '__doc__':
            return str(self.obs[0].__doc__)
        if key == '__weakref__':
            return str(self.obs[0].__weakref__)

        item = None

        for ob in self.obs:
            item = self.__getitem_ob(key, ob)
            if item is not None:
                break

        if item is None:
            if self.replace_missing:
                return '%%(%s)s' % key
            else:
                raise AttributeError('%s is neither attribute nor key' %
                                     repr(key))

        # Assume callables should be called.
        try:
            item = item()
        except TypeError:
            pass

        # Assume iterables are string generators; flatten.
        if not (isinstance(item, str) or isinstance(item, unicode)) and hasattr(item, '__iter__'):
            item = '\n'.join([str(i) for i in iter(item)])

        return item

    def __getitem_ob(self, key, ob):
        '''Helper for __getitem__. Attempts to retrieve value for key from ob,
        trying both subscript and attribute access.
        
        '''
        try:
            return ob[key]
        except (TypeError, KeyError):
            try:
                return getattr(ob, key)
            except:
                return None
