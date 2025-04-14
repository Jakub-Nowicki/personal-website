from flask import Blueprint, render_template, request, redirect, url_for
from ..utils.sudoku_solver import solve, find_empty, valid, is_valid_sudoku
import time

sudoku_bp = Blueprint('sudoku', __name__)


@sudoku_bp.route('/sudoku')
def sudoku_solver():
    grid = [['' for _ in range(9)] for _ in range(9)]  # Local variable
    return render_template('sudoku_index.html', grid=grid)


@sudoku_bp.route('/update', methods=['POST'])
def update():
    grid = [['' for _ in range(9)] for _ in range(9)]  # Recreate the grid
    values = []
    error = None

    try:
        # Parse input values
        for i in range(9):
            for j in range(9):
                cell_value = request.form.get(f'cell-{i}-{j}', '').strip()
                if cell_value and cell_value.isdigit() and 1 <= int(cell_value) <= 9:
                    grid[i][j] = int(cell_value)
                    values.append((i, j))
                else:
                    grid[i][j] = 0

        # Check if the grid is valid before attempting to solve
        if not is_valid_sudoku(grid):
            # Convert zeros back to empty strings for display
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        grid[i][j] = ''

            return render_template('sudoku_index.html',
                                   grid=grid,
                                   error="The puzzle has conflicts. Please check your inputs.")

        # Create a copy of the grid for solving
        grid_copy = [row[:] for row in grid]

        # Set a time limit for solving (in seconds)
        start_time = time.time()
        max_solve_time = 3  # Maximum 3 seconds to solve

        # Try to solve with a call that has a timeout mechanism
        solve_result = solve(grid_copy)

        # Check if we've hit the time limit
        if time.time() - start_time > max_solve_time or not solve_result:
            # Convert zeros back to empty strings for display
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        grid[i][j] = ''

            return render_template('sudoku_index.html',
                                   grid=grid,
                                   error="This puzzle appears to be unsolvable. Please check your inputs.")

        # If we got here, the puzzle was solved successfully
        return render_template('sudoku_update.html', grid=grid_copy, values=values)

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error solving Sudoku: {str(e)}")

        # Convert zeros back to empty strings for display (if grid exists)
        try:
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        grid[i][j] = ''
        except:
            grid = [['' for _ in range(9)] for _ in range(9)]

        return render_template('sudoku_index.html',
                               grid=grid,
                               error=f"An error occurred while solving: {str(e)}")


@sudoku_bp.route('/solve_grid', methods=['POST'])
def solve_grid():
    return redirect(url_for('sudoku.sudoku_solver'))