######################################################################
## visible code

import math
import pytest
import random
import string
import typing

######################################################################
## student code

def to_snake(s: str) -> str:
    s2 = ""
    for c in s:
        if c.isupper():
            s2 += "_" + c.lower()
        else:
            s2 += c
    return s2


def to_camel(s: str) -> str:
    s2 = ""
    found_delim = False
    for c in s:
        if c == "_":
            found_delim = True
        elif found_delim:
            s2 += c.upper()
            found_delim = False
        else:
            s2 += c
    return s2


def test_to_snake():
    assert to_snake("fooBarBaz") == "foo_bar_baz"

def test_to_camel():
    assert to_camel("foo_bar_baz") == "fooBarBaz"