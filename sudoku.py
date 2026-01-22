import random

#function to set difficulty level based on input
def set_difficulty(difficulty):
    switch = {
        "easy": 0.7,
        "medium": 0.5,
        "hard": 0.3
    }
    return switch.get(difficulty, 0.3)

#function to check if placing a number is valid
def is_valid(board, row, col, num):
    #check row and column for duplicates
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    #check 3x3 subgrid for duplicates
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

#function to solve sudoku using backtracking
def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                #shuffle numbers to add randomness
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        #backtrack if solution not found
                        board[row][col] = 0
                return False
    return True

#function to generate a complete sudoku board
def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    return board
