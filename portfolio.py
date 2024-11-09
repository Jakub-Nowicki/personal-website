from sudoku_solver import display_board, solve, find_empty, valid
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

grid = [['' for _ in range(9)] for _ in range(9)]

@app.route('/sudoku')
def sudoku_solver():
    values = []
    grid = [['' for _ in range(9)] for _ in range(9)]
    return render_template('sudoku_index.html', grid=grid, values=values)

@app.route('/update', methods=['POST'])
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

@app.route('/solve_grid', methods =['POST'])
def solve_grid():
    return redirect(url_for('sudoku_solver'))
