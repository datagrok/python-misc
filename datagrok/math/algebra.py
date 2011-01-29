"""Utilities for MAT 313 Abstract Algebra"""

from euclid import gcd

def rprime(x,y):
	"""True if x is relatively prime to y
	>>> rprime(25,36)
	True
	>>> rprime(25,30)
	False
	"""
	return gcd(x,y) == 1

def U(n):
	"""The group of units of integers modulo n. This is
	U(n), all x in Z_n such that x relatively prime to
	n."""
	return [x for x in range(n) if rprime(x, n)]

def U_n_ord(n):
	"""List of tuples (x, n_x) of U(n) with the order of
	>>> U_n_ord(20)
	([1, 3, 7, 9, 11, 13, 17, 19], [1, 4, 4, 2, 2, 4, 4, 2])
	>>> U_n_ord(24)
	([1, 5, 7, 11, 13, 17, 19, 23], [1, 2, 2, 2, 2, 2, 2, 2])
	"""
	p = U(n)
	l = len(p)
	o = []
	for x in p:
		y = 1
		for e in range(l):
			y = y * x % n
			if y == 1:
				o.append(e+1)
				break
	return p, o
