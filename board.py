import numpy as np

class Board:
    def drop_piece(self, board, move, player):
        """Drops a piece on the board and checks if game is over"""
        next_board = board.copy()
        for index in list(reversed(range(6))):
            if next_board[index][move] == 0:
                next_board[index][move] = player
                break

        reward = 0
        # someone won
        if self.is_win_state(next_board):
            reward = player
        # it's a draw
        elif np.count_nonzero(next_board[0]) == 7:
            reward = 0.5

        return next_board, reward 

    def is_valid_move(self, move, board):
        """Checks if move is valid"""
        return board[0][move] == 0

    def available_moves(self, board):
        """Get available moves in position board"""
        return [i for i in range(7) if self.is_valid_move(i, board)]

    def is_win_state(self, board):
        """Determines if board is in a winning state"""
        # Test rows
        for i in range(6):
            for j in range(4):
                value = sum(board[i][j:j + 4])
                if abs(value) == 4:
                    return True

        # Test columns on transpose array
        reversed_board = [list(i) for i in zip(*board)]
        for i in range(7):
            for j in range(3):
                value = sum(reversed_board[i][j:j + 4])
                if abs(value) == 4:
                    return True

        # Test diagonal
        for i in range(3):
            for j in range(4):
                value = 0
                for k in range(4):
                    value += board[i + k][j + k]
                    if abs(value) == 4:
                        return True

        reversed_board = np.fliplr(board)
        # Test reverse diagonal
        for i in range(3):
            for j in range(4):
                value = 0
                for k in range(4):
                    value += reversed_board[i + k][j + k]
                    if abs(value) == 4:
                        return True
        return False
