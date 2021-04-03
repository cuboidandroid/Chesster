
def bishop(x, y, board):
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


def rook(x, y, board):
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


def queen(x, y, board):
    return bishop(x, y, board) | rook(x, y, board)


def knight(x, y, board):
    return {(x+i, y+j) for i, j in zip([1, 2, -1, -2, 1, 2, -1, -2], [2, 1, 2, 1, -2, -1, -2, -1])
            if (0 <= x + i < 8) and (0 <= y + j < 8) and (board[x+i, y+j]) * board[x, y] <= 0}
# if inside the board and square is not occupied by same colored piece


def king(x, y, board):
    return {(x + i, y + j) for i, j in zip([-1, 0, 1, -1, 0, 1, -1, 0, 1], [-1, -1, -1, 0, 0, 0, 1, 1, 1])
            if (0 <= x + i < 8) and (0 <= y + j < 8) and (board[x+i, y+j]) * board[x, y] <= 0}


def wpawn(x, y, board):
    out = set()

# start move and normal move

    if board[x-1, y] == 0 and (x-1 > 0):
        out.add((x - 1, y))
        if x == 6 and board[x-2, y] == 0:
            out.add((x - 2, y))

# capture

    if (x-1 > 0) and (y+1 <= 7):
        if (board[x-1, y+1]) * board[x, y] < 0:
            out.add((x-1, y+1))

    if (x-1 > 0) and (y-1 >= 0):
        if (board[x-1, y-1]) * board[x, y] < 0:
            out.add((x-1, y-1))

# en passant

# promotion

    if y == 1:
        pass
    return out


def bpawn(x, y, board):
    out = set()

    # start move and normal move

    if board[x + 1, y] == 0 and (x+1 < 7):
        out.add((x + 1, y))
        if x == 1 and board[x + 2, y] == 0:
            out.add((x + 2, y))

    # capture

    if (x+1 < 7) and (y+1 <= 7):
        if (board[x + 1, y + 1]) * board[x, y] < 0:
            out.add((x + 1, y + 1))

    if (x+1 < 7) and (y-1 >= 0):
        if (board[x + 1, y - 1]) * board[x, y] < 0:
            out.add((x + 1, y - 1))

    # en passant

    # promotion

    if y == 1:
        pass
    return out
