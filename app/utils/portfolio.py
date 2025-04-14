from sudoku_solver import solve
from converter import convert_to_decimal, convert_to_any_base
from number_converter import convert_to_decimal, convert_from_decimal, convert_between_bases
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/projects')
def projects_page():
    return render_template('projects.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/sudoku')
def sudoku_solver():
    grid = [['' for _ in range(9)] for _ in range(9)]  # Local variable
    return render_template('sudoku_index.html', grid=grid)

@app.route('/update', methods=['POST'])
def update():
    grid = [['' for _ in range(9)] for _ in range(9)]  # Recreate the grid
    values = []
    for i in range(9):
        for j in range(9):
            cell_value = request.form.get(f'cell-{i}-{j}', '')
            grid[i][j] = int(cell_value) if cell_value.isdigit() else 0
            if cell_value:
                values.append((i, j))
    solve(grid)  # Solving the grid
    return render_template('sudoku_update.html', grid=grid, values=values)


@app.route('/solve_grid', methods =['POST'])
def solve_grid():
    return redirect(url_for('sudoku_solver'))


@app.route('/converter', methods=['POST', 'GET'])
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
