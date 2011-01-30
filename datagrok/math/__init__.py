'''Miscellaneous mathematics'''


def lin(p1, p2):
    """Return the linear function of the line intersecting two points.
    
    Example:
    >>> melt = (0, 32)
    >>> boil = (100, 212)
    >>> celsius_to_farenheit = lin(melt, boil)
    >>> celsius_to_farenheit(10)
    50
    """
    (x1,y1) = p1
    (x2,y2) = p2
    return lambda x: (x-x1)*(y2-y1)/(x2-x1)+y1


def ran(r1, r2):
    """Return the function mapping range r1 to range r2.

    Example:
    >>> cels_range = (0,100)
    >>> farn_range = (32,212)
    >>> celsius_to_farenheit = ran(cels_range, farn_range)
    >>> celsius_to_farenheit(10)
    50
    """
    return lin((r1[0],r2[0]),(r1[1],r2[1]))
