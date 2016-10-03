from datagrok.misc import memoized

@memoized
def lev(s1, s2):
    """Returns the levenshtein distance between strings s1 and s2."""
    if not len(s1): return len(s2)
    if not len(s2): return len(s1)
    return min(
            lev(s1[:-1], s2) + 1,
            lev(s1, s2[:-1]) + 1,
            lev(s1[:-1], s2[:-1]) + (0 if s1[-1] == s2[-1] else 1)
            )

if __name__ == "__main__":
    for s1, s2 in [
        ('kitten', 'sitting'),
        ('kitten', 'kitten'),
        ('', ''),
        ('confide', 'deceit'),
        ('CUNsperrICY', 'conspiracy'),
        ]
    print(lev(s1, s2))
