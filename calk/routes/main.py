from flask import Blueprint, render_template, request, redirect, url_for
from flask_babel import gettext, get_locale

from ..services import calculator_service as svc

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    # Handle language selection
    lang = request.args.get('lang')
    if lang:
        response = redirect(url_for('main.index'))
        response.set_cookie('lang', lang, max_age=60*60*24*365)
        return response
    result = None
    error = None
    op = None

    if request.method == 'POST':
        op = request.form.get('operation')
        a_raw = request.form.get('a', '').strip()
        b_raw = request.form.get('b', '').strip()

        # try to parse inputs
        try:
            a = float(a_raw) if a_raw != '' else 0.0
        except ValueError:
            error = gettext('Invalid input for A')
            return render_template('index.html', result=result, error=error)

        try:
            b = float(b_raw) if b_raw != '' else 0.0
        except ValueError:
            error = gettext('Invalid input for B')
            return render_template('index.html', result=result, error=error)

        try:
            # Basic operations
            if op == 'add':
                result = svc.add(a, b)
            elif op == 'sub':
                result = svc.sub(a, b)
            elif op == 'mul':
                result = svc.mul(a, b)
            elif op == 'div':
                result = svc.div(a, b)
            elif op == 'square':
                result = svc.square(a)
            elif op == 'sqrt':
                result = svc.sqrt(a)
            # Engineering functions (single operand)
            elif op == 'sin':
                result = svc.sin(a, in_degrees=True)
            elif op == 'cos':
                result = svc.cos(a, in_degrees=True)
            elif op == 'tan':
                result = svc.tan(a, in_degrees=True)
            elif op == 'log':
                result = svc.log10(a)
            elif op == 'ln':
                result = svc.ln(a)
            elif op == 'exp':
                result = svc.exp(a)
            elif op == 'factorial':
                result = svc.factorial(a)
            elif op == 'reciprocal':
                result = svc.reciprocal(a)
            elif op == 'percent':
                result = svc.percent(a)
            elif op == 'negate':
                result = svc.negate(a)
            # Two-operand engineering
            elif op == 'power':
                result = svc.power(a, b)
            elif op == 'log_base':
                result = svc.log(a, b)
            # Constants
            elif op == 'pi':
                result = svc.get_pi()
            elif op == 'e':
                result = svc.get_e()
            else:
                error = gettext('Unknown operation')
        except svc.DivisionByZeroError:
            error = gettext('Cannot divide by zero. Please check your values.')
        except svc.CalculatorError as e:
            # Translate specific error messages
            error_msg = str(e)
            if 'sqrt of negative' in error_msg:
                error = gettext('Cannot take square root of a negative number.')
            elif 'logarithm of non-positive' in error_msg:
                error = gettext('Logarithm is only defined for positive numbers.')
            elif 'factorial of negative' in error_msg:
                error = gettext('Factorial is only defined for non-negative integers.')
            elif 'factorial of non-integer' in error_msg:
                error = gettext('Factorial requires a whole number (integer).')
            elif 'invalid logarithm base' in error_msg:
                error = gettext('Invalid logarithm base. Must be positive and not equal to 1.')
            else:
                error = str(e)
        except Exception:
            error = gettext('Calculation error. Please check your input and try again.')

    return render_template('index.html', result=result, error=error)
