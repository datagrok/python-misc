# Miscellaneous Python modules

This package collects several small scripts that do not yet warrant their own
independent code repository. See pydoc for purpose and use of each.

### Directory layout

I keep my home directory in a git repository, and I like to structure my system thus:

	$HOME/
		lib/
			python/
				datagrok/
					misc -> ~/var/submodules/python-misc/misc
		var/
			submodules/
				python-misc/	A clone of this repository
					README.md
					misc/
						__init__.py

I keep ~/lib/python in my $PYTHONPATH, so whenever I need a utility script I can say for example:

	from datagrok.misc import lin
	from datagrok.misc.templates import TemplateStringHelper
