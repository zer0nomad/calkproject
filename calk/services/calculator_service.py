"""Service layer: pure Python, no Flask dependencies.

Provides basic arithmetic operations and raises clear exceptions
for invalid operations (division by zero, sqrt of negative).
"""
from math import sqrt as _sqrt


class CalculatorError(Exception):
    pass


class DivisionByZeroError(CalculatorError):
    pass


def add(a: float, b: float) -> float:
    return a + b


def sub(a: float, b: float) -> float:
    return a - b


def mul(a: float, b: float) -> float:
    return a * b


def div(a: float, b: float) -> float:
    if b == 0:
        raise DivisionByZeroError('division by zero')
    return a / b


def square(a: float) -> float:
    return a * a


def sqrt(a: float) -> float:
    if a < 0:
        raise CalculatorError('sqrt of negative number')
    return _sqrt(a)
