#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import copy
import time

ROW = "ABCDEFGHI"
COL = "123456789"

dictcoord = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8,
    "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8
}

# Use some extra memory to hard-code the rows, columns, and squares of each
# cell, rather than redundantly perform the list manipulation to create these

rows = [
    {0,1,2,3,4,5,6,7,8},          # 0
    {9,10,11,12,13,14,15,16,17},  # 1
    {18,19,20,21,22,23,24,25,26}, # 2
    {27,28,29,30,31,32,33,34,35}, # 3
    {36,37,38,39,40,41,42,43,44}, # 4
    {45,46,47,48,49,50,51,52,53}, # 5
    {54,55,56,57,58,59,60,61,62}, # 6
    {63,64,65,66,67,68,69,70,71}, # 7
    {72,73,74,75,76,77,78,79,80}  # 8
]

columns = [
    {0,9,18,27,36,45,54,63,72},   # 0
    {1,10,19,28,37,46,55,64,73},  # 1
    {2,11,20,29,38,47,56,65,74},  # 2
    {3,12,21,30,39,48,57,66,75},  # 3
    {4,13,22,31,40,49,58,67,76},  # 4
    {5,14,23,32,41,50,59,68,77},  # 5
    {6,15,24,33,42,51,60,69,78},  # 6
    {7,16,25,34,43,52,61,70,79},  # 7
    {8,17,26,35,44,53,62,71,80},  # 8
]

# There doesn't seem to be a simple way to calculate the square of a cell, so
# instead also keep this hash
square = {
     0:0,  1:0,  2:0,  3:1,  4:1,  5:1,  6:2,  7:2,  8:2,
     9:0, 10:0, 11:0, 12:1, 13:1, 14:1, 15:2, 16:2, 17:2,
    18:0, 19:0, 20:0, 21:1, 22:1, 23:1, 24:2, 25:2, 26:2,
    27:3, 28:3, 29:3, 30:4, 31:4, 32:4, 33:5, 34:5, 35:5,
    36:3, 37:3, 38:3, 39:4, 40:4, 41:4, 42:5, 43:5, 44:5,
    45:3, 46:3, 47:3, 48:4, 49:4, 50:4, 51:5, 52:5, 53:5,
    54:6, 55:6, 56:6, 57:7, 58:7, 59:7, 60:8, 61:8, 62:8,
    63:6, 64:6, 65:6, 66:7, 67:7, 68:7, 69:8, 70:8, 71:8,
    72:6, 73:6, 74:6, 75:7, 76:7, 77:7, 78:8, 79:8, 80:8
#
#    0:0,  1:0,  2:0,  9:0, 10:0, 11:0, 18:0, 19:0, 20:0,
#    3:1,  4:1,  5:1, 12:1, 13:1, 14:1, 21:1, 22:1, 23:1,
#    6:2,  7:2,  8:2, 15:2, 16:2, 17:2, 24:2, 25:2, 26:2,
#   27:3, 28:3, 29:3, 36:3, 37:3, 38:3, 45:3, 46:3, 47:3,
#   30:4, 31:4, 32:4, 39:4, 40:4, 41:4, 48:4, 49:4, 50:4,
#   33:5, 34:5, 35:5, 42:5, 43:5, 44:5, 51:5, 52:5, 53:5,
#   54:6, 55:6, 56:6, 63:6, 64:6, 65:6, 72:6, 73:6, 74:6,
#   57:7, 58:7, 59:7, 66:7, 67:7, 68:7, 75:7, 76:7, 77:7,
#   60:8, 61:8, 62:8, 69:8, 70:8, 71:8, 78:8, 79:8, 80:8
}

squares = [
    {0,1,2,9,10,11,18,19,20},     # 0 (top-left)
    {3,4,5,12,13,14,21,22,23},    # 1 (top-center)
    {6,7,8,15,16,17,24,25,26},    # 2 (top-right)
    {27,28,29,36,37,38,45,46,47}, # 3 (center-left)
    {30,31,32,39,40,41,48,49,50}, # 4 (center)
    {33,34,35,42,43,44,51,52,53}, # 5 (center-right)
    {54,55,56,63,64,65,72,73,74}, # 6 (bottom-left)
    {57,58,59,66,67,68,75,76,77}, # 7 (bottom-center)
    {60,61,62,69,70,71,78,79,80}  # 8 (bottom-right)
]


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def backtracking(board):
    """Takes a board and returns solved board."""

    # Store a board state as a table of 81 entries, where each entry is set of
    # some integers {1, 2, ..., 9}, representing the possible remaining values
    # at the square row i//9, column i%9 (row r, column c is at entry (r*9)+c)
    
    init_board = [set()] * 81
    initisgoal = True
    
    for i in ROW:
        for j in COL:
            if board[i+j] == 0:
                init_board[(dictcoord[i] * 9) + dictcoord[j]] = \
                    {1, 2, 3, 4, 5, 6, 7, 8, 9}
                initisgoal = False
            else:
                init_board[(dictcoord[i] * 9) + dictcoord[j]] = board[i+j]
    
    if initisgoal: return board
    
    # Perform initial full constraint propagation for each index noted
    for i in range(81):
        if type(init_board[i]) is int:
            forwardcheck(init_board, init_board[i], constrains(i))
    
    fin_board = rbacktrack(init_board)
    # rbacktrack() performs the DFS by recursion
    assert fin_board is not None, "No solution was found for input"
    for i in fin_board:
        assert type(i) is int, "Solution was returned incomplete"
    
    solved_board = dict()
    for i in ROW:
        for j in COL:
            solved_board[i+j] = fin_board[(dictcoord[i]*9)+dictcoord[j]]
    
    return solved_board

def rbacktrack(board):
    """Recursive function to backtrack search a board through its sub-boards"""
    
    if isgoal(board):
        return board
    
    while boardisopen(board):
        
        index = findmrv(board)
        assert index is not None, \
            "No MRV index found on a believed-solvable board"
        value = board[index].pop()          
        
        sboard = copy.deepcopy(board)
        sboard[index] = value
        forwardcheck(sboard, value, constrains(index))
        
        sback = rbacktrack(sboard)
        if sback is not None:
            return sback
    
    return None

def constrains(i):
    """Given an index i on the board, return a set of all cells in the
       row, column, or square of i"""
    x = rows[i//9] | columns[i%9] | squares[square[i]]
    return x

def forwardcheck(board, val, constrains):
    """Remove value val from any set in the indeces constrains of the board"""
    for i in constrains:
        if type(board[i]) is set:
            board[i].discard(val)

def findmrv(board):
    """Gets the first index of the smallest possible set in this list"""
    for s in range(1,10):
        for i in range(81):
            if type(board[i]) is set:
                if len(board[i]) == s:
                    return i
    return None

def boardisopen(board):
    """Return False if any cell of this board is the empty set, else True."""
    for i in board:
        if type(i) is set:
            if not bool(i):
                return False
    return True

def isgoal(board):
    """Return True if all cells of this board are ints, else False."""
    for i in board:
        if type(i) is not int:
            return False
    return True

# TODO delete
def printmyboard(board):
    print("===")
    for i in range(9):
        print(' '.join(map(str, board[i*9:(i+1)*9])))
    print("===")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")