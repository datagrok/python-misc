"""Euclid's Algorithms

	>>> gcd(12, 18)
	6

	XXX FIXME Hmm, this does not actually work, revist.
	Calculating the inverse of an integer x, modulo y:
	>>> (x, y) = (12, 18)
	>>> (r, s, d) = euclid(x, y)
	>>> print "%d ^-1 (mod %d) = %d" % (x, y, r%y)
	12 ^-1 (mod 18) = 17
	>>> (x * (r%y)) % y == 1
	True

	>>> for x,y in [(12,18),(18,12),(12,6),(6,12),(18,30),(1234,4321)]:
	...		(r,s,d) = euclid(x,y)
	...		print "%dx + %dy = %d" % (r,s,d)
	... 
	-1x + 1y = 6
	1x + -1y = 6
	0x + 1y = 6
	1x + 0y = 6
	2x + -1y = 6
	-1082x + 309y = 1

"""
def gcd(x,y):
	"""Return the greatest common divisor of x and y"""
	return _euclid((1,0,x),(0,1,y))[2]

def euclid(x,y):
	"""Perform euclid's extended algorithm, to return
		rx + sy = d
	where d is the greatest common divisor of x and y."""
	return _euclid((1,0,x),(0,1,y))

def _euclid(u,v):
	#print u
	if u[2] == 0: return v
	if u[2] == 1: return u
	r = v[2]/u[2]
	return _euclid([x - r*y for x,y in zip(v,u)], u)

if __name__ == "__main__":
	import doctest; doctest.testmod()
