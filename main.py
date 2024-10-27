from flask import Flask, jsonify, request, render_template
from tictactoe import TicTacToe  # Importing TicTacToe class
from agent import MDPAgent        # Importing MDPAgent class

app = Flask(__name__)

# Initialize the game and the AI agent
game = TicTacToe()
agent = MDPAgent()

@app.route('/')
def index():
    return render_template('index.html', board=game.board, current_player=game.current_player)

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    position = data['position']

    # Make the move for the human player
    if game.make_move(position):
        # AI's turn
        if game.current_player == 'O':
            position = agent.choose_action(game.board)
            game.make_move(position)

    winner = game.check_winner()
    is_draw = game.is_draw()

    return jsonify({
        'board': game.board,
        'winner': winner,
        'draw': is_draw,
        'next_player': game.current_player  # Send the next player
    })

@app.route('/reset', methods=['POST'])
def reset():
    game.reset()
    return jsonify({
        'board': game.board
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
