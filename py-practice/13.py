from typing import Callable, TypeVar, Union
from dataclasses import dataclass


def inc(x: int) -> int:
    return x + 1

def mul_1(x: int) -> Callable[[int], int]:
    def mul_with_x(y):
        return x * y
    return mul_with_x

mul_2: Callable[[int], Callable[[int], int]] = lambda x: lambda y: x * y

def test_mul():
    assert mul_1(2)(3) == 6
    assert mul_2(2)(3) == 6

T = TypeVar('T')
def compose(f: Callable[[T], T], g: Callable[[T], T]) -> Callable[[T], T]:
    return lambda x: f(g(x))

def test_comp():
    assert compose(lambda x: x + 1, lambda x: x * 2)(4) == 9

@dataclass
class V3:
    x: int
    y: int
    z: int

    def __add__(self, other: 'V3'):
        if type(other) is not V3:
            raise TypeError
        return mapV3(lambda x, y: x + y)(self, other)

    def __sub__(self, other: 'V3'):
        if type(other) is not V3:
            raise TypeError
        return mapV3(lambda x, y: x - y)(self, other)

    def __mul__(self, other: Union['V3', int]):
        if type(other) is int:
            other = V3(other, other, other)
        if type(other) is not V3:
            raise TypeError
        return mapV3(lambda x, y: x * y)(self, other)



def mapV3(f: Callable[[int, int], int]) -> Callable[[V3, V3], V3]:
    return lambda v0, v1: V3(f(v0.x, v1.x), f(v0.y, v1.y), f(v0.z, v1.z))

def test_map():
    v0 = V3(0, 0, 0)
    v1 = V3(1, 2, 3)
    assert v0 + v1 == v1
    assert v0 - v1 == v1 *  -1
    v0 - 1


