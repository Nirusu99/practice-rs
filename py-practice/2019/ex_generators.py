######################################################################
## visible code

import math
import pytest
import random
import string
import typing

######################################################################
## student code

def accumulate(xs: list):
    acc = 0
    for x in xs:
        acc += x
        yield acc


def char_range(start: str, end: str):
    for i in range(ord(start), ord(end) + 1):
        yield chr(i)


def partitions(xs: list):
    for i in range(0, len(xs)):
        yield (xs[i], xs[:i] + xs[i+1:])


def test_accumulate():
    assert list(accumulate([1,2,3,4])) == [1,3,6,10]

def test_char_range():
    assert list(char_range('a', 'd')) == ['a', 'b', 'c', 'd']

def test_partitions():
    assert list(partitions([1,2,3,4])) == [ (1, [2,3,4]), (2, [1,3,4]), (3, [1,2,4]), (4, [1,2,3]) ]
