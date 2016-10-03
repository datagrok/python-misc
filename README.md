# Miscellaneous Python modules

This package collects several small scripts of mine that do not yet warrant their own independent code repository. See pydoc for purpose and use of each.

    datagrok                   
       .math                   Miscellaneous mathematics
          .algebra             Utilities for MAT 313 Abstract Algebra
          .collatz             The Collatz conjecture
          .euclid              Euclid's Algorithms
          .stats               Utilities for statistics
          .vector              Snippets from linear algebra class
       .misc                   Miscellaneous Python scripts and utilities
          .ansicolor           A quick hack for making ansi colored text on the terminal.
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
          .templates           Utilities for templating.
          .timestamps          Format python 9-tuples as common timestamp formats
          .tree                A hierarchical mapping container in a variety of flavors and toppings.
          .xml               * Utilities for working with XML.

# Workflow

I used to maintain a long-running 'dev' branch intended to house unfinished work.

That was a good learning exercise in git branching and [workflow][2], but it was tedious and unnecessary. No sane person is going to use something from a git clone of "datagrok.misc" in production.

So, the policy for branch `master` is now: beware, some of this stuff works great, some is broken out of the box, some doesn't even do what it claims.

If there's something here you really like, let me know, and I'll be motivated to ensure it actually works, document it, write better tests, move it into its own repository, package it, and release it on PyPI.

# TODO

- Better unit testing, or at least an automated testrunner so we know what the test coverage is, and what's probably not broken
- Find a way to automatically present pydocs nicely, and automatically. No, not Sphinx, I hate that mess. Explore [method used in dinoboff's github-tools][1].

# License

All of the code herein is copyright 2016 [Michael F. Lamb][] and released under the terms of the [GNU Affero General Public License, version 3][AGPL-3.0+] (or, at your option, any later version.)

[1]: http://dinoboff.github.com/github-tools/overview.html#documentation-hosting
[2]: http://www.kernel.org/pub/software/scm/git/docs/gitworkflows.html
[AGPL-3.0+]: http://www.gnu.org/licenses/agpl.html
[Michael F. Lamb]: http://datagrok.org
