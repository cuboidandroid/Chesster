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
        self.enp = set()
        self.prom = set()
        self.scope = set()

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

        opt, enp, prom, scope = self.get_options((move.from_sq[0], move.from_sq[1]))
        if (move.to_sq[0], move.to_sq[1]) in opt:
            conditions.append(True)
        elif (move.to_sq[0], move.to_sq[1]) in enp:
            conditions.append(True)
            self.enp = enp
        elif (move.to_sq[0], move.to_sq[1]) in prom:
            conditions.append(True)
            self.prom = prom
        else:
            conditions.append(False)

        return all(conditions)

    def get_options(self, field):
        opt = set()
        enp = set()
        prom = set()
        scope = set()

        if abs(self.board[field]) == 30:
            opt, scope = knight(field[0], field[1], self.board)
        elif abs(self.board[field]) == 32:
            opt, scope = bishop(field[0], field[1], self.board)
        elif abs(self.board[field]) == 90:
            opt, scope = queen(field[0], field[1], self.board)
        elif abs(self.board[field]) == 50:
            opt, scope = rook(field[0], field[1], self.board)
        elif self.board[field] == 10:
            opt, enp, prom, scope = wpawn(field[0], field[1], self.board, self.history)
        elif self.board[field] == -10:
            opt, enp, prom, scope = bpawn(field[0], field[1], self.board, self.history)
        elif abs(self.board[field]) == 99:
            opt, scope = king(field[0], field[1], self.board, self.history)

        return opt, enp, prom, scope

    def all_attacked_squares(self, sign):
        attacked = set()
        for i in np.ndindex(8, 8):
            if self.board[i] * sign > 0:  # the same sign
                opt, _, _, scope = self.get_options(i)
                attacked.update(scope)
                # print(self.board[i], {self.translate_square(f) for f in scope})
        return attacked

    def make_move(self, move):
        if self.validate_move(move):
            if move.to_sq in self.enp:
                self.board[move.from_sq] = 0
                self.board[move.to_sq] = move.moved_piece

                if self.white_to_move:
                    self.board[(move.to_sq[0]+1, move.to_sq[1])] = 0  # en passant take with white
                else:
                    self.board[(move.to_sq[0]-1, move.to_sq[1])] = 0   # en passant take with black

                self.history.append(move)
                self.update_notation(move)
                self.white_to_move = not self.white_to_move
            elif move.to_sq in self.prom:

                self.board[move.from_sq] = 0
                if self.white_to_move:
                    self.board[move.to_sq] = move.promo_input
                else:
                    self.board[move.to_sq] = - move.promo_input
                self.history.append(move)
                self.update_notation(move)
                self.white_to_move = not self.white_to_move
            else:

                self.board[move.from_sq] = 0
                self.board[move.to_sq] = move.moved_piece
                self.history.append(move)
                self.update_notation(move)
                self.white_to_move = not self.white_to_move

        self.enp = set()
        self.prom = set()

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
    def translate_square(cords):
        files = 'abcdefgh'
        ranks = '12345678'
        return files[cords[1]] + ranks[::-1][cords[0]]

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

    def __init__(self, from_sq, to_sq, board, promo_input):
        self.from_sq = from_sq
        self.to_sq = to_sq

        self.label = ''
        self.moved_piece = board[from_sq]
        self.destination_field = board[to_sq]
        self.promo_input = promo_input

    def generate_move_notation(self):
        files = 'abcdefgh'
        # st_row = 7 - self.from_sq[0]+1
        # st_col = files[self.from_sq[1]]

        to_row = 7 - self.to_sq[0]+1
        to_col = files[self.to_sq[1]]

        return GameSession.piece_name(self.moved_piece)[1:] + ' ' + str(to_col) + str(to_row)
