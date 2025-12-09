import pytest
import sys
import os
import math

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


def test_sin():
    assert pytest.approx(svc.sin(0), 1e-9) == 0
    assert pytest.approx(svc.sin(90), 1e-9) == 1


def test_cos():
    assert pytest.approx(svc.cos(0), 1e-9) == 1
    assert pytest.approx(svc.cos(90), 1e-9) == 0


def test_tan():
    assert pytest.approx(svc.tan(0), 1e-9) == 0


def test_log10():
    assert pytest.approx(svc.log10(10), 1e-9) == 1
    assert pytest.approx(svc.log10(100), 1e-9) == 2


def test_ln():
    assert pytest.approx(svc.ln(math.e), 1e-9) == 1


def test_exp():
    assert pytest.approx(svc.exp(0), 1e-9) == 1
    assert pytest.approx(svc.exp(1), 1e-9) == math.e


def test_power():
    assert svc.power(2, 3) == 8
    assert svc.power(5, 0) == 1


def test_factorial():
    assert svc.factorial(5) == 120
    assert svc.factorial(0) == 1


def test_reciprocal():
    assert svc.reciprocal(2) == 0.5
    assert svc.reciprocal(0.5) == 2


def test_reciprocal_zero():
    with pytest.raises(svc.DivisionByZeroError):
        svc.reciprocal(0)


def test_percent():
    assert svc.percent(50) == 0.5
    assert svc.percent(100) == 1


def test_negate():
    assert svc.negate(5) == -5
    assert svc.negate(-3) == 3


def test_constants():
    assert pytest.approx(svc.get_pi(), 1e-9) == math.pi
    assert pytest.approx(svc.get_e(), 1e-9) == math.e
