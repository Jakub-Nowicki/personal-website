from flask import Blueprint, render_template, request
from ..utils.number_converter import convert_between_bases

converter_bp = Blueprint('converter', __name__)


@converter_bp.route('/converter', methods=['GET', 'POST'])
def system_converter():
    # Default values
    input_number = ""
    result = ""
    from_base = 10
    to_base = 2
    error = None

    if request.method == 'POST':
        try:
            input_number = request.form.get('input_number', '').strip()
            from_base_input = request.form.get('from_base', '10')
            to_base_input = request.form.get('to_base', '2')

            # Validate bases
            if not from_base_input.isdigit() or not to_base_input.isdigit():
                error = "Base must be a number."
            else:
                from_base = int(from_base_input)
                to_base = int(to_base_input)

                if not (2 <= from_base <= 16) or not (2 <= to_base <= 16):
                    error = "Base must be between 2 and 16."
                elif not input_number:
                    error = "Please enter a number to convert."
                else:
                    try:
                        # Perform the conversion
                        result = convert_between_bases(input_number, from_base, to_base)
                    except ValueError as e:
                        error = str(e)
        except Exception as e:
            error = f"An error occurred: {str(e)}"

    return render_template('converter.html',
                           input_number=input_number,
                           result=result,
                           from_base=from_base,
                           to_base=to_base,
                           error=error)