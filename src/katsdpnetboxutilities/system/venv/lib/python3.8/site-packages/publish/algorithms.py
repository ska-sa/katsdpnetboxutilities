"This module implements some useful algorithms."

__author__ = "Anna Logg (anna@loggsystems.se)"
__date__ = "2008-11-02 -- 2008-11-02"
__copyright__ = "Copyright (C) 2008 Anna Logg"
__license__  = "GNU GPL version 3 or any later version"

import Levenshtein as levenshtein

def distance(s0, s1):
    "Compute the relative edit distance between the two strings."

    d  = float(levenshtein.distance(s0, s1))
    d /= max(len(s0), len(s1), 1)

    return d
