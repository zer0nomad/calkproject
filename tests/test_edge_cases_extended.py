"""Extended edge case tests for comprehensive coverage."""
import pytest
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from calk.services import calculator_service as svc


@pytest.mark.edge_case
class TestArithmeticEdgeCases:
    """Test edge cases in arithmetic operations."""

    def test_add_infinity(self):
        """Test addition with infinity."""
        assert svc.add(float('inf'), 5) == float('inf')
        assert svc.add(5, float('inf')) == float('inf')

    def test_sub_very_close_numbers(self):
        """Test subtraction of very close floating point numbers."""
        result = svc.sub(1.0000001, 1.0000000)
        assert pytest.approx(result, abs=1e-7) == 1e-7

    def test_mul_by_zero(self):
        """Test multiplication by zero."""
        assert svc.mul(999999, 0) == 0
        assert svc.mul(0, 999999) == 0

    def test_mul_negative_numbers(self):
        """Test multiplication of negative numbers."""
        assert svc.mul(-5, -3) == 15
        assert svc.mul(-5, 3) == -15
        assert svc.mul(5, -3) == -15

    def test_div_result_one(self):
        """Test division resulting in 1."""
        assert svc.div(5, 5) == 1
        assert svc.div(123, 123) == 1

    def test_div_very_small_divisor(self):
        """Test division by very small number."""
        result = svc.div(1, 1e-10)
        assert result == 1e10

    def test_div_negative_numbers(self):
        """Test division of negative numbers."""
        assert svc.div(-10, -2) == 5
        assert svc.div(-10, 2) == -5
        assert svc.div(10, -2) == -5


@pytest.mark.edge_case
class TestSquareRootEdgeCases:
    """Test edge cases for square root."""

    def test_sqrt_zero(self):
        """Test square root of zero."""
        assert svc.sqrt(0) == 0

    def test_sqrt_one(self):
        """Test square root of one."""
        assert svc.sqrt(1) == 1

    def test_sqrt_small_number(self):
        """Test square root of small number."""
        result = svc.sqrt(0.0001)
        assert pytest.approx(result, rel=1e-6) == 0.01

    def test_sqrt_large_number(self):
        """Test square root of large number."""
        result = svc.sqrt(1e10)
        assert pytest.approx(result, rel=1e-6) == 1e5

    def test_sqrt_perfect_square(self):
        """Test square root of perfect squares."""
        for i in range(1, 20):
            result = svc.sqrt(i * i)
            assert pytest.approx(result) == i


@pytest.mark.edge_case
class TestTrigonometricEdgeCases:
    """Test edge cases for trigonometric functions."""

    def test_sin_zero(self):
        """Test sin(0)."""
        assert pytest.approx(svc.sin(0), abs=1e-10) == 0

    def test_sin_pi(self):
        """Test sin(π)."""
        result = svc.sin(math.pi, in_degrees=False)
        assert pytest.approx(result, abs=1e-10) == 0

    def test_sin_pi_half(self):
        """Test sin(π/2)."""
        result = svc.sin(math.pi / 2, in_degrees=False)
        assert pytest.approx(result, rel=1e-10) == 1

    def test_cos_zero(self):
        """Test cos(0)."""
        result = svc.cos(0)
        assert pytest.approx(result, rel=1e-10) == 1

    def test_cos_pi(self):
        """Test cos(π)."""
        result = svc.cos(math.pi, in_degrees=False)
        assert pytest.approx(result, abs=1e-10) == -1

    def test_tan_zero(self):
        """Test tan(0)."""
        assert pytest.approx(svc.tan(0), abs=1e-10) == 0

    def test_tan_pi_quarter(self):
        """Test tan(π/4)."""
        result = svc.tan(math.pi / 4, in_degrees=False)
        assert pytest.approx(result, rel=1e-10) == 1

    def test_large_angle_values(self):
        """Test trigonometric functions with large angles."""
        # sin and cos should still be between -1 and 1
        assert -1 <= svc.sin(1000) <= 1
        assert -1 <= svc.cos(1000) <= 1


@pytest.mark.edge_case
class TestLogarithmEdgeCases:
    """Test edge cases for logarithm functions."""

    def test_ln_one(self):
        """Test ln(1)."""
        result = svc.ln(1)
        assert pytest.approx(result, abs=1e-10) == 0

    def test_ln_e(self):
        """Test ln(e)."""
        result = svc.ln(math.e)
        assert pytest.approx(result, rel=1e-10) == 1

    def test_ln_small_number(self):
        """Test ln of small number."""
        result = svc.ln(0.1)
        assert pytest.approx(result, rel=1e-10) == math.log(0.1)

    def test_log10_one(self):
        """Test log10(1)."""
        result = svc.log10(1)
        assert pytest.approx(result, abs=1e-10) == 0

    def test_log10_ten(self):
        """Test log10(10)."""
        result = svc.log10(10)
        assert pytest.approx(result, rel=1e-10) == 1

    def test_log10_hundred(self):
        """Test log10(100)."""
        result = svc.log10(100)
        assert pytest.approx(result, rel=1e-10) == 2


@pytest.mark.edge_case
class TestExponentialEdgeCases:
    """Test edge cases for exponential function."""

    def test_exp_zero(self):
        """Test e^0."""
        result = svc.exp(0)
        assert pytest.approx(result, rel=1e-10) == 1

    def test_exp_one(self):
        """Test e^1."""
        result = svc.exp(1)
        assert pytest.approx(result, rel=1e-10) == math.e

    def test_exp_negative(self):
        """Test e^(-x)."""
        result = svc.exp(-1)
        assert pytest.approx(result, rel=1e-10) == 1 / math.e

    def test_exp_large_number(self):
        """Test e^(large number)."""
        # Should handle large numbers
        result = svc.exp(100)
        assert result > 1e40


@pytest.mark.edge_case
class TestFactorialEdgeCases:
    """Test edge cases for factorial."""

    def test_factorial_zero(self):
        """Test 0!"""
        assert svc.factorial(0) == 1

    def test_factorial_one(self):
        """Test 1!"""
        assert svc.factorial(1) == 1

    def test_factorial_sequence(self):
        """Test factorial sequence."""
        expected = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
        for i, exp in enumerate(expected):
            assert svc.factorial(i) == exp

    def test_factorial_large_number(self):
        """Test factorial of large number."""
        result = svc.factorial(20)
        assert result == 2432902008176640000

    def test_factorial_commutative_with_mul(self):
        """Test that factorial is consistent with multiplication."""
        assert svc.factorial(5) == svc.mul(5, svc.factorial(4))


@pytest.mark.edge_case
class TestPowerEdgeCases:
    """Test edge cases for power function."""

    def test_power_zero_exponent(self):
        """Test x^0."""
        assert svc.power(5, 0) == 1
        assert svc.power(0, 0) == 1  # By convention
        assert svc.power(1000, 0) == 1

    def test_power_one_exponent(self):
        """Test x^1."""
        assert svc.power(5, 1) == 5
        assert svc.power(0, 1) == 0

    def test_power_negative_exponent(self):
        """Test x^(-n)."""
        result = svc.power(2, -2)
        assert pytest.approx(result, rel=1e-10) == 0.25

    def test_power_fractional_exponent(self):
        """Test x^(1/2) as square root."""
        result = svc.power(4, 0.5)
        assert pytest.approx(result, rel=1e-10) == 2

    def test_power_zero_base_positive_exponent(self):
        """Test 0^n where n > 0."""
        assert svc.power(0, 5) == 0

    def test_power_negative_base_even_exponent(self):
        """Test (-x)^(even)."""
        result = svc.power(-2, 2)
        assert result == 4

    def test_power_negative_base_odd_exponent(self):
        """Test (-x)^(odd)."""
        result = svc.power(-2, 3)
        assert result == -8


@pytest.mark.edge_case
class TestSquareEdgeCases:
    """Test edge cases for square operation."""

    def test_square_zero(self):
        """Test 0^2."""
        assert svc.square(0) == 0

    def test_square_one(self):
        """Test 1^2."""
        assert svc.square(1) == 1

    def test_square_negative(self):
        """Test (-x)^2."""
        assert svc.square(-5) == 25

    def test_square_large_number(self):
        """Test square of large number."""
        result = svc.square(1e10)
        assert result == 1e20


@pytest.mark.edge_case
class TestPercentEdgeCases:
    """Test edge cases for percent operation."""

    def test_percent_of_zero(self):
        """Test 0% of anything."""
        assert svc.percent(0, 100) == 0

    def test_percent_of_itself(self):
        """Test 100% of number."""
        assert svc.percent(100, 100) == 100

    def test_percent_zero_base(self):
        """Test x% of 0."""
        assert svc.percent(50, 0) == 0

    def test_percent_negative(self):
        """Test negative percentages."""
        result = svc.percent(-50, 100)
        assert result == -50

    def test_percent_over_hundred(self):
        """Test percentages over 100%."""
        result = svc.percent(150, 100)
        assert result == 150


@pytest.mark.edge_case
class TestReciprocalEdgeCases:
    """Test edge cases for reciprocal."""

    def test_reciprocal_one(self):
        """Test 1/1."""
        assert svc.reciprocal(1) == 1

    def test_reciprocal_negative(self):
        """Test reciprocal of negative number."""
        result = svc.reciprocal(-2)
        assert pytest.approx(result, rel=1e-10) == -0.5

    def test_reciprocal_fraction(self):
        """Test reciprocal of fraction."""
        result = svc.reciprocal(0.5)
        assert pytest.approx(result, rel=1e-10) == 2

    def test_reciprocal_very_small_number(self):
        """Test reciprocal of very small number."""
        result = svc.reciprocal(1e-10)
        assert result == 1e10


@pytest.mark.edge_case
class TestNegateEdgeCases:
    """Test edge cases for negate operation."""

    def test_negate_zero(self):
        """Test negating zero."""
        assert svc.negate(0) == 0 or svc.negate(0) == -0  # -0 == 0

    def test_negate_positive(self):
        """Test negating positive number."""
        assert svc.negate(5) == -5

    def test_negate_negative(self):
        """Test negating negative number."""
        assert svc.negate(-5) == 5

    def test_double_negate(self):
        """Test double negation."""
        assert svc.negate(svc.negate(5)) == 5


@pytest.mark.edge_case
class TestConstantsEdgeCases:
    """Test edge cases for constants."""

    def test_pi_value(self):
        """Test pi constant value."""
        pi = svc.pi()
        assert pytest.approx(pi, rel=1e-10) == math.pi

    def test_euler_value(self):
        """Test Euler's number value."""
        e = svc.euler()
        assert pytest.approx(e, rel=1e-10) == math.e

    def test_pi_usage_in_calculation(self):
        """Test using pi in calculations."""
        # 2 * pi * r for radius 1
        result = svc.mul(2, svc.pi())
        assert pytest.approx(result, rel=1e-10) == 2 * math.pi


@pytest.mark.edge_case
class TestNumericalStability:
    """Test numerical stability of operations."""

    def test_cancellation_error(self):
        """Test potential cancellation error."""
        # (a + b) - a should equal b
        a = 1e10
        b = 1.0
        result = svc.sub(svc.add(a, b), a)
        # Due to floating point, might not be exactly equal
        assert result == pytest.approx(b, rel=0.01)

    def test_associativity_floating_point(self):
        """Test associativity with floating point."""
        # (a + b) + c vs a + (b + c)
        a, b, c = 0.1, 0.2, 0.3
        result1 = svc.add(svc.add(a, b), c)
        result2 = svc.add(a, svc.add(b, c))
        # Both should be close to 0.6
        assert pytest.approx(result1, rel=1e-10) == pytest.approx(0.6, rel=1e-10)
        assert pytest.approx(result2, rel=1e-10) == pytest.approx(0.6, rel=1e-10)
