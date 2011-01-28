# Miscellaneous Python modules

This package collects several small scripts of mine that do not yet warrant their own independent code repository. See pydoc for purpose and use of each.

# TODO

- **Create dev branch, remove broken scripts from master.** Various of these scripts are in an incomplete state, since prior to now they have lived in a mostly-private subversion repository (where branching and merging requires more thinking). Now that these are on GitHub and elsewhere, re-examine all scripts, and put only those that are working, pass tests, and might be useful to others in master branch; I'll keep my work-in-progress in a development branch.

- Find a way to automatically present pydoc nicely. Explore [method used in dinoboff's github-tools][1].

[1]: http://dinoboff.github.com/github-tools/overview.html#documentation-hosting

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
