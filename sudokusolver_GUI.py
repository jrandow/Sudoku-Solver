import pandas as pd
import numpy as np
import random
import copy
import sys
import time
import GUI

# ----------------- insert the sudoku puzzle ----------------- #

# puzzleToSolve =  [[5, 3, 0, 0, 7, 0, 0, 0, 0],
#                   [6, 0, 0, 1, 9, 5, 0, 0, 0],
#                   [0, 9, 8, 0, 0, 0, 0, 6, 0],
#                   [8, 0, 0, 0, 6, 0, 0, 0, 3],
#                   [4, 0, 0, 8, 0, 3, 0, 0, 1],
#                   [7, 0, 0, 0, 2, 0, 0, 0, 6],
#                   [0, 6, 0, 0, 0, 0, 2, 8, 0],
#                   [0, 0, 0, 4, 1, 9, 0, 0, 5],
#                   [0, 0, 0, 0, 8, 0, 0, 7, 9]]

puzzleToSolve =  [[8,4,0,0,0,5,0,0,7],
                  [6,3,0,4,2,0,0,0,0],
                  [0,0,5,0,0,6,0,0,0],
                  [0,0,0,0,0,0,9,5,3],
                  [0,0,0,0,4,0,0,0,0],
                  [1,8,6,0,0,0,0,0,0],
                  [0,0,0,9,0,0,8,0,0],
                  [0,0,0,0,6,3,0,9,2],
                  [9,0,0,8,0,0,0,4,6]]



# ----------------- end of user interaction ----------------- #


def draw(list_label, puzzle):
    puzzle_list = puzzle[0] + puzzle[1] + puzzle[2] + puzzle[3] + puzzle[4] + puzzle[5] + puzzle[6] + puzzle[7] + puzzle[8]
    for i, label in enumerate(list_label):
        label.setText(str(puzzle_list[i]))



def fillBoard(puzzle):
    rows = puzzle

    cols = []
    for i in range(len(puzzle)):
        col = []
        for val in puzzle:
            col.append(val[i])
        cols.append(col)
    
    block1 = []
    block2 = []
    block3 = []
    block4 = []
    block5 = []
    block6 = []
    block7 = []
    block8 = []
    block9 = []
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            if row < 3 and col < 3:
                block1.append(puzzle[row][col])
            elif row < 3 and 2 < col < 6:
                block2.append(puzzle[row][col])
            elif row < 3 and col > 5:
                block3.append(puzzle[row][col])
            elif 2 < row < 6 and col < 3:
                block4.append(puzzle[row][col])
            elif 2 < row < 6 and 2 < col < 6:
                block5.append(puzzle[row][col])
            elif 2 < row < 6 and col > 5:
                block6.append(puzzle[row][col])
            elif row > 5 and col < 3:
                block7.append(puzzle[row][col])
            elif row > 5 and 2 < col < 6:
                block8.append(puzzle[row][col])
            elif row > 5 and col > 5:
                block9.append(puzzle[row][col])
        
    blocks = list([block1,block2,block3,block4,block5,block6,block7,block8,block9]) 

    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            if puzzle[row][col] == 0:
                numbers, amount = possibleNumbers(puzzle,row,col,rows,cols,blocks)
                if amount == 1:
                    puzzle[row][col] = numbers[0]
                    return puzzle
    
    #if no single possible number is found
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            if puzzle[row][col] == 0:
                numbers, amount = possibleNumbers(puzzle,row,col,rows,cols,blocks)
                try:
                    puzzle[row][col] = random.choice(numbers)
                    return puzzle
                except IndexError:
                    return puzzleToSolve


def possibleNumbers(puzzle,row,col,rows,cols,blocks):
    numbers = []
    matching_row = rows[row]
    matching_col = cols[col]

    if row < 3 and col < 3:
        matching_block = blocks[0]
    elif row < 3 and 2 < col < 6:
        matching_block = blocks[1]
    elif row < 3 and col > 5:
        matching_block = blocks[2]
    elif 2 < row < 6 and col < 3:
        matching_block = blocks[3]
    elif 2 < row < 6 and 2 < col < 6:
        matching_block = blocks[4]
    elif 2 < row < 6 and col > 5:
        matching_block = blocks[5]
    elif row > 5 and col < 3:
        matching_block = blocks[6]
    elif row > 5 and 2 < col < 6:
        matching_block = blocks[7]
    else:
        matching_block = blocks[8]

    for nr in range(1,10):
        if nr not in matching_row and nr not in matching_col and nr not in matching_block:
            numbers.append(nr)
            
    amount = len(numbers)

    return numbers, amount


def countZeros(puzzle):
    counter = 0
    for i in puzzle:
        counter += i.count(0)
    return counter


def solveSudoku(list_label, puzzle):
    iterations = 0
    while True:
        draw(list_label, puzzle)
        # app.exec_() funktioniert nicht, soll aber
        #time.sleep(1) # to see what happens
        freeSpaces = countZeros(puzzle)
        #print("There are", freeSpaces, "free spaces left.")

        if freeSpaces == 0:
            print("The Sudoku has been solved!")
            print("It took", iterations, "iterations.")
            break

        puzzle = copy.deepcopy(fillBoard(puzzle))
        iterations += 1

#solveSudoku(list(map(list, puzzleToSolve)))

if __name__ == "__main__":
    app = GUI.QtWidgets.QApplication(sys.argv)
    MainWindow = GUI.QtWidgets.QMainWindow()
    ui = GUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())