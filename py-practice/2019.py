from typing import Optional, Tuple
from dataclasses import dataclass


def to_snake(s: str) -> str:
    return "".join([c if c.islower() else '_' + c.lower() for c in s])


def test_snake():
    assert to_snake("myFancyFunction") == "my_fancy_function"

def to_camel(s: str) -> str:
    i = iter(s)
    sc = ""
    while (c := next(i, None)):
        if c == '_' and (c2 := next(i, None)) is not None:
            sc += c2.upper()
        else:
            sc += c
    return sc

def test_camel():
    assert to_camel("my_fancy_function") == "myFancyFunction"

def word_counts(s: str) -> dict[str, int]:
    d: dict[str, int] = {}
    for w in s.split():
        if w not in d:
            d[w] = 1
        else:
            d[w] += 1
    return d

def test_word_counts():
    assert sorted(word_counts("This sentence is a sentence")) == sorted({ "This": 1, "sentence": 2, "is": 1, "a": 1 })


def fizzbuzz(n: int) -> str:
    if n % 3 == 0:
        if n % 5 == 0:
            return "fizzbuzz"
        else:
            return "fizz"
    elif n % 5 == 0:
        return "buzz"
    else:
        return str(n)


def test_fizzbuzz():
    assert fizzbuzz(15) == "fizzbuzz"
    assert fizzbuzz(3) == "fizz"
    assert fizzbuzz(5) == "buzz"
    assert fizzbuzz(1) == "1"

def compose(f, g):
    return lambda x: f(g(x))

def test_compose():
    f = lambda x: x + 1
    g = lambda x: x * 2
    assert compose(f, g)(5) == 11

def factor_pairs(n: int) -> list[Tuple[int, int]]:
    return [(x, y)  for x in range(0, n + 1)
                    for y in range(0, n + 1)
                    if x * y == n]

def test_factor_pairs():
    assert sorted(factor_pairs(6)) == sorted([(1,6), (2,3), (3,2), (6,1)])


def accumulate(xs: list[int]):
    for (i, _) in enumerate(xs):
        yield sum(xs[:i + 1])

def test_acc():
    assert list(accumulate([1,2,3,4])) == [1, 1+2, 1+2+3, 1+2+3+4] == [1, 3, 6, 10]

def char_range(c0: str, c1: str) -> list[str]:
    return [chr(i) for i in range(ord(c0), ord(c1) + 1)]

def test_char():
    assert list(char_range('d', 'h')) == ['d', 'e', 'f', 'g', 'h']


def partitions(ls: list[int]):
    for (i, x) in enumerate(ls):
        yield (x, ls[:i] + ls[i + 1:])

def test_part():
    assert list(partitions([1,2,3,4])) == [ (1, [2,3,4]), (2, [1,3,4]), (3, [1,2,4]), (4, [1,2,3]) ]


@dataclass
class Rect:
    x1: int
    y1: int
    x2: int
    y2: int

    def __post_init__(self):
        assert self.x1 < self.x2
        assert self.y1 < self.y2

    def __eq__(self, other):
        return (self.x1 == other.x1
                and self.x2 == other.x2
                and self.y1 == other.y1
                and self.y2 == other.y2)

def merge(r1: Rect, r2: Rect) -> Rect:
    return Rect(min(r1.x1, r2.x1), min(r1.y1, r2.x1), max(r1.x2, r2.x2), max(r1.y2, r2.y2))

def test_merge():
    r1 = Rect(0, 0, 1, 1)
    r2 = Rect(1, 1, 2, 2)
    assert Rect(0, 0, 2, 2) == merge(r1, r2)

def test_eq():
    assert Rect(0, 0, 1, 1) == Rect(0, 0, 1, 1)

@dataclass
class Node:
    m: int
    l: Optional['Node']
    r: Optional['Node']

    def marks(self) -> list[int]:
        ls = [self.m]
        if self.l is not None:
            ls += self.l.marks()
        if self.r is not None:
            ls += self.r.marks()
        return ls

    def map(self, f):
        n = Node(f(self.m), None, None)
        if self.l is not None:
            n.l = self.l.map(f)
        if self.r is not None:
            n.r = self.r.map(f)
        return n

def test_map():
    n = Node(0, Node(1, Node(2, None, None), None), Node(3, None, None))
    assert n.map(lambda x: x + 1) ==  Node(1, Node(2, Node(3, None, None), None), Node(4, None, None))

def test_marks():
    n = Node(0, Node(1, Node(2, None, None), None), Node(3, None, None))
    assert n.map(lambda x: x + 1).marks() == [1, 2, 3, 4]






