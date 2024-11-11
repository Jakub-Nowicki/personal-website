from sudoku_solver import solve
from converter import convert_to_decimal, convert_to_any_base
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
    if request.method == 'POST':
        num_dec = request.form['num_dec']
        num_base = request.form['num_base']
        base = request.form['base']

        # Ensure base is an integer
        base = int(base) if base.isdigit() else 10

        if num_dec.strip():
            num_base = convert_to_any_base(num_dec, base)
        elif num_base.strip():
            num_dec = convert_to_decimal(num_base, base)

        return render_template('converter.html', num_dec=num_dec, num_base=num_base, base=base)
    else:
        return render_template('converter.html')
