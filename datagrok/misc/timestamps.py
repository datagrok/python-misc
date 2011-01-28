from __future__ import absolute_import
import time

def to_w3c(self, dts):
	"""Return ISO8601-formatted date (given python 9-tuple)."""
	return time.strftime("%Y-%m-%dT%H:%M:%S%Z",dts)

def to_rfc822(self, dts):
	"""Return RFC2822-formatted date (given python 9-tuple)."""
	return time.strftime("%a, %d %b %Y %H:%M:%S %Z",dts)

def to_msec(self, dts):
	"""Return milliseconds since the epoch (given python 9-tuple).
	Useful for interoperation with ECMAscript."""
	return int(time.mktime(dts) * 1000)
