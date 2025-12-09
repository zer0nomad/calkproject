"""Service layer: pure Python, no Flask dependencies.

Provides basic arithmetic operations and raises clear exceptions
for invalid operations (division by zero, sqrt of negative).
"""
from math import sqrt as _sqrt, sin as _sin, cos as _cos, tan as _tan
from math import log as _log, log10 as _log10, exp as _exp, radians, degrees
from math import factorial as _factorial, pi, e


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


def sin(a: float, in_degrees: bool = True) -> float:
    """Sine function. If in_degrees=True, convert from degrees to radians."""
    rad = radians(a) if in_degrees else a
    return _sin(rad)


def cos(a: float, in_degrees: bool = True) -> float:
    """Cosine function. If in_degrees=True, convert from degrees to radians."""
    rad = radians(a) if in_degrees else a
    return _cos(rad)


def tan(a: float, in_degrees: bool = True) -> float:
    """Tangent function. If in_degrees=True, convert from degrees to radians."""
    rad = radians(a) if in_degrees else a
    return _tan(rad)


def log(a: float, base: float = 10) -> float:
    """Logarithm with given base (default 10)."""
    if a <= 0:
        raise CalculatorError('logarithm of non-positive number')
    if base <= 0 or base == 1:
        raise CalculatorError('invalid logarithm base')
    return _log(a) / _log(base)


def ln(a: float) -> float:
    """Natural logarithm (base e)."""
    if a <= 0:
        raise CalculatorError('logarithm of non-positive number')
    return _log(a)


def log10(a: float) -> float:
    """Base-10 logarithm."""
    if a <= 0:
        raise CalculatorError('logarithm of non-positive number')
    return _log10(a)


def exp(a: float) -> float:
    """Exponential function (e^a)."""
    return _exp(a)


def power(a: float, b: float) -> float:
    """Power function (a^b)."""
    if a == 0 and b < 0:
        raise DivisionByZeroError('division by zero in power')
    return a ** b


def factorial(a: float) -> float:
    """Factorial function (a!)."""
    if a < 0 or a != int(a):
        raise CalculatorError('factorial of negative or non-integer number')
    return float(_factorial(int(a)))


def reciprocal(a: float) -> float:
    """Reciprocal function (1/a)."""
    if a == 0:
        raise DivisionByZeroError('division by zero')
    return 1.0 / a


def percent(a: float) -> float:
    """Percent (divide by 100)."""
    return a / 100.0


def negate(a: float) -> float:
    """Negate a number."""
    return -a


def get_pi() -> float:
    """Return pi constant."""
    return pi


def get_e() -> float:
    """Return e constant."""
    return e
