# app.py
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for session

def check_winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

@app.route('/')
def index():
    if 'board' not in session:
        session['board'] = [[' ' for _ in range(3)] for _ in range(3)]
        session['current_player'] = 'X'
    return render_template('index.html', board=session['board'], current_player=session['current_player'])

@app.route('/play/<int:row>/<int:col>')
def play(row, col):
    if session['board'][row][col] == ' ':
        session['board'][row][col] = session['current_player']
        winner = check_winner(session['board'])
        if winner:
            session['winner'] = winner
        elif all(cell != ' ' for row in session['board'] for cell in row):
            session['winner'] = 'Tie'
        else:
            session['current_player'] = 'O' if session['current_player'] == 'X' else 'X'
    session.modified = True
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.pop('board', None)
    session.pop('current_player', None)
    session.pop('winner', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
