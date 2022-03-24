import numpy as np
import random
from time import sleep


class Node():
  def __init__(self, parent=False):
    self.leaf = True
    self.terminal = False
    self.parent = parent
    self.lock = False

  def expand(self, moves):
    m = len(moves)
    if m == 0:
      self.terminal = True
    else:
      # Cumulative reward
      self.S = np.zeros(m)

      # History of plays
      self.T = np.full(m, 0.001)

      self.moves = moves

      self.children = [Node(self) for a in range(m)]
      self.leaf = False

  def update(self, idx, score):
    while self.lock:
      sleep(0.01)
    self.lock = True
    self.S[idx]+=score
    self.T[idx]+=1
    self.lock = False

  def choose(self):
    idx = np.argmax(self.S / self.T + np.sqrt(2.0 / self.T * np.log(1 + self.T.sum())))
    return idx


class MCTS():
  def __init__(self, root_node, iterations=5000):
    self.game = TicTacToe()
    self.iterations = iterations
    self.node = root_node

  def act(self):
    move = self.search() 
    return move

  def feed(self, move):
    self.game.make_move(move)
    pos = np.argwhere(self.node.moves == move)[0][0]
    self.node = self.node.children[pos]

  def search(self):
    for t in range(self.iterations):
      self.mcts(self.node)

    idx = np.argmax(self.node.T)
    move = self.node.moves[idx]

    return move


  def mcts(self, node):
    # if leaf node, expand it
    if node.leaf:
      node.expand(self.game.moves())
      rollout = True
    else:
      rollout = False

    if node.terminal:
      return 0

    # choose a move 
    idx = node.choose()
    move = node.moves[idx]
    if self.game.make_move(move):
      val = 1
    elif rollout:
      val = -self.rollout()
    else:
      val = -self.mcts(node.children[idx])
    self.game.unmake_move()

    node.update(idx, val)
    return val

  def rollout(self):
    moves = self.game.moves()
    if len(moves) == 0:
      return 0
    move = random.choice(moves)
    if self.game.make_move(move):
      val = 1
    else:
      val = -self.rollout()
    self.game.unmake_move()
    return val


red = blue = lambda x: str(x)


class TicTacToe():

    ROWS = 3
    COLS = 3

    def __init__(self):
        self.board = np.zeros((self.COLS, self.ROWS), dtype = 'i')
        self.turn = 1 
        self.hist = []

    
    def check_win(self, turn):
        diag1 = np.diag(self.board) == turn
        diag2 = np.diag(np.fliplr(self.board)) == turn

        if False not in diag1:
            return True
        if False not in diag2:
            return True

        for i in range(3):
            if False not in (self.board[i, :] == turn):
                return True
            if False not in (self.board[:, i] == turn):
                return True

        return False
        
    def make_move(self, x):

        self.hist.append(x)
        self.board.reshape(9,)[x] = self.turn
        status = self.check_win(self.turn)
        self.turn*=-1
        return status

    def unmake_move(self):
        self.board.reshape(9,)[self.hist.pop(-1)] = 0
        self.turn*=-1

    def moves(self):
        return np.argwhere(self.board.reshape(9,)==0).flatten()

    def show(self):
        print("Player one: ●           Player two: △")
        for x in range(self.ROWS):
            print('|', end = '')
            for y in range(self.COLS):
                if self.board[x, y] == 1:
                    print(red('●') + '|', end = '')
                elif self.board[x, y] == -1:
                    print(blue('△') + '|', end = '')
                else:
                    print(' |', end = '')
            print('')