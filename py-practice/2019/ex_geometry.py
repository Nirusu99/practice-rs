######################################################################
## visible code

import math
import pytest
import random
import string
import typing

######################################################################
## student code

class Rect:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __eq__(self, other):
        return (type(other) == Rect and
                self.x1 == other.x1 and self.y1 == other.y1 and
                self.x2 == other.x2 and self.y2 == other.y2)


def merge(r1: Rect, r2: Rect) -> Rect:
    return Rect(
        min(r1.x1, r2.x1), min(r1.y1, r2.y1),
        max(r1.x2, r2.x2), max(r1.y2, r2.y2),
    )

def test_eq():
    assert Rect(2,2,4,8) == Rect(2,2,4,8)
    assert Rect(2,2,4,8) != Rect(2,2,4,7)

def test_merge():
    assert merge(Rect(2,2,4,8), Rect(5,5,6,6)) == Rect(2,2,6,8)