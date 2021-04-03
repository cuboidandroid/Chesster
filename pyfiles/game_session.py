import numpy as np
from pyfiles.board_and_pieces import *


class GameSession:

    def __init__(self):
        self.board = self.startup_board()
        self.white_can_castle_long = True
        self.white_can_castle_short = True
        self.black_can_castle_long = True
        self.black_can_castle_short = True
        self.white_to_move = True
        self.highlighted = []
        self.notation = []
        self.history = []

    @staticmethod
    def startup_board():
        board = np.zeros((8, 8)).astype(int)
        board[7][:] = [50, 30, 32, 90, 99, 32, 30, 50]
        board[6][:] = [10, 10, 10, 10, 10, 10, 10, 10]
        board[0][:] = -board[7][:]
        board[1][:] = -board[6][:]
        return board

    def is_on_a_move(self, field):
        if self.board[field] > 0 and self.white_to_move:
            return True
        elif self.board[field] < 0 and not self.white_to_move:
            return True
        else:
            return False

    def validate_move(self, move):
        conditions = list()

        # who is on the move

        conditions.append(self.is_on_a_move(move.from_sq))

        # check available moves for piece

        if (move.to_sq[0], move.to_sq[1]) in self.get_options((move.from_sq[0], move.from_sq[1])):
            conditions.append(True)
        else:
            conditions.append(False)

        return all(conditions)

    def get_options(self, field):

        if abs(self.board[field]) == 30:
            opt = knight(field[0], field[1], self.board)
        elif abs(self.board[field]) == 32:
            opt = bishop(field[0], field[1], self.board)
        elif abs(self.board[field]) == 90:
            opt = queen(field[0], field[1], self.board)
        elif abs(self.board[field]) == 50:
            opt = rook(field[0], field[1], self.board)
        elif self.board[field] == 10:
            opt = wpawn(field[0], field[1], self.board)
        elif self.board[field] == -10:
            opt = bpawn(field[0], field[1], self.board)
        elif abs(self.board[field]) == 99:
            opt = king(field[0], field[1])

        else:
            opt = set()
        return opt

    def make_move(self, move):
        if self.validate_move(move):
            self.board[move.from_sq] = 0
            self.board[move.to_sq] = move.moved_piece
            self.history.append(move)
            self.update_notation(move)
            self.white_to_move = not self.white_to_move

    def update_notation(self, move):
        if move:
            self.notation.append(move.generate_move_notation())
        else:
            self.notation.pop()

    def undo_move(self):
        if self.history:
            self.update_notation(None)

            last_move = self.history.pop()
            self.board[last_move.to_sq] = last_move.destination_field
            self.board[last_move.from_sq] = last_move.moved_piece
            self.white_to_move = not self.white_to_move
        else:
            pass

    @staticmethod
    def piece_name(n):
        d = {
            0: "--",
            -10: "bp",
            10: "wp",
            -30: "bN",
            30: "wN",
            -32: "bB",
            32: "wB",
            -50: "bR",
            50: "wR",
            -90: "bQ",
            90: "wQ",
            -99: "bK",
            99: "wK"
        }
        return d[n]


class Move:

    def __init__(self, from_sq, to_sq, board):
        self.from_sq = from_sq
        self.to_sq = to_sq

        self.moved_piece = board[from_sq]
        self.destination_field = board[to_sq]

    def generate_move_notation(self):
        files = 'abcdefgh'
        # st_row = 7 - self.from_sq[0]+1
        # st_col = files[self.from_sq[1]]

        to_row = 7 - self.to_sq[0]+1
        to_col = files[self.to_sq[1]]

        return GameSession.piece_name(self.moved_piece)[1:] + ' ' + str(to_col) + str(to_row)
