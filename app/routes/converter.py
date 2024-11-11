from flask import Blueprint, render_template, request
from ..utils.number_converter import convert_to_decimal, convert_to_any_base

converter_bp = Blueprint('converter', __name__)

@converter_bp.route('/converter', methods=['GET', 'POST'])
def system_converter():
    num_dec = ""
    num_base = ""
    base = 10

    if request.method == 'POST':
        num_dec = request.form.get('num_dec', '')
        num_base = request.form.get('num_base', '')
        base = request.form.get('base', '10')

        # Ensure base is an integer
        base = int(base) if base.isdigit() else 10

        if num_dec.strip():
            num_base = convert_to_any_base(num_dec, base)
        elif num_base.strip():
            num_dec = convert_to_decimal(num_base, base)

    return render_template('converter.html', num_dec=num_dec, num_base=num_base, base=base)
