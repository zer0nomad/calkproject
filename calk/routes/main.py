from flask import Blueprint, render_template, request
from flask_babel import gettext

from ..services import calculator_service as svc

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
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
            error = gettext('Division by zero is not allowed')
        except svc.CalculatorError as e:
            error = str(e)
        except Exception:
            error = gettext('Calculation error')

    return render_template('index.html', result=result, error=error)
