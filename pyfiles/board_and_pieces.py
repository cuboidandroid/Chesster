import numpy as np


def setup_board():
    board = np.zeros((8, 8)).astype(int)
    board[7][:] = [50, 30, 32, 90, 99, 32, 30, 50]
    board[6][:] = [10, 10, 10, 10, 10, 10, 10, 10]
    board[0][:] = -board[7][:]
    board[1][:] = -board[6][:]
    return board


def setup_position():
    board = np.array([[00, -50, 00, 00, 00, -50, -99, 00],
                      [00, 00, 00, 00, 00, -10, -10, -10],
                      [-10, 00, 00, 00, 00, 00, 00, 00],
                      [00, 00, 00, 00, 00, 00, 00, 00],
                      [00, 00, 00, 00, 00, 00, 00, 00],
                      [00, 00, 00, 00, 10, 00, 00, 90],
                      [00, 00, 00, 00, 00, 00, 10, 10],
                      [00, 50, 00, 00, 00, 50, 32, 99]
                      ])
    return board


def bishop(x, y, board=setup_board()):
    scope = set()
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    for d in directions:
        for n in range(1, 8):
            if (0 <= x+d[0]*n < 8) and (0 <= y+d[1]*n < 8) and (board[x+d[0]*n, y+d[1]*n] == 0):
                scope.add((x+d[0]*n, y+d[1]*n))

            elif (0 <= x+d[0]*n < 8) and (0 <= y+d[1]*n < 8) and (board[x+d[0]*n, y+d[1]*n] * board[x, y] > 0):
                break

            elif (0 <= x+d[0]*n < 8) and (0 <= y+d[1]*n < 8) and (board[x+d[0]*n, y+d[1]*n] * board[x, y] < 0):
                scope.add((x+d[0]*n, y+d[1]*n))
                break

    return scope


def rook(x, y, board=setup_board()):
    scope = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for d in directions:
        for n in range(1, 8):
            if (0 <= x + d[0] * n < 8) and (0 <= y + d[1] * n < 8) and (board[x + d[0] * n, y + d[1] * n] == 0):
                scope.add((x + d[0] * n, y + d[1] * n))

            elif (0 <= x + d[0] * n < 8) and (0 <= y + d[1] * n < 8) and (
                    board[x + d[0] * n, y + d[1] * n] * board[x, y] > 0):
                break

            elif (0 <= x + d[0] * n < 8) and (0 <= y + d[1] * n < 8) and (
                    board[x + d[0] * n, y + d[1] * n] * board[x, y] < 0):
                scope.add((x + d[0] * n, y + d[1] * n))
                break

    return scope

    # return {(x + n, y + n) for n in range(0, 8) if (n != 0) and (0 <= x + n < 8) and (0 <= y + n < 8)
    #         and (board(x + n, y + n) == 0) elif (board(x + n, y + n) * (board(x, y) > 0))} | \
    #        {(x + n, y + n) for n in range(-7, 0) if n != 0 and 0 <= x + n < 8 and 0 <= y + n < 8} | \
    #        {(x + n, y - n) for n in range(0, 8) if n != 0 and 0 <= x + n < 8 and 0 <= y - n < 8} | \
    #        {(x + n, y - n) for n in range(-7, 0) if n != 0 and 0 <= x + n < 8 and 0 <= y - n < 8}


# def rook(x, y):
#     return {(x + n, y) for n in range(-7, 8) if n != 0 and 0 <= x + n < 8} | \
#            {(x, y + n) for n in range(-7, 8) if n != 0 and 0 <= y + n < 8}


def queen(x, y, board=setup_board()):
    return bishop(x, y, board) | rook(x, y, board)


def knight(x, y):
    return {(x + i, y + j) for i, j in zip([1, 2, -1, -2, 1, 2, -1, -2], [2, 1, 2, 1, -2, -1, -2, -1])
            if 0 <= x + i < 8 and 0 <= y + j < 8}


def king(x, y):
    return {(x + i, y + j) for i, j in zip([-1, 0, 1, -1, 0, 1, -1, 0, 1], [-1, -1, -1, 0, 0, 0, 1, 1, 1])
            if 0 <= x + i < 8 and 0 <= y + j < 8}


def wpawn(x, y):
    out = set()
    if y > 1:
        out.add((x - 1, y))
        if x == 6:
            out.add((x - 2, y))
    if y == 1:  # promotion
        pass
    return out


def bpawn(x, y):
    out = set()
    if y < 6:
        out.add((x + 1, y))
        if x == 1:
            out.add((x + 2, y))
    if y == 6:  # promotion
        pass
    return out


def check_collisions(piece):
    return piece
