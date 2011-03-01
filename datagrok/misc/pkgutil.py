'''Tools for working with python packages and modules.

    Warning: this module overlaps the name of a module in the Python standard
    library. If you're a sensible and pragmatic developer who obeys the
    recommendations in the Python documentation, you may wish to rename this
    module before use.

'''

from __future__ import absolute_import
import sys

class system_imports_only():
    '''Sometimes, I want to create packages or modules named something like
    'datagrok.misc.email' that complement the 'email' module in the Python
    standard library.

    Unfortunately, despite the 'one honking great idea' of namespaces, having a
    module that overlaps one from the standard library can still confuse
    Python in certain situations.

    The obvious, easy, practical solution, which is recommended by the python
    documentation, is to rename my own package to not conflict with the
    standard library. But that offends my sense of aesthetics. What good are
    namespaces if I still have to avoid naming conflicts?

    If you insist on eschewing the recommendation like I do, just:

        - Make sure that all sibling modules in the same package as your
          misbehaving module use 'from __future__ import absolute_import'
          
        - Also, if your current directory contains a misbehaving module, remove
          '' from sys.path.

        - Don't run 'python -m doctest path/to/filename.py'; instead run
          'python -m datagrok.misc.doctest path/to/filename.py'

    If you do those things you shouldn't need this class.

    This function allows me to work around the problem with a minimum of mess.
    Since this module is named pkgutil, which also conflicts with a package in
    the standard library, you can see a demonstration of this function in use
    in the source code of this module.

    It's still just a hack unsuitable for anything that is intended for
    packaging and distribution. It assumes that your stdlib-overlapping module
    does not live within /usr/lib as the python standard library does.
    
    '''

    # TODO: finish carefully diagnosing and testing example failure cases and
    # how this class solves them.

    '''
    Problem:

        Current directory contains 'A.py' and a module wants to 'import A' from
        the standard library.

    Problem:

        Standard library contains module 'A' and module 'B' that does 'import
        A'.  'email.py'
        imports 'smtplib'.
    '''

    def __enter__(self):
        self.private_lib_path = []
        while sys.path and not sys.path[0].startswith('/usr/lib'):
            self.private_lib_path.append(sys.path.pop(0))

    def __exit__(self, type, value, traceback):
        sys.path[:0] = self.private_lib_path


with system_imports_only():
    import pkgutil


def get_modules():
    '''In progress. A wrapper around pkgutil.walk_packages to find packages and
    modules and return their name and first line of docstring.
    
    '''
    for module_loader, name, ispkg in pkgutil.walk_packages(['.']):
        imploader = module_loader.find_module(name)
        try:
            doc = imploader.load_module(name).__doc__ or ''
            doc = doc.strip().splitlines() or ['']
            doc = doc[0]
        except (SyntaxError, ImportError) as ex:
            doc = 'Could not import: %s' % ex
        yield name, doc


def standard_library_names():
    with system_imports_only():
        for module_loader, name, ispkg in pkgutil.iter_modules():
            yield name
        # this is a builtin. How do I retrieve it and others programmatically?
        yield 'itertools'


def module_list():
    stdlibnames = list(standard_library_names())
    for name, doc in get_modules():
        name = name.split('.')
        basename = name.pop()
        conflict = basename in stdlibnames
        if name:
            basename = '.%s' % basename
        name = ''.join(['   ' for n in name]) + basename
        print '    %-25s%1s %s' % (name, conflict and '*' or ' ', doc)


if __name__=='__main__':
    module_list()
