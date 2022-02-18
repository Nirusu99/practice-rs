from dataclasses import dataclass
from typing import Optional
import math


def is_prime(n: int) -> bool:
    if n == 2:
        return True
    elif n < 2 or n % 2 == 0:
        return False
    else:
        x = math.floor(math.sqrt(n)) + 1
        i = 3
        while i < x:
            if n % i == 0:
                return False
            i += 2
        return True


def test_two():
    assert is_prime(2)


def test_not_two():
    assert not is_prime(1)


def test_prime():
    assert is_prime(31)


def test_not_prime():
    assert not is_prime(35)


@dataclass
class Node:
    mark: str
    left: Optional['Node']
    right: Optional['Node']


def find_substrings(node: Node, substr: str) -> list[str]:
    subs: list[str] = []
    if substr in node.mark:
        subs.append(node.mark)
    if type(node.left) is Node:
        subs += find_substrings(node.left, substr)
    if type(node.right) is Node:
        subs += find_substrings(node.right, substr)
    return subs


def test_subs():
    tree = Node("aab", Node("baa", None, None), Node("aba", None, None))
    assert find_substrings(tree, 'ab') == ['aab', 'aba']


def my_enumerate(s: str):
    for (i, c) in enumerate(s):
        yield (i, c)


def prefixes(ls: list[int]):
    ls_n: list[int] = []
    yield ls_n
    for i in ls:
        yield (ls_n := ls_n + [i])


def alternate(xs, ys):
    while [x := next(xs, None), y := next(ys, None)] != [None, None]:
        if x is not None:
            yield x
        if y is not None:
            yield y


def test_enu():
    assert list(my_enumerate("abcd")) == [(0, 'a'), (1, 'b'), (2, 'c'),
                                          (3, 'd')]
    assert list(prefixes([1, 2, 3, 4])) == [[], [1], [1, 2], [1, 2, 3],
                                            [1, 2, 3, 4]]
    assert list(alternate(iter("abcdef"), iter(
        [0, 1, 2]))) == ['a', 0, 'b', 1, 'c', 2, 'd', 'e', 'f']


def twice(f):
    return lambda x: f(f(x))


def test_twice():
    assert twice(lambda x: x * 2)(5) == 20


def pythagorean_triples(n: int):
    return [(a, b, c) for a in range(1, n) for b in range(1, n)
            for c in range(1, n) if a**2 + b**2 == c**2 and a <= b]


def test_pyth():
    assert sorted(list(pythagorean_triples(15))) == sorted([(3, 4, 5),
                                                            (6, 8, 10),
                                                            (5, 12, 13)])


print(list(alternate(iter("abcdef"), iter([0, 1, 2]))))
