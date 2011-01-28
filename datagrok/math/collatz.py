
"""The Collatz conjecture

Also known as the 3n + 1 conjecture. Conjecture that this
sequence always converges to 1 regardless of the input is a
currently unsolved (unproven) problem in mathematics.

See http://en.wikipedia.org/wiki/Collatz_conjecture

>>> list(collatz_seq(12))
[12, 6, 3, 10, 5, 16, 8, 4, 2, 1]

"""

def collatz(x):
	"""Return the next number in the Collatz sequence."""
	if (x % 2) == 0:
		return x/2
	else:
		return x*3+1


def collatz_seq(x):
	"""Return the Collatz sequence for x, iterating until 1
	is reached."""
	while x != 1:
		yield x
		x = collatz(x)
	yield x
