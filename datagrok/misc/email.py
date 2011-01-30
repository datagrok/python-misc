'''Utilities for e-mail related things.

    Warning: this module overlaps the name of a module in the Python standard
    library. If you're a sensible and pragmatic developer who obeys the
    recommendations in the Python documentation, you may wish to rename this
    module before use.

'''
from __future__ import absolute_import
from smtplib import SMTP
from os import system

class TunneledSMTP(SMTP):
    '''An SMTP client (like smtplib.SMTP) that opens and employs an SSH tunnel
    to the mailserver by way of another server. The local port for the tunnel
    is always localhost:2525.

    '''

    def __init__(self, tunnelhost, host='', port=0, local_hostname=None):
        '''Initialize a new instance.

        tunnelhost:
            The server to SSH through. SSH must be configured for passwordless
            login to this server.
        host:
            The remote mailserver.
        port:
            The port on the mailserver, default: smtplib.SMTP_PORT.
        local_hostname:
            The FQDN of the local host, default: socket.getfqdn().

        An SMTPConnectError is raised if the specified mail host doesn't
        respond correctly.

        '''
        self.tunnelhost = tunnelhost
        SMTP.__init__(self, host=host, port=port,
                              local_hostname=local_hostname)

    def connect(self, host, port):
        '''Connect to a mail host on a given port, by tunneling through the SSH
        server configured on instantiation.

        If the hostname ends with a colon (`:') followed by a number, and
        there is no port specified, that suffix will be stripped off and the
        number interpreted as the port number to use.

        Note: This method is automatically invoked by __init__, if a mailhost
        is specified during instantiation.

        '''
        # Taken from smtplib.py and modified.
        if not port and (host.find(':') == host.rfind(':')):
            i = host.rfind(':')
            if i >= 0:
                host, port = host[:i], host[i+1:]
                try: port = int(port)
                except ValueError:
                    raise socket.error, "nonnumeric port"
        if not port: port = self.default_port

        system('ssh -f -L2525:%s:%d %s "sleep 4"' % (host, port, self.tunnelhost))
        return SMTP.connect(self, 'localhost', 2525)
