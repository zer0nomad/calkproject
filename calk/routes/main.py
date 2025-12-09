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
            else:
                error = gettext('Unknown operation')
        except svc.DivisionByZeroError:
            error = gettext('Division by zero is not allowed')
        except Exception:
            error = gettext('Calculation error')

    return render_template('index.html', result=result, error=error)
