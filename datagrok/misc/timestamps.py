'''Format python 9-tuples as common timestamp formats'''

from __future__ import absolute_import
import time


def to_w3c(self, dts):
	'''Return ISO8601-formatted date (given python 9-tuple).'''
	return time.strftime("%Y-%m-%dT%H:%M:%S%Z", dts)


def to_rfc822(self, dts):
	'''Return RFC2822-formatted date (given python 9-tuple).'''
	return time.strftime("%a, %d %b %Y %H:%M:%S %Z", dts)


def to_msec(self, dts):
	'''Return milliseconds since the epoch (given python 9-tuple).
	Useful for interoperation with ECMAscript.'''
	return int(time.mktime(dts) * 1000)


def to_fuzzy_date(date, now=None):
    '''(stub. needs implementation.) Returns a short, user friendly string,
    given a python date (9-tuple)

    now - specifies a time to compare date to.
        3 days
        3 days

    Like:
        3 days ago
        About an hour ago
        This morning
        Last week
        Next week
        5 weeks from now
        6 years ago
        less than a minute

    '''

    # TODO: Implement. I have done this in Javascript, re-implement in python.
    # This idea is fairly popular; Explore techniques used by others.

    raise NotImplementedError
    return "Sometime"
