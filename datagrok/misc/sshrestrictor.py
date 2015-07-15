#!/usr/bin/python

"""Limit ssh users to a restricted set of commands.

OpenSSH's authorized_keys file supports a "command=" syntax that
overrides the command that a user is allowed to execute when connecting
using that key. This alone can be too restrictive for some uses, for
example if you want to enable some user to run a command with any
argument, or one of a limited set of commands.

This module is a helper that you may use to build dispatch scripts which
allow the user's command passed to ssh to be run if it matches one of a
set of valid patterns. When a match is found, the command is executed
using the absolute path to the executable you provide.

Installation: make a script that executes run() in this module, and
assign it as the target of the command="..." argument in
.ssh/authorized_keys, for the key to be restricted. See the docstring
for run() for its configuration format.

Example:

    in .ssh/sendmail_or_sleep.py:

        #!/usr/bin/python
        from datagrok.misc.sshrestrictor import run
        run([

            # User may call sendmail
            (r'(?:/usr/sbin/)?sendmail [a-zA-Z0-9. -]*$', '/usr/sbin/sendmail'),

            # Or just sleep a bit, useful for establishing tunnels.
            (r'(?:/bin/)?sleep \d?\d?\d$', '/bin/sleep'),

        ])

    in .ssh/authorized_keys:

        command="~/.ssh/sendmail_or_sleep.py" ssh-rsa AAAAB3za...LiPk== user@example.net

"""
from __future__ import absolute_import
import os
import re

__author__ = 'Michael F. Lamb <mike@datagrok.org>'
__date__ = 'Wed, 27 Feb 2008 03:12:54 -0400'

# TODO: support optional validation and/or re-writing of arguments
# instead of passing them directly to executable.

# TODO: unit tests, more examples.

def run(valid):
    """Match requested command against list of patterns, first to match
    is executed. Otherwise exit with nonzero status.

    valid is a list of (re, path) 2-tuples where:

        re is a compiled regular expression object (or any other object
        with a .match(string) method accepting one argument), or a
        regular expression string to be compiled into an expression.

        path is the full path to the acutal executable to be run.

    """

    try:
        cmd = os.environ['SSH_ORIGINAL_COMMAND']
    except KeyError:
        raise SystemExit("Permission denied for interactive shell.")

    for rx, c in valid_re:
        if isinstance(rx, basestring):
            rx = re.compile(rx)
        if rx.match(cmd):
            # TODO: support a mechanism for rewriting arguments
            # TODO: split() is not good enough; use shlex
            os.execvp(c, cmd.split())
            # os.execvp replaces this process with new; script essentially ends
            # here. Imagine a call to sys.exit().

    raise SystemExit("Permission denied for that command.")
