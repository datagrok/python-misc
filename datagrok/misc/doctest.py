'''Helpers for the standard library 'doctest' module.

    Warning: this module overlaps the name of a module in the Python standard
    library. If you're a sensible and pragmatic developer who obeys the
    recommendations in the Python documentation, you may wish to rename this
    module before use.

Sometimes I break the rules and give modules names that overlap those in the
standard library. (See datagrok.misc.pkgutil for more on that.)

When I do that, standard doctest when run like this will break:

    python -m doctest datagrok/misc/email.py

Because it adds datagrok/misc to sys.path and then imports 'email' for testing.
This occludes the standard library 'email' module.

I wish instead for nothing to be added to sys.path and for doctest to import
'datagrok.misc.email' and test that.

This module allows me to:

    # Test all packages and modules recursively discoverable from the current
    # directory.
    python -m datagrok.misc.doctest

'''
from __future__ import absolute_import
import doctest
import pkgutil

# TODO: enable the other use cases below:
'''
    # Test a module by filename
    python -m datagrok.misc.doctest datagrok/misc/email.py

    # Test many modules by filename
    python -m datagrok.misc.doctest datagrok/misc/*.py

    # Test a module by name
    python -m datagrok.misc.doctest datagrok.misc.email

    # Test all packages and modules recursively discoverable from a particular
    # directory.
    python -m datagrok.misc.doctest datagrok/misc

'''
def test_modules():
    '''Recursively searches for modules and packages starting in current
    directory, testing each.
    
    '''

    # TODO: pile all testable modules into a DocTestRunner instead of running
    # several (or only one) test. (Basically duplicate doctest.testmod() but
    # allow for an iterable of modules rather than just one.)

    #for module_loader, name, ispkg in pkgutil.walk_packages(['datagrok/misc'], prefix='datagrok.misc.'):
    for module_loader, name, ispkg in pkgutil.walk_packages(['.'], prefix=''):
        print name
        imploader = module_loader.find_module(name)
        m = imploader.load_module(name)
        failures, _ = doctest.testmod(m)
        if failures:
            print failures
            return 'Errors found in %s.' % repr(name)

if __name__ == '__main__':
    raise SystemExit(test_modules())
