from dataclasses import dataclass
from typing import Optional
import math
from dataclasses import dataclass


def count_iterations(n: int) -> int:
    counter = 0
    while n != 0:
        if n % 3 == 0:
            n += 4
        elif n % 4 == 0:
            n //= 2
        else:
            n -= 1
        counter += 1
    return counter


def test_count():
    assert count_iterations(5) == 4


def cluster_by_points(points: dict[str, int]) -> dict[int, list[str]]:
    cl: dict[int, list[str]] = {}
    for (v, k) in points.items():
        if (k2 := k - (k % 10)) not in cl:
            cl[k2] = [v]
        else:
            cl[k2].append(v)
    return cl


def test_cl():
    points = {"Line": 9, "Daniel": 12, "Charlotte": 15, "Frank": 30}
    assert cluster_by_points(points) == {
        0: ['Line'],
        10: ['Daniel', 'Charlotte'],
        30: ['Frank']
    }


def is_strong(pw: str) -> bool:
    c = len(pw)
    if c < 8:
        return False
    c_d = sum(1 for s in pw if s.isdigit())
    if c_d < 1:
        return False
    c_s = sum(1 for s in pw if s in "!?+*")
    if c_d <= 3 and c_s < 1:
        return False
    c_u = sum(1 for s in pw if s.isupper())
    if c_u < 3 and c_s < 1:
        return False
    if c_u < 3 and c_d <= 3 and c_s < 2:
        return False
    return True


@dataclass
class Ranking:
    club: str
    wins: int
    draws: int
    losses: int
    goals_archived: int
    goals_conceded: int

    def points(self) -> int:
        return self.wins * 3 + self.draws

    def diff(self) -> int:
        return self.goals_archived - self.goals_conceded

    def games(self) -> int:
        return self.wins + self.draws + self.losses

    def table_entry(self) -> str:
        return " ".join([
            str(self.club),
            str(self.games()),
            str(self.wins),
            str(self.draws),
            str(self.losses), f"{self.goals_archived}:{self.goals_conceded}",
            str(self.diff()),
            str(self.points())
        ])

    def __lt__(self, o) -> bool:
        if type(o) is not Ranking:
            return False
        if self.points() < o.points():
            return True
        elif self.points() == o.points():
            if self.diff() < o.diff():
                return True
            elif self.diff() == o.diff():
                return self.goals_archived < o.goals_archived
        return False


def test_str():
    assert Ranking("FC H.", 6, 2, 2, 23,
                   14).table_entry() == "FC H. 10 6 2 2 23:14 9 20"


def test_ls():
    r1 = Ranking("FC H.", 6, 2, 2, 23, 14)
    r2 = Ranking("FC U.", 5, 3, 2, 20, 15)
    assert r2 < r1
    assert not (r1 < r1)


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
    return [(a, b, c) for a in range(1, n) for b in range(a, n)
            for c in range(b, n) if a**2 + b**2 == c**2]


def test_pyth():
    assert sorted(list(pythagorean_triples(15))) == sorted([(3, 4, 5),
                                                            (6, 8, 10),
                                                            (5, 12, 13)])
