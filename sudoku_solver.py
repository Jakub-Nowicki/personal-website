from flask import Flask, render_template, redirect, url_for, request

def display_board(bo): #function to display board on the screen
    for i in range(len(bo)):

        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - -')

        for j in range(len(bo[0])):

            if j % 3 == 0 and j !=0: 
                print(' | ', end='')

            if j == 8:
                print(bo[i][j])
            else:
                print(bo[i][j], end=' ')


def solve(bo):

    find = find_empty(bo) 

    if not find: # we check if it is the end of the sudoku, and if there is something more to solve
        return True
    else:
        row, col = find

    for i in range(1,10):
    
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            display_board(bo)
            if solve(bo):
                return True  # true if the number might be right
            
            bo[row][col] = 0 # if the number is not right we gonna change it to the 0 and try with other previous one

    return False # we gonna return false if any of the numbers is correct in this currect positon so we have to backtrack

def find_empty(bo): # finding where the 0 is 
    for i in  range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j) # we are returning row and column
    return None
            

def valid(bo, num, pos): #checking if the number is valid 

    for i in range(len(bo[0])): #checking row
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
        
    for i in range(len(bo)): #checking col
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
        
    row = pos[0] // 3 # if it is 2nd box the row will be 1 and so on
    column = pos[1] // 3

    #checking inside the box
    for i in range(row*3, row*3 + 3): #iterating between rows we start at the beginning for example 2nd 
        #box will be 1 * 3 starting from 3rd iteration so 4th positions and ending at 5th iteraton so 6th posistion
        for j in range(column*3, column*3 + 3): # same thing here but with the columns
            if bo[i][j] == num and (i, j) != pos:
                return False
    
    return True







