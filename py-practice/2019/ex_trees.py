######################################################################
## visible code

import math
import pytest
import random
import string
import typing

######################################################################
## student code

class Tree:
    def __init__(self, mark, children: list):
        self.mark = mark
        self.children = children

    def marks(self) -> list:
        marks = [self.mark]
        for c in self.children:
            marks = marks + c.marks()
        return marks

    def map(self, f):
        return Tree(f(self.mark), [c.map(f) for c in self.children])

def test_marks():
    t = Tree(1, [
          Tree(2, [
              Tree(3, []),
              Tree(4, []),
          ]),
          Tree(5, []),
        ])
    assert t.marks() == [1,2,3,4,5]

def test_map():
    t = Tree(1, [
          Tree(2, [
              Tree(3, []),
              Tree(4, []),
          ]),
          Tree(5, []),
        ])
    t2 = t.map(lambda x: x * 2)
    assert t2.marks() == [2,4,6,8,10]