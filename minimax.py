import numpy as np
import sys
from board import Board

class Minimax():

    def __init__(self):
        self.board = Board()

    def _score(self, win, player):
        """Scoring function, determines the value of different states"""
        value = win.count(player)
        empties = win.count(0)
        if value == 4: 
            return 500
        elif value == 3 and empties == 1:
            return 10
        elif value == 2 and empties == 2:
            return 5
        return 0

    def eval(self, board, player):
        """Evaluates the postion for player p"""
        score = 0
        # Test rows
        for i in range(6):
            for j in range(4):
                score += self._score(list(board[i][j:j + 4]), player)
                score -= 2 * self._score(list(board[i][j:j + 4]), player * -1)

        # Test columns on transpose array
        reversed_board = [list(i) for i in zip(*board)]
        for i in range(7):
            for j in range(3):
                score += self._score(list(reversed_board[i][j:j + 4]), player)
                score -= 2 * self._score(list(reversed_board[i][j:j + 4]), player * -1)

        # Test diagonal
        for i in range(3):
            for j in range(4):
                l = []
                for k in range(4):
                    l.append(board[i + k][j + k])
                score += self._score(l, player)
                score -= 2 * self._score(l, player * -1)

        reversed_board = np.fliplr(board)
        # Test reverse diagonal
        for i in range(3):
            for j in range(4):
                l = []
                for k in range(4):
                    l.append(reversed_board[i + k][j + k])
                score += self._score(l, player)
                score -= 2 * self._score(l, player * -1)

        return score

    def minimax(self, board, player):
        """Returns the optimal move for player p in state board"""
        value, move = self.max_value(board, -sys.maxsize, sys.maxsize, 6, player)
        return move

    def max_value(self, board, alpha, beta, depth, player):
        # checking terminal states
        if depth == 0 or self.board.is_win_state(board) or len(self.board.available_moves(board)) == 0:
            return self.eval(board, player), None

        v = -sys.maxsize
        m = -10

        # going through available moves
        for move in self.board.available_moves(board):
            next_board, reward = self.board.drop_piece(board, move, player)
            v2, a2 = self.min_value(next_board, alpha, beta, depth - 1, player)
            if v2 > v:
                v = v2
                m = move
                alpha = max(alpha, v)
            if v >= beta:
                return v, m

        return v, m

    def min_value(self, board, alpha, beta, depth, player):
        # checking terminal states
        if depth == 0 or self.board.is_win_state(board) or len(self.board.available_moves(board)) == 0:
            return self.eval(board, player), None

        v = sys.maxsize
        m = -10

        for move in self.board.available_moves(board):
            next_board, reward = self.board.drop_piece(board, move, player * -1)
            v2, a2 = self.max_value(next_board, alpha, beta, depth - 1, player)
            if v2 < v:
                v = v2
                m = move
                beta = min(beta, v)
            if v <= alpha:
                return v, m

        return v, m

    def get_move(self, board):
        return self.minimax(board, 1)
