
"""Helper for creating tools that employ a robust command-line interface.

TODO: interface to datagrok.ansicolor ?

"""

from __future__ import absolute_import
import os
import shutil

class CLIManager(object):
    """Captures the boilerplate involved in making a decent command-line
    interface for a multi-function script.
    
    Think about the interface to cvs, svn, git, etc.

    Example: 
        class MyApp(CLIManager):
            def cmd_who(self):
                "Tells who"
                pass
            def cmd_what(self)
                "Tells what"
                pass
            ...

        if __name__=='__main__':
            import sys
            # Create an instance with arg0
            App = MyApp(sys.argv.pop(0))
            # Call the instance with command line arguments
            App(*sys.argv)
            
    """
    def __init__(self, argv0):
        self.argv0 = os.path.basename(argv0)

    def __call__(self, *args):
        args = list(args)
        command = '_default'
        if len(args):
            command = args.pop(0)
        if command == '--help':
            command = 'help'
        getattr(self, 'cmd_%s' % command, self._cmd_not_found(command))(*args)
        if len(args) == 1 and command != 'help':
            print
            print "See '%s help' for more information." % self.argv0

    def _cmd_not_found(self, command):
        def error():
            print "%s: '%s' is not a known command. see '%s help'" % (self.argv0, command, self.argv0)
        return error

    def cmd_help(self, *args):
        """Prints the usage information for this program or a command"""
        if len(args) == 0:
            print "usage: %s COMMAND [ARGS]" % self.argv0
            print
            print "The most commonly used commands are:"
            for command in [x[len('cmd_'):] for x in dir(self) if x.startswith('cmd_') and not x.startswith('cmd__')]:
                print "     %-10s %s" % (command, getattr(self, 'cmd_' + command).__doc__.splitlines()[0])
            print
            print "See '%s help COMMAND' for more information on a specific command." % self.argv0
        else:
            command = list(args).pop(0)
            cmd = getattr(self, 'cmd_%s' % command, None)
            if cmd:
                print "usage: %s %s [ARGS]" % (self.argv0, command)
                print cmd.__doc__
            else:
                self._cmd_not_found(command)(self)
            
    cmd__default = cmd_help
    

