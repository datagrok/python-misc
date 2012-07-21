# Miscellaneous Python modules

This package collects several small scripts of mine that do not yet warrant their own independent code repository. See pydoc for purpose and use of each.

    datagrok                   
       .math                   Miscellaneous mathematics
          .collatz             The Collatz conjecture
          .stats               Utilities for statistics
          .vector              Snippets from linear algebra class
       .misc                   Miscellaneous Python scripts and utilities
          .atomicsymlink       Change the destination of a symlink as an atomic operation.
          .autoinitialize      Mixin that auto-populates instance attributes.
          .cli                 Framework for creating tools that employ a robust command-line interface.
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
          .xml               * Utilities for working with XML.

# Workflow

This started out as a private branchless repository of a mixture of in-development, broken, buggy, and stub code and polished well-tested, frequently-used code.

I'm employing git branches now to try to separate the stuff that should be useful to the public from the ideas and buggy sketches. I'm still a bit green with git so I'm documenting what I *hope* is a good workflow here.

Branches:

- `master`: few bugs, tests pass.
- `dev`: includes buggy, unfinished, and stub modules.

As of today, `master` still contains some buggy code. To clean up:

    git checkout master
    git rm -f buggyfile
    git commit
    git checkout dev
    git merge -s ours --no-commit master
    git diff
    git commit

Bugfixing should occur in a topic branch from master (or directly in master if I'm lazy and cavalier) wherever possible. Then merge topic to master, then master to dev.

    git checkout master
    git branch -d bugfix
    git checkout -b bugfix
    (fix bugs)
    git commit
    git checkout master
    git merge bugfix
    git checkout dev
    git merge master

When a new module or feature from dev becomes stable, cherry-pick or patch it into an integration branch from master, then merge to master, then merge master to dev.

    git checkout master
    git checkout -b integration
    git cherry-pick 

# TODO

- Find a way to automatically present pydoc nicely, and automatically. Explore [method used in dinoboff's github-tools][1].

[1]: http://dinoboff.github.com/github-tools/overview.html#documentation-hosting
[2]: http://www.kernel.org/pub/software/scm/git/docs/gitworkflows.html
