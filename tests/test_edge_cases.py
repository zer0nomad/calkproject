"""Extended calculator service tests with edge cases and boundaries."""
import pytest
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from calk.services import calculator_service as svc


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        assert svc.add(-5, -3) == -8
        assert svc.add(-5, 3) == -2
        assert svc.add(5, -3) == 2

    def test_add_zero(self):
        """Test addition with zero."""
        assert svc.add(0, 0) == 0
        assert svc.add(5, 0) == 5
        assert svc.add(0, 5) == 5

    def test_add_floating_point(self):
        """Test addition with floating point numbers."""
        assert pytest.approx(svc.add(0.1, 0.2), 1e-9) == 0.3
        assert pytest.approx(svc.add(1.5, 2.5), 1e-9) == 4.0

    def test_add_very_large_numbers(self):
        """Test addition with very large numbers."""
        assert svc.add(1e10, 1e10) == 2e10
        assert svc.add(1e100, 1) == 1e100  # Floating point precision

    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        assert svc.sub(-5, -3) == -2
        assert svc.sub(-5, 3) == -8
        assert svc.sub(5, -3) == 8

    def test_subtract_zero(self):
        """Test subtraction with zero."""
        assert svc.sub(5, 0) == 5
        assert svc.sub(0, 5) == -5
        assert svc.sub(0, 0) == 0

    def test_subtract_equal_numbers(self):
        """Test subtracting equal numbers."""
        assert svc.sub(5, 5) == 0
        assert svc.sub(3.14, 3.14) == pytest.approx(0, 1e-9)

    def test_multiply_zero(self):
        """Test multiplication by zero."""
        assert svc.mul(5, 0) == 0
        assert svc.mul(0, 5) == 0
        assert svc.mul(0, 0) == 0

    def test_multiply_one(self):
        """Test multiplication by one."""
        assert svc.mul(5, 1) == 5
        assert svc.mul(1, 5) == 5
        assert svc.mul(1, 1) == 1

    def test_multiply_negative(self):
        """Test multiplication with negative numbers."""
        assert svc.mul(-5, 3) == -15
        assert svc.mul(5, -3) == -15
        assert svc.mul(-5, -3) == 15

    def test_multiply_floating_point(self):
        """Test multiplication with floating point."""
        assert pytest.approx(svc.mul(0.5, 0.5), 1e-9) == 0.25
        assert pytest.approx(svc.mul(2.5, 4), 1e-9) == 10.0

    def test_divide_one(self):
        """Test division by one."""
        assert svc.div(5, 1) == 5
        assert svc.div(0, 1) == 0

    def test_divide_itself(self):
        """Test dividing number by itself."""
        assert svc.div(5, 5) == 1
        assert svc.div(3.14, 3.14) == pytest.approx(1, 1e-9)

    def test_divide_negative(self):
        """Test division with negative numbers."""
        assert svc.div(-10, 2) == -5
        assert svc.div(10, -2) == -5
        assert svc.div(-10, -2) == 5

    def test_divide_floating_point(self):
        """Test division with floating point."""
        assert pytest.approx(svc.div(1, 3), 1e-9) == 1/3
        assert pytest.approx(svc.div(10, 4), 1e-9) == 2.5

    def test_divide_very_small_number(self):
        """Test division by very small number (but not zero)."""
        result = svc.div(1, 1e-10)
        assert result > 0
        assert result > 1e9

    def test_square_zero(self):
        """Test squaring zero."""
        assert svc.square(0) == 0

    def test_square_one(self):
        """Test squaring one."""
        assert svc.square(1) == 1

    def test_square_negative(self):
        """Test squaring negative number."""
        assert svc.square(-5) == 25
        assert svc.square(-3) == 9

    def test_square_fraction(self):
        """Test squaring fractional number."""
        assert pytest.approx(svc.square(0.5), 1e-9) == 0.25

    def test_square_large_number(self):
        """Test squaring large number."""
        result = svc.square(1e6)
        assert result == 1e12

    def test_sqrt_one(self):
        """Test square root of one."""
        assert svc.sqrt(1) == 1

    def test_sqrt_zero(self):
        """Test square root of zero."""
        assert svc.sqrt(0) == 0

    def test_sqrt_fraction(self):
        """Test square root of fraction."""
        assert pytest.approx(svc.sqrt(0.25), 1e-9) == 0.5

    def test_sqrt_perfect_squares(self):
        """Test square root of perfect squares."""
        for n in [4, 9, 16, 25, 100]:
            assert pytest.approx(svc.sqrt(n), 1e-9) == math.sqrt(n)

    def test_sqrt_large_number(self):
        """Test square root of large number."""
        assert pytest.approx(svc.sqrt(1e8), 1e-9) == 1e4

    def test_sin_common_angles(self):
        """Test sine of common angles."""
        assert pytest.approx(svc.sin(0), 1e-9) == 0
        assert pytest.approx(svc.sin(90), 1e-9) == 1
        assert pytest.approx(svc.sin(180), 1e-9) == 0

    def test_sin_negative_angle(self):
        """Test sine of negative angle."""
        assert pytest.approx(svc.sin(-90), 1e-9) == -1

    def test_cos_common_angles(self):
        """Test cosine of common angles."""
        assert pytest.approx(svc.cos(0), 1e-9) == 1
        assert pytest.approx(svc.cos(90), 1e-9) == 0
        assert pytest.approx(svc.cos(180), 1e-9) == -1

    def test_tan_zero(self):
        """Test tangent of zero."""
        assert pytest.approx(svc.tan(0), 1e-9) == 0

    def test_tan_45_degrees(self):
        """Test tangent of 45 degrees."""
        assert pytest.approx(svc.tan(45), 1e-9) == 1

    def test_log10_one(self):
        """Test log10 of 1."""
        assert pytest.approx(svc.log10(1), 1e-9) == 0

    def test_log10_ten(self):
        """Test log10 of 10."""
        assert pytest.approx(svc.log10(10), 1e-9) == 1

    def test_log10_zero_error(self):
        """Test that log10(0) raises error."""
        with pytest.raises(svc.CalculatorError):
            svc.log10(0)

    def test_log10_negative_error(self):
        """Test that log10(negative) raises error."""
        with pytest.raises(svc.CalculatorError):
            svc.log10(-5)

    def test_log10_large_number(self):
        """Test log10 of large number."""
        assert pytest.approx(svc.log10(1e6), 1e-9) == 6

    def test_ln_one(self):
        """Test natural log of 1."""
        assert pytest.approx(svc.ln(1), 1e-9) == 0

    def test_ln_e(self):
        """Test natural log of e."""
        assert pytest.approx(svc.ln(math.e), 1e-9) == 1

    def test_ln_zero_error(self):
        """Test that ln(0) raises error."""
        with pytest.raises(svc.CalculatorError):
            svc.ln(0)

    def test_exp_zero(self):
        """Test e^0."""
        assert pytest.approx(svc.exp(0), 1e-9) == 1

    def test_exp_one(self):
        """Test e^1."""
        assert pytest.approx(svc.exp(1), 1e-9) == math.e

    def test_exp_negative(self):
        """Test e^(-x)."""
        assert pytest.approx(svc.exp(-1), 1e-9) == 1/math.e

    def test_power_zero(self):
        """Test 0^n."""
        assert svc.power(0, 5) == 0
        assert svc.power(0, 0) == 1  # Mathematical convention

    def test_power_one(self):
        """Test 1^n."""
        assert svc.power(1, 100) == 1

    def test_power_negative_exponent(self):
        """Test x^(-n)."""
        assert pytest.approx(svc.power(2, -1), 1e-9) == 0.5
        assert pytest.approx(svc.power(10, -2), 1e-9) == 0.01

    def test_power_fractional_exponent(self):
        """Test x^(0.5) (square root via power)."""
        assert pytest.approx(svc.power(4, 0.5), 1e-9) == 2
        assert pytest.approx(svc.power(9, 0.5), 1e-9) == 3

    def test_factorial_zero(self):
        """Test 0! = 1."""
        assert svc.factorial(0) == 1

    def test_factorial_one(self):
        """Test 1! = 1."""
        assert svc.factorial(1) == 1

    def test_factorial_small_numbers(self):
        """Test factorial for small numbers."""
        assert svc.factorial(2) == 2
        assert svc.factorial(3) == 6
        assert svc.factorial(5) == 120
        assert svc.factorial(10) == 3628800

    def test_factorial_negative_error(self):
        """Test that factorial of negative number raises error."""
        with pytest.raises(svc.CalculatorError):
            svc.factorial(-1)

    def test_factorial_float_error(self):
        """Test that factorial of float raises error."""
        with pytest.raises(svc.CalculatorError):
            svc.factorial(3.5)

    def test_reciprocal_one(self):
        """Test 1/1."""
        assert svc.reciprocal(1) == 1

    def test_reciprocal_negative(self):
        """Test reciprocal of negative number."""
        assert svc.reciprocal(-5) == -0.2

    def test_reciprocal_fraction(self):
        """Test reciprocal of fraction."""
        assert svc.reciprocal(0.5) == 2

    def test_percent_zero(self):
        """Test 0% (0/100)."""
        assert svc.percent(0) == 0

    def test_percent_hundred(self):
        """Test 100% (100/100)."""
        assert svc.percent(100) == 1.0

    def test_percent_fifty(self):
        """Test 50% (50/100)."""
        assert svc.percent(50) == 0.5

    def test_percent_negative(self):
        """Test negative percentage."""
        assert svc.percent(-50) == -0.5

    def test_negate_positive(self):
        """Test negating positive number."""
        assert svc.negate(5) == -5

    def test_negate_negative(self):
        """Test negating negative number."""
        assert svc.negate(-5) == 5

    def test_negate_zero(self):
        """Test negating zero."""
        assert svc.negate(0) == 0

    def test_pi_value(self):
        """Test that pi has correct value."""
        assert pytest.approx(svc.get_pi(), 1e-9) == math.pi

    def test_euler_value(self):
        """Test that euler number has correct value."""
        assert pytest.approx(svc.get_e(), 1e-9) == math.e
