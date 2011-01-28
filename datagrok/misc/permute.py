def all_perms(str):
	"""Generates all permutations of (immutable) sequence str.
	From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252178

	>>> list(all_perms("abc"))
	['abc', 'bac', 'bca', 'acb', 'cab', 'cba']
	"""
	if len(str) <=1:
		yield str
	else:
		for perm in all_perms(str[1:]):
			for i in range(len(perm)+1):
				yield perm[:i] + str[0:1] + perm[i:]
