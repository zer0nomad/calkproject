import pytest
import sys
import os

# ensure project root is on sys.path for test discovery
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from calk.services import calculator_service as svc


def test_add():
    assert svc.add(1, 2) == 3


def test_sub():
    assert svc.sub(5, 3) == 2


def test_mul():
    assert svc.mul(2, 3) == 6


def test_div():
    assert svc.div(10, 2) == 5


def test_div_by_zero():
    with pytest.raises(svc.DivisionByZeroError):
        svc.div(1, 0)


def test_square():
    assert svc.square(4) == 16


def test_sqrt():
    assert pytest.approx(svc.sqrt(9), 1e-9) == 3


def test_sqrt_negative():
    with pytest.raises(svc.CalculatorError):
        svc.sqrt(-4)
