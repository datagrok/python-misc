"""Snippets from linear algebra class"""

from numpy import dot, array, sqrt, matrix

# TODO: many of these may be part of numpy now. Check and cull

def proj(M,x):
    """
    >>> A = array([[1, 2], [2, 1]])
    >>> x = array([[1], [2]])
    >>> proj(A, x)
    matrix([[ 1.],
            [ 2.]])

    """
    # proj_w(x) = M(M^TM)^-1M^Tx
    M = matrix(M)
    return M * (M.T * M).I * M.T * x


def mat_array(s):
    """Returns an array created from a spaces-and-lines blob of data.
    
    >>> mat_array('''
    ...     1 2 3
    ...     4 5 6
    ...     7 8 9
    ... ''')
    array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]])

    """
    return array([[int(v) for v in row.strip().split()] for row in [l for l in s.splitlines() if l]])


def col_array(s):
    """Returns transpose of mat_array.
    
    >>> col_array('''
    ...     1 2 3
    ...     4 5 6
    ...     7 8 9
    ... ''')
    array([[1, 4, 7],
           [2, 5, 8],
           [3, 6, 9]])
    
    """
    return (mat_array(s)).T


def norm(x):
    """Returns the norm (length) of vector x
    
    >>> norm(array([3, 4]))
    5.0

    """
    return sqrt(sum(x*x))


def unit(x):
    """Returns a unit vector in the direction of vector x.
    
    >>> unit(array([9, 0]))
    array([ 1.,  0.])
    >>> unit(array([0, 9]))
    array([ 0.,  1.])
    >>> unit(array([9, 9]))
    array([ 0.70710678,  0.70710678])

    """
    return x/norm(x)


def lss(A, b):
    """Finds the least squares solution for Ax=b"""
    A = matrix(A)
    return (A.T * A).I * A.T * b
