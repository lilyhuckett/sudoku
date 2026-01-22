from flask import Flask, render_template, request, redirect, url_for, jsonify
from sudoku import generate_sudoku, set_difficulty
import random

app = Flask(__name__)

#game state
full_board = generate_sudoku()
difficulty = "medium"
probability = set_difficulty(difficulty)
blank_board = [
     [full_board[i][j] if random.random() < probability else 0 for j in range(9)]
     for i in range(9)
]

@app.route('/', methods=['GET'])
def index():
     #render the main sudoku page with the current board and difficulty
     return render_template('sudoku.html', board=blank_board, difficulty=difficulty, enumerate=enumerate, message='', show_solution=False)

@app.route('/set_difficulty/<level>')
def set_difficulty_route(level):
     #update the difficulty level and regenerate the board
     global difficulty, probability, full_board, blank_board
     difficulty = level
     probability = set_difficulty(difficulty)
     full_board = generate_sudoku()
     blank_board = [
          [full_board[i][j] if random.random() < probability else 0 for j in range(9)]
          for i in range(9)
     ]
     return redirect(url_for('index'))

@app.route('/reset',methods=['GET'])
def reset():
     #reset the board to a new puzzle with the same difficulty
     global full_board, blank_board, probability
     full_board = generate_sudoku()
     blank_board = [
          [full_board[i][j] if random.random() < probability else 0 for j in range(9)]
          for i in range(9)
     ]
     return redirect(url_for('index'))

@app.route('/complete', methods=['POST'])
def complete():
     #check if the user's solution is correct
     global full_board, blank_board
     user_board = [[0]*9 for _ in range(9)]
     is_correct = True

     for i in range(9):
          for j in range(9):
               val = request.form.get(f'cell_{i}_{j}')
               if val and val.isdigit():
                    user_val = int(val)
                    user_board[i][j] = user_val
                    if user_val != full_board[i][j]:
                         is_correct = False
               else:
                    user_board[i][j] = 0
                    is_correct = False

     if is_correct:
          #generate a new puzzle if the solution is correct
          message = "Correct! A new puzzle has been loaded."
          full_board_new = generate_sudoku()
          blank_board_new = [
               [full_board_new[i][j] if random.random() < probability else 0 for j in range(9)]
               for i in range(9)
          ]
          #update global state
          full_board = full_board_new
          blank_board = blank_board_new
          return render_template('sudoku.html', board=blank_board, difficulty=difficulty, enumerate=enumerate, message=message, show_solution=False)
     else:
          #return the user's board with an error message if incorrect
          message = "Incorrect. Please try again!"
          return render_template('sudoku.html', board=user_board, difficulty=difficulty, enumerate=enumerate, message=message, show_solution=False)

@app.route('/give_up')
def give_up():
     #show the solution to the current puzzle
     global full_board
     return render_template('sudoku.html', board=full_board, difficulty=difficulty, enumerate=enumerate, message="Here's the solution 💡 (You gave up!)", show_solution=True)
