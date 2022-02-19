######################################################################
## visible code

import math
import pytest
import random
import string
import typing

######################################################################
## student code

def compose(f, g):
    return lambda x: f(g(x))


def factor_pairs(n: int):
    return [ (x, y) for x in range(0, n+1)
                    for y in range(0, n+1)
                    if x * y == n ]


def test_compose():
    assert compose(lambda x: x+1, lambda x: x+2)(0) == 3

def test_factor_pairs():
    assert factor_pairs(6) == [(1,6), (2,3), (3,2), (6,1)]