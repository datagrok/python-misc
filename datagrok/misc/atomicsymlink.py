"""Change the destination of a symlink as an atomic operation."""

from __future__ import absolute_import
import os


def symlink(src, dst, tmp=None):
    """Create a symbolic link pointing to src named dst.
    
    This function does the same thing as os.symlink, except when dst is an
    existing symlink. In this case, the new symlink is created in a temporary
    location and rename()d onto dst. This has the effect of "switching" the
    symlink as an atomic operation. This prevents a race condition where the
    symlink does not exist for a small finite amount of time, when another
    process might attempt to access it. (E.g. consider hot-swapping a symlink
    configured as the DocumentRoot of a high-traffic website.)

    Note that CALLING this function is NOT an atomic operation. It does a
    couple stat()s, etc. It implies only that the manipulation of the symlink's
    destination happens without a window of time where the symlink might not
    exist.

    This code relies upon os.tempnam() which will complain on stdout about a
    security risk. We have essentially replaced a probable race condition which
    might be triggered by any benign process with an improbable one only likely
    to be triggered by an active local attacker. To make it shut up, specify
    your own transient filename to be used for the swap as the argument tmp.
    
    """
    if not os.path.islink(dst):
        return os.symlink(src, dst)
    if not tmp:
        tmp = os.tempnam(None, 'alns_')
    os.symlink(src, tmp)
    os.rename(tmp, dst)
