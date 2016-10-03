# Miscellaneous Python modules

This package collects several small scripts of mine that do not yet warrant their own independent code repository. See pydoc for purpose and use of each.

Beware, some of this stuff works great, some is broken out of the box, some doesn't even do what it claims. Much of this is quite old, so may work only with Python 2, may be completely supplanted by pypi packages or even the standard library.

If there's something here you really like, let me know, and I'll be motivated to ensure it actually works, document it, write better tests, move it into its own repository, package it, and release it on PyPI.

       .django               * Miscellaneous utilities for the Django framework.
          .markdown_tag        Markdown template tag for Django.
          .middleware          Middleware for Django.
             .stfuat           Middleware hack to silence missing variable debug messages.
       .math                   Miscellaneous mathematics
          .algebra             Utilities for MAT 313 Abstract Algebra
          .collatz             The Collatz conjecture
          .euclid              Euclid's Algorithms
          .stats               Utilities for statistics
          .vector              Snippets from linear algebra class
       .misc                   Miscellaneous Python scripts and utilities
          .ansicolor           Making ANSI-format colored text for the terminal.
          .atomicsymlink       Change the destination of a symlink as an atomic operation.
          .autoinitialize      Mixin that auto-populates instance attributes.
          .cli                 Framework for creating tools that employ a robust command-line interface.
          .closuredict         Various syntax sugars for use with mapping types.
          .color               Object-oriented color manipulation
          .combinatorial       Utilities for higher-order function composition.
          .debug               Small hacks for printing debugging messages.
          .doctest           * Helpers for the standard library 'doctest' module.
          .dreamhostapi        Talk to the Dreamhost API with xmlrpclib.
          .email             * Utilities for e-mail related things.
          .flatten             Flatten an arbitrarily nested iterable structure down to a single iterable.
          .fstree              Manages a unix-filesystem-like heiarchy of objects.
          .health              Various utilities for health and fitness.
          .inline              In-line Python code processor
          .inversedict         Invert dictionaries. (keys->values and values->keys)
          .itertools         * Tools for working with iterators.
          .mappingunion        A unioned view of multiple wrapped mapping objects.
          .pandoc              Filter pandoc->html for use with e-mail clients like mutt.
          .pkgutil           * Tools for working with python packages and modules.
          .server              A Python webserver that loosely emulates Apache's Multiviews
          .sqlcriteria         An idea for a Python DSL for lazily constructing SQL queries.
          .sshrestrictor       Limit ssh users to a restricted set of commands.
          .timestamps          Format python 9-tuples as common timestamp formats
          .tree                Hierarchical mapping containers with a variety of flavors and toppings.
          .tree_keyhier        Idea: keys are a particular subclass with parent/child/sibling
          .tree_smrm           'SubMappingResolverMixin' and more mapping container experiments.
          .xml               * Utilities for working with XML.

    \* = conflicts with a name in the standard library; see datagrok.misc.pkgutil for discussion

# TODO

- Better unit testing, or at least an automated testrunner so we know what the test coverage is, and what's probably not broken
- Find a way to automatically present pydocs nicely, and automatically. Not Sphinx.

# License

All of the code herein is copyright 2016 [Michael F. Lamb][] and released under the terms of the [GNU Affero General Public License, version 3][AGPL-3.0+] (or, at your option, any later version.)

[AGPL-3.0+]: http://www.gnu.org/licenses/agpl.html
[Michael F. Lamb]: http://datagrok.org
