import numpy as np
from game_main import piece_name


class GameSession:

    def __init__(self):
        self.board = self.startup_board()
        self.white_can_castle_long = True
        self.white_can_castle_short = True
        self.black_can_castle_long = True
        self.black_can_castle_short = True
        self.white_to_move = True

    @staticmethod
    def startup_board():
        board = np.zeros((8, 8)).astype(int)
        board[7][:] = [50, 30, 32, 90, 99, 32, 30, 50]
        board[6][:] = [10, 10, 10, 10, 10, 10, 10, 10]
        board[0][:] = -board[7][:]
        board[1][:] = -board[6][:]
        return board

    class Move:

        def __init__(self, from_sq, to_sq, board):
            self.from_sq = from_sq
            self.to_sq = to_sq

            self.moved_piece = piece_name(board[from_sq])
            self.destination_field = piece_name(board[to_sq])

        def chess_note(self, from_sq, to_sq, moved_piece):
            files = 'abcdefgh'
            st_row = 7 - from_sq[0]+1
            st_col = files[from_sq[1]]

            to_row = 7 - to_sq[0]+1
            to_col = files[to_sq[1]]

            return moved_piece + " : " + str(st_col) + str(st_row) + " - " + str(to_col) + str(to_row)
