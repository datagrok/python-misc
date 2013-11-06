from datagrok.misc import memoized

@memoized
def lev(s1, s2):
    """Returns the levenshtein distance between strings s1 and s2."""
    #print s1, s2
    if not len(s1): return len(s2)
    if not len(s2): return len(s1)
    return min(
            lev(s1[:-1], s2) + 1,
            lev(s1, s2[:-1]) + 1,
            lev(s1[:-1], s2[:-1]) + (0 if s1[-1] == s2[-1] else 1)
            )

print lev.__doc__
print lev('kitten', 'sitting')
print lev('kitten', 'kitten')
print lev('', '')
print lev('confide', 'deceit')
print lev('CUNsperrICY', 'conspiracy')
