import re
from dataclasses import dataclass
from typing import Callable, Iterator, Optional, TypeVar

def count_folds(width: int, height: int) -> int:
    if width == 0 or height == 0:
        return 0
    if width > height:
        return count_folds(width//2, height) + 1
    else:
        return count_folds(width, height//2) + 1

def test_count_folds():
    assert count_folds(2, 1) == 2
    assert count_folds(15, 7) == 6

def cluster_by_ingredience(recipes: dict[str, list[str]]) -> dict[str, list[str]]:
    d: dict[str, list[str]] = {}
    for (meal, ls) in recipes.items():
        for ing in ls:
            if ing not in d:
                d[ing] = [meal]
            else:
                d[ing] += [meal]
    return d


def is_scientific(s: str) -> bool:
    return bool(re.match(r"-?\d+\.\d+e-?\d+", s))

def test_sc():
    assert is_scientific("3.0e5")
    assert is_scientific("2.1e-3")
    assert is_scientific("-7.0e13")
    assert not is_scientific("3.0")

@dataclass
class Robot:
    hp: int
    armor: int
    attack: int
    robot_typ: int

    def __post_init__(self):
        assert 0 < self.robot_typ < 4

    def hit_damage(self, other: 'Robot') -> int:
        dmg = self.attack - other.armor
        match (self.robot_typ, other.robot_typ):
            case (1, 2): dmg -= 1
            case (1, 3): dmg += 2
        return dmg if dmg > 0 else 1

    def __ge__(self, other) -> bool:
        if type(other) is not Robot:
            return False
        hp_s = self.hp
        hp_o = other.hp
        while (hp_o > 0):
            if hp_s < 1:

                return False
            hp_o -= self.hit_damage(other)
            hp_s -= other.hit_damage(self)
        return True

def test_fight():
    r1 = Robot(10, 1, 5, 1)
    r2 = Robot(16, 2, 3, 2)
    assert not (r1 >= r2)
    assert r1 >= Robot(10, 1, 5, 1)


@dataclass
class Node:
    mark: str
    left: Optional['Node']
    right: Optional['Node']

def layer(n: int, node: Node) -> list[str]:
    ls: list[str] = []
    if n == 0:
        return [node.mark]
    if node.left is not None:
        ls += layer(n - 1, node.left)
    if node.right is not None:
        ls += layer(n - 1, node.right)
    return ls


def test_tree():
    tree = Node("0", Node("1a", None, Node("2", None, None)), Node("1b", None, None))
    assert layer(0, tree) == ['0']
    assert layer(1, tree) == ['1a', '1b']
    assert layer(2, tree) == ['2']

def accumulate(it: Iterator[int]) -> Iterator[int]:
    sum = 0
    while (i := next(it, None)) is not None:
        yield (sum := sum + i)

def test_acc():
    assert list(accumulate(iter([1, 2, 3, 4, 5, 6]))) == [1, 3, 6, 10, 15, 21]

def double(n: int) -> int:
    return n * 2

def my_map(f, xs: Iterator[int]) -> Iterator[int]:
    for i in xs:
        yield f(i)

def test_map():
    assert list(my_map(lambda x: x * 2, iter([1, 2, 3, 4]))) == [2, 4, 6, 8]

T = TypeVar('T')
def init(xs: Iterator[T]) -> Iterator[T]:
    t: Optional[T] = next(xs, None)
    while (i0 := next(xs, None)) is not None:
        assert t is not None
        yield t
        t = i0

def test_init():
    assert list(init(iter([1, 2, 3, 4]))) == [1, 2, 3]
    assert list(init(iter([]))) == []

S = TypeVar('S')
def paired(f: Callable[[S], S], g: Callable[[S], S]) -> Callable[[S, S], tuple[S, S]]:
    return lambda x, y: (f(x), g(y))

def test_paired():
    assert paired(lambda x: x * 2, lambda x: x * 3)(5, 10) == (10, 30)

def is_prime(n: int) -> bool:
    return not (any( [x for x in iter(range(2, n)) if n % x == 0]) or n < 2)

def test_prime():
    assert not is_prime(0)
    assert not is_prime(4)
    assert is_prime(5)
    assert is_prime(13)
