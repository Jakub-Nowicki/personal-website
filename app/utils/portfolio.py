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

        # Check if the puzzle is solvable
        if not is_valid_sudoku(grid):
            error = "The puzzle has conflicts. Please check your inputs."

            # Convert zeros back to empty strings for display
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        grid[i][j] = ''

            return render_template('sudoku_index.html', grid=grid, error=error)

        # Create a copy of the grid for solving
        grid_copy = [row[:] for row in grid]

        # Try to solve the puzzle
        if solve(grid_copy):
            return render_template('sudoku_update.html', grid=grid_copy, values=values)
        else:
            # Convert zeros back to empty strings for display
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        grid[i][j] = ''
            error = "This puzzle cannot be solved. Please check your inputs."
            return render_template('sudoku_index.html', grid=grid, error=error)

    except Exception as e:
        # Handle any unexpected errors
        error = f"An error occurred: {str(e)}"
        return render_template('sudoku_index.html', grid=[['' for _ in range(9)] for _ in range(9)], error=error)


@app.route('/solve_grid', methods=['POST'])
def solve_grid():
    return redirect(url_for('sudoku_solver'))


# Helper function to validate the initial Sudoku state
def is_valid_sudoku(board):
    # Check rows
    for row in board:
        seen = set()
        for cell in row:
            if cell != 0 and cell in seen:
                return False
            if cell != 0:
                seen.add(cell)

    # Check columns
    for col in range(9):
        seen = set()
        for row in range(9):
            cell = board[row][col]
            if cell != 0 and cell in seen:
                return False
            if cell != 0:
                seen.add(cell)

    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    cell = board[box_row + i][box_col + j]
                    if cell != 0 and cell in seen:
                        return False
                    if cell != 0:
                        seen.add(cell)

    return True