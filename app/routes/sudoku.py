from flask import Blueprint, render_template, request, redirect, url_for
from ..utils.sudoku_solver import solve, find_empty, valid

sudoku_bp = Blueprint('sudoku', __name__)

grid = [['' for _ in range(9)] for _ in range(9)]

@sudoku_bp.route('/sudoku')
def sudoku_solver():
    values = []
    grid = [['' for _ in range(9)] for _ in range(9)]
    return render_template('sudoku_index.html', grid=grid, values=values)

@sudoku_bp.route('/update', methods=['POST'])
def update():
    values = []
    for i in range(9):
        for j in range(9):
            grid[i][j] = request.form.get(f'cell-{i}-{j}', '') #getting values from the grid

    for i in range(9):
        for j in range(9):
            if grid[i][j] != '':
                values.append((i,j))
                grid[i][j] = int(grid[i][j]) #changing all the '' values to 0
            else:
                grid[i][j] = 0
    solve(grid) #solving the grid

    return render_template('sudoku_update.html', grid=grid, values=values)


@sudoku_bp.route('/solve_grid', methods=['POST'])
def solve_grid():
    # This route can be used to trigger solving from the client-side
    # It currently just redirects to the main Sudoku page
    return redirect(url_for('sudoku.sudoku_solver'))
