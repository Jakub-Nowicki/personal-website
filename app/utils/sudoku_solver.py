from flask import Flask, render_template, redirect, url_for, request

# Make sure all these functions are properly exported

def display_board(bo):  # function to display board on the screen
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - -')

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(' | ', end='')

            if j == 8:
                print(bo[i][j])
            else:
                print(bo[i][j], end=' ')


def solve(bo, max_attempts=1000000):
    """
    Solves a Sudoku puzzle using backtracking with a limit on attempts
    to prevent infinite loops on unsolvable puzzles.

    Args:
        bo: The Sudoku board
        max_attempts: Maximum number of attempts before giving up

    Returns:
        bool: True if solved, False if unsolvable
    """
    attempts = 0

    def backtrack():
        nonlocal attempts

        # Check if we've tried too many times
        attempts += 1
        if attempts > max_attempts:
            return False

        find = find_empty(bo)
        if not find:  # we check if it is the end of the sudoku
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(bo, i, (row, col)):
                bo[row][col] = i

                if backtrack():
                    return True

                bo[row][col] = 0  # backtrack

        return False

    return backtrack()


def find_empty(bo):  # finding where the 0 is
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # we are returning row and column
    return None


def valid(bo, num, pos):  # checking if the number is valid
    for i in range(len(bo[0])):  # checking row
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):  # checking col
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    row = pos[0] // 3  # if it is 2nd box the row will be 1 and so on
    column = pos[1] // 3

    # checking inside the box
    for i in range(row * 3, row * 3 + 3):  # iterating between rows we start at the beginning for example 2nd
        # box will be 1 * 3 starting from 3rd iteration so 4th positions and ending at 5th iteraton so 6th posistion
        for j in range(column * 3, column * 3 + 3):  # same thing here but with the columns
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def is_valid_sudoku(board):
    """
    Validates if a Sudoku board is valid based on the rules of Sudoku

    Args:
        board: The Sudoku board to validate

    Returns:
        bool: True if valid, False if invalid
    """
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