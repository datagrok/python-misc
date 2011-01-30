# Miscellaneous Python modules

This package collects several small scripts of mine that do not yet warrant their own independent code repository. See pydoc for purpose and use of each.

    datagrok        
       .math                   Miscellaneous mathematics
          .algebra             Utilities for MAT 313 Abstract Algebra
          .collatz             The Collatz conjecture
          .euclid              Euclid's Algorithms
          .stats               Utilities for statistics
          .vector              Snippets from Linear Algebra class
       .misc                   Miscellaneous Python scripts and utilities
          .ansicolor           A quick hack for making ansi colored text on the terminal.
          .atomicsymlink       Change the destination of a symlink as an atomic operation.
          .autoinitialize      A mixin that causes an object to automatically populate instance attributes
          .cli                 Helper for creating tools that employ a robust command-line interface.
          .closuredict         FIXME: Why did I name this "closuredict" again?
          .color               Object-oriented color manipulation
          .combinatorial       Utilities for higher-order function composition.
          .debug               Small hacks for printing debugging messages.
          .doctest           * Helpers for the standard library 'doctest' module.
          .dreamhostapi        A quick hack for using xmlrpclib to talk to the Dreamhost API.
          .easypickle          Manage a single pickled object.
          .email             * Utilities for e-mail related things.
          .flatten             Flatten an arbitrarily nested iterable structure down to a single iterable.
          .fstree              Manages a unix-filesystem-like heiarchy of objects. Backed by a string-keyed
          .inline              In-line Python code processor
          .inversedict         Invert dictionaries. (keys->values and values->keys)
          .itertools           Tools for working with iterators.
          .mappingunion        A mapping type which presents a unioned view of multiple other mapping
          .pandoc              Filter pandoc->html for use with e-mail clients like mutt.
          .pkgutil           * Tools for working with python packages and modules.
          .server              MultiviewsRequestHandler
          .sqlcriteria         An idea for a DSL implemented in Python for lazily constructing SQL queries.
          .sshrestrictor       A restricted environment to allow users to execute commands by way of ssh,
          .templates           Utilities for templating.
          .timestamps          Format python 9-tuples as common timestamp formats
          .tree                A hierarchical mapping container in a variety of flavors and toppings.
          .xml               * Utilities for working with XML.

# TODO

- **Create dev branch, remove broken scripts from master.** Various of these scripts are in an incomplete state, since prior to now they have lived in a mostly-private subversion repository (where branching and merging requires more thinking). Now that these are on GitHub and elsewhere, re-examine all scripts, and put only those that are working, pass tests, and might be useful to others in master branch; I'll keep my work-in-progress in a development branch.

	- Figure out the best workflow to manage this in git, and document. Does [gitworkflows(7)][2] apply here?

- Find a way to automatically present pydoc nicely. Explore [method used in dinoboff's github-tools][1].

[1]: http://dinoboff.github.com/github-tools/overview.html#documentation-hosting
[2]: http://www.kernel.org/pub/software/scm/git/docs/gitworkflows.html

### Directory layout

I keep my home directory in a git repository, and I like to structure my system thus:

	$HOME/
		lib/
			python/
				datagrok/
					__init__.py			Empty file
					misc -> ~/var/submodules/python-misc/datagrok/misc
					math -> ~/var/submodules/python-misc/datagrok/math
					site -> ~/var/submodules/datagrok-site/datagrok/site (a different project that I also keep in the 'datagrok' package)
					...
		var/
			submodules/
				python-misc/	A clone of this repository

I keep ~/lib/python in my $PYTHONPATH, so whenever I need a utility script I can say for example:

	from datagrok.misc import lin
	from datagrok.misc.templates import TemplateStringHelper
