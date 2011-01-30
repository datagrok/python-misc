'''Talk to the Dreamhost API with xmlrpclib.

This is a bit of a hack to work around some subtle conflicts between
Dreamhost's API and assumptions made by the xmlrpclib library. Specifically,
the Dreamhost API uses '-' in method names, which are invalid python method
names. (xmlrpclib translates python method names to method names.)

Dreamhost API: http://wiki.dreamhost.com/Application_programming_interface

'''
from __future__ import absolute_import
from xmlrpclib import ServerProxy, _Method
from uuid import uuid1
from os import environ
from datagrok.misc.debug import debug


class DreamHostMethod(_Method):

    def __init__(self, send, name):
        _Method.__init__(self, send, name)

    def __getattr__(self, name):
        return DreamHostMethod(self._Method__send, "%s-%s" % (self._Method__name, name))

    def __call__(self, **kw):
        return self._Method__send(self._Method__name, kw)


class DreamHostServerProxy(ServerProxy):

    dh_api_server = 'https://api.dreamhost.com/xmlrpc'

    def __init__(self, key, verbose=0):
        ServerProxy.__init__(self, uri=self.dh_api_server, verbose=verbose)
        self.dh_api_key = key

    def __getattr__(self, name):
        return DreamHostMethod(self.__request, name)

    def __request(self, name, params):
        if not params:
            params = {}

        params['key'] = self.dh_api_key
        params['uuid'] = str(uuid1())
        result = ServerProxy._ServerProxy__request(self, name, (params,))

        if result['result'] != 'success':
            raise ValueError("Server returned %(result)s: %(data)s" % result)

        return result['data']


def set_dynamic_ip(dh_api_key, hostname):
    '''Uses the Dreamhost API to configure a DNS A record that points to the
    user's IP address. Useful for setting up a "phone home" dns name.

    This script is intended to be executed on the Dreamhost server by a user
    manually connecting using SSH. This lets us find the IP address to use by
    examining the SSH_CLIENT environment variable.

    '''

    new_ip = environ['SSH_CLIENT'].split()[0]
    server = DreamHostServerProxy(dh_api_key)

    debug("Retrieving list of current domains...")

    for record in server.dns.list_records():

        if not (record['record'] == hostname and record['type'] == 'A'):
            continue

        if record['value'] == new_ip:
            debug("Old record for %(record)s found with IP %(value)s. No update needed." % record)
            raise SystemExit()
            debug("Old record for %(record)s found with IP %(value)s. Removing." % record)

        result = server.dns.remove_record(
            record=record['record'],
            type=record['type'],
            value=record['value'],
        )

    result = server.dns.add_record(
        comment='Dynamic DNS IP',
        record=hostname,
        type='A',
        value=new_ip,
    )

    if result != 'record_added':
        raise ValueError("There was a problem adding the record.")

    debug("Success")
