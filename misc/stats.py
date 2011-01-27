"""Utilities for statistics"""

def sorted(xs):
	"""Return a sorted copy of the list xs"""
	_xs = list(xs)
	_xs.sort()
	return _xs

def stemleaf(ns):
	"""Given a list of integers ns, print a stem-and-leaf display."""
	return _stemleaf(sorted(ns))

def dsd(ns):
	"""Given a list of integers ns, print a double-stem display."""
	return _dsd(sorted(ns))

def fsd(ns):
	"""Given a list of integers ns, print a five-stem display."""
	return _fsd(sorted(ns))

def _stemleaf(ns):
	"Given a sorted list of integers ns, print a stem-and-leaf display."
	for q in range(10*(min(ns)/10), 10*(max(ns)/10+1), 10):
		print "%d|%s" % (q/10, ''.join([str(x % 10) for x in ns if x<q+10 and x>=q]))

def _dsd(ns):
	"Given a sorted list of integers ns, print a double-stem display."
	for q in range(10*(min(ns)/10), 10*(max(ns)/10+1), 5):
		print "%d|%s" % (q/10, ''.join([str(x % 10) for x in ns if x<q+5 and x>=q]))

def _fsd(ns):
	"Given a sorted list of integers ns, print a five-stem display."
	for q in range(10*(min(ns)/10), 10*(max(ns)/10+1), 2):
		print "%d|%s" % (q/10, ''.join([str(x % 10) for x in ns if x<q+2 and x>=q]))

if __name__ == "__main__":
	import doctest; doctest.testmod()
