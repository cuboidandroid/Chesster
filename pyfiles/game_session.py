import numpy as np


class GameSession:

    def __init__(self):
        self.board = self.startup_board()
        self.white_can_castle_long = True
        self.white_can_castle_short = True
        self.black_can_castle_long = True
        self.black_can_castle_short = True

    @staticmethod
    def startup_board():
        board = np.zeros((8, 8)).astype(int)
        board[7][:] = [50, 30, 32, 90, 99, 32, 30, 50]
        board[6][:] = [10, 10, 10, 10, 10, 10, 10, 10]
        board[0][:] = -board[7][:]
        board[1][:] = -board[6][:]
        return board
