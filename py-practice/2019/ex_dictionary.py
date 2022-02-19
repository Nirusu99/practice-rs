######################################################################
## visible code

import math
import pytest
import random
import string
import typing

######################################################################
## student code

def word_counts(s: str) -> dict:
    d = dict()
    for w in s.split():
        if w in d:
            d[w] += 1
        else:
            d[w] = 1
    return d

def test_word_counts():
    assert word_counts("foo bar foo baz") == {'foo': 2, 'bar': 1, 'baz': 1}
