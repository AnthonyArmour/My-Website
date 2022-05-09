from flask import render_template, Flask, request, jsonify, Blueprint
import numpy as np
from .backend.TicTacToe import TicTacToe, Node, MCTS


def get_root_node(games=30):
    nd = Node()

    for i in range(games):
        game = TicTacToe()
        cpu = MCTS(nd, iterations=200)

        while len(game.moves()) > 0:
            move = cpu.act()
            cpu.feed(move)

            if game.make_move(move):
                break
    return nd

views = Blueprint('views', __name__)

# class App():
# app = Flask(__name__)

data = np.arange(9)
node = get_root_node()
agents = {}
board = np.arange(9).reshape(3, 3)
games = {}


@views.route('/')
def home():
    return render_template("index.html")

@views.route('/create_agent')
def create_agent():
    uid = str(np.random.randint(9999))
    agents[uid] = MCTS(node, iterations=200)
    games[uid] = TicTacToe()
    # print("Created id: ", uid)
    return jsonify({"data": uid})

@views.route('/delete_agent/<uid>', methods=['GET','POST'])
def delete_agent(uid):
    try:
        del agents[uid]
        del games[uid]
    except:
        pass
    # print("Deleted: ", uid)
    return jsonify({"data": "success"})

@views.route('/player_move/<mv>/<uid>', methods=['GET','POST'])
def player_mv(mv, uid):
    move = board[int(mv[-2])][int(mv[-1])]
    games[uid].make_move(move)
    agents[uid].feed(move)

    # print("player mv: {} - id: {}".format(move, uid))
    return jsonify({"data": "Success"})

@views.route('/cpu_move/<uid>', methods=['GET','POST'])
def cpu_mv(uid):
    move = agents[uid].act()
    agents[uid].feed(move)
    games[uid].make_move(move)
    # print("cpu mv: {} - id: {}".format(move, uid))

    move = np.argwhere(board == move)[0]
    move = str(move[0]) + str(move[1])
    return jsonify({"data": move})

# @views.route('/site_views')
# def my_views():
#     return "\nTotal site views: ".format(site_views)

# @views.route('/game_plays')
# def games_played():
#     return "\nTotal games played: ".format(plays)