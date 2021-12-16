import pandas as pd
import numpy as np
from typing import Optional, List
import random
import copy
import sys
import time


class Sudoku():
    def __init__(self, puzzle: Optional[List[int]] = None, list_label = None) -> None: # TODO: Optional on list_label
        self.puzzle = puzzle
        self.list_label = list_label
        self.do_save_puzzle = True
        #self.default_puzzle = list(map(list, puzzle))
        #self.puzzle_save = [] #this list will contain a structured set of save states, which can be refered, TODO: work with this


    def draw(self):
        puzzle_list = self.puzzle[0] + self.puzzle[1] + self.puzzle[2] + self.puzzle[3] + self.puzzle[4] + self.puzzle[5] + self.puzzle[6] + self.puzzle[7] + self.puzzle[8]
        for i, label in enumerate(self.list_label):
            label.setText(str(puzzle_list[i]))


    def fillBoard(self):
        rows = self.puzzle
        cols = []
        for i in range(len(self.puzzle)):
            col = []
            for val in self.puzzle:
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
        for row in range(len(self.puzzle)):
            for col in range(len(self.puzzle)):
                if row < 3 and col < 3:
                    block1.append(self.puzzle[row][col])
                elif row < 3 and 2 < col < 6:
                    block2.append(self.puzzle[row][col])
                elif row < 3 and col > 5:
                    block3.append(self.puzzle[row][col])
                elif 2 < row < 6 and col < 3:
                    block4.append(self.puzzle[row][col])
                elif 2 < row < 6 and 2 < col < 6:
                    block5.append(self.puzzle[row][col])
                elif 2 < row < 6 and col > 5:
                    block6.append(self.puzzle[row][col])
                elif row > 5 and col < 3:
                    block7.append(self.puzzle[row][col])
                elif row > 5 and 2 < col < 6:
                    block8.append(self.puzzle[row][col])
                elif row > 5 and col > 5:
                    block9.append(self.puzzle[row][col])
            
        blocks = list([block1,block2,block3,block4,block5,block6,block7,block8,block9]) 

        # if there is a single possbible number: update the puzzle and SAVE this state
        for row in range(len(self.puzzle)):
            for col in range(len(self.puzzle)):
                if self.puzzle[row][col] == 0:
                    numbers = self.possibleNumbers(row,col,rows,cols,blocks)
                    if len(numbers) == 1:
                        self.puzzle[row][col] = numbers[0]
                        # self.puzzle_save.append(self.puzzle)
                        return
        
        #if no single possible number is found: iterate through puzzle, find spot with least possible numbers and get on from the possbile numbers
        #TODO: when this work, integrate it into the above for loop
        for n in range(2,10):   #iterate through the amount (n) of possible numbers, !when integrating this onto above maybe start this iteration at 1
            for row in range(len(self.puzzle)):
                for col in range(len(self.puzzle)):
                    if self.puzzle[row][col] == 0:
                        numbers = self.possibleNumbers(row,col,rows,cols,blocks)
                        if len(numbers) == n:
                            if self.do_save_puzzle:
                                self.puzzle_save = list(map(list, self.puzzle))
                                self.do_save_puzzle = False
                            self.puzzle[row][col] = random.choice(numbers)
                            return
                            # try:
                            #     self.puzzle[row][col] = random.choice(numbers)
                            #     return
                            # except IndexError:                  #IndexError occurs when numbers is empty meaning there is no possible number meaning there was an error
                            #     self.puzzle = list(map(list, self.default_puzzle)) # maybe want to increase this number if we get back ?
                            #     return
                        #if len(numbers) == 0:
                            #self.puzzle = list(map(list, self.puzzle_save))
        self.puzzle = list(map(list, self.puzzle_save))
        include guessedNumbers(row,col,randomchoice(numbers)) # save guessed numbers which did not work and don't use them again (guessed numbers for each)
        # or include it in the possibleNumbers function


        # for row in range(len(self.puzzle)):
        #     for col in range(len(self.puzzle)):
        #         if self.puzzle[row][col] == 0:
        #             numbers, amount = self.possibleNumbers(row,col,rows,cols,blocks)
        #             try:
        #                 self.puzzle[row][col] = random.choice(numbers)
        #             except IndexError:                  #IndexError occurs when numbers is empty meaning there is no possible number meaning there was an error
        #                 self.puzzle = self.default_puzzle 


    def possibleNumbers(self,row,col,rows,cols,blocks):
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
                
        return numbers


    def countZeros(self):
        counter = 0
        for i in self.puzzle:
            counter += i.count(0)
        return counter


    def solveSudoku(self):
        iterations = 0
        while True:
            self.draw()
            #time.sleep(1) # to see what happens
            freeSpaces = self.countZeros()
            #print("There are", freeSpaces, "free spaces left.")

            if freeSpaces == 0:
                print("The Sudoku has been solved!")
                print("It took", iterations, "iterations.")
                break

            if iterations == 10000:
                print("It took", iterations, "iterations.")
                print("The Sudoku could not be solved. Try again with another one.")
                break

            self.fillBoard() #TODO: change to self.puzzle ?
            iterations += 1