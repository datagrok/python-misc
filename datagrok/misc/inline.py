#!/usr/bin/env python
# Encoding: iso8859-1

# inline.py 0.1
# Copyright 2004 Michael Lamb

# This code was derived from:
#   pytext 2.1
#   Copyright 1999-2001 Daniel Robbins
#   http://www-106.ibm.com/developerworks/linux/library/us-gentoo/
# and
#   pyhtml.py by José Fonseca
#   http://jrfonseca.dyndns.org/source.html

# Distributed under the GPL

"""In-line Python code processor

Allows one to embed Python code in otherwise plain-text documents like HTML.
Anything between the tokens:

    <?python
    ...
    ?>

Gets replaced by the standard output of the code within. The inline() function
takes an input and an optional output filehandle. Simple use:

    $ python inline.py < file_to_parse.pyhtml > output.html

or:

    open('output.html', 'w').write(inline(open('file_to_parse.pyhtml')).read())

"""
from __future__ import absolute_import
import sys
import StringIO

def inline(fpin, fpout=None, locals_={}):
    """Expands in-line python code in an otherwise textual document.
    
    fpin:
        input filehandle.
    fpout:
        output filehandle (defaults to a new StringIO object).
    locals:
        a locals dict passed to the code being executed.

    Returns fpout.

    """
    real_sys_stdout = sys.stdout
    if fpout is None:
        fpout = StringIO.StringIO()
    sys.stdout = fpout
    codeblock = []
    is_code = False
    for line_number, line in enumerate(fpin.readlines()):
        if line_number == 0 and line.startswith('#!'):
            continue
        if line.startswith("<?python"):
            is_code = True
            codeblock = []
        elif line.startswith("?>"):
            is_code = False
            exec("".join(codeblock), globals(), locals_)
        elif is_code:
            codeblock.append(line)
        else:
            fpout.write(line)
    sys.stdout = real_sys_stdout
    fpout.seek(0)
    return fpout

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stdout.write(inline(sys.stdin).read())
    else:
        for filename in sys.argv[1:]:
            try:
                sys.stdout.write(inline(open(filename)).read())
            except IOError:
                sys.stderr.write("Error opening %s.\n" % filename)
                raise
