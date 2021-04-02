import numpy as np


class GameSession:

    def __init__(self):
        self.board = self.startup_board()
        self.white_can_castle_long = True
        self.white_can_castle_short = True
        self.black_can_castle_long = True
        self.black_can_castle_short = True
        self.white_to_move = True
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

    def validate_move(self, move):
        conditions = []

        # who is on the move

        if self.white_to_move and move.moved_piece > 0:
            conditions.append(True)
        elif not self.white_to_move and move.moved_piece < 0:
            conditions.append(True)
        else:
            conditions.append(False)

        return all(conditions)

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
