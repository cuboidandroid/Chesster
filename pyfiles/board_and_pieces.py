
def bishop(x, y, board):
    opt = set()
    scope = set()
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    for d in directions:
        for n in range(1, 8):
            if (0 <= x+d[0]*n < 8) and (0 <= y+d[1]*n < 8) and (board[x+d[0]*n, y+d[1]*n] == 0):
                opt.add((x+d[0]*n, y+d[1]*n))
                scope.add((x+d[0]*n, y+d[1]*n))

            elif (0 <= x+d[0]*n < 8) and (0 <= y+d[1]*n < 8) and (board[x+d[0]*n, y+d[1]*n] * board[x, y] > 0):
                scope.add((x+d[0]*n, y+d[1]*n))
                break

            elif (0 <= x+d[0]*n < 8) and (0 <= y+d[1]*n < 8) and (board[x+d[0]*n, y+d[1]*n] * board[x, y] < 0):
                opt.add((x+d[0]*n, y+d[1]*n))
                scope.add((x + d[0] * n, y + d[1] * n))
                break

    return opt, scope


def rook(x, y, board):
    opt = set()
    scope = set()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for d in directions:
        for n in range(1, 8):
            if (0 <= x + d[0] * n < 8) and (0 <= y + d[1] * n < 8) and (board[x + d[0] * n, y + d[1] * n] == 0):
                opt.add((x + d[0] * n, y + d[1] * n))
                scope.add((x + d[0] * n, y + d[1] * n))

            elif (0 <= x + d[0] * n < 8) and (0 <= y + d[1] * n < 8) and (
                    board[x + d[0] * n, y + d[1] * n] * board[x, y] > 0):
                scope.add((x + d[0] * n, y + d[1] * n))
                break

            elif (0 <= x + d[0] * n < 8) and (0 <= y + d[1] * n < 8) and (
                    board[x + d[0] * n, y + d[1] * n] * board[x, y] < 0):
                opt.add((x + d[0] * n, y + d[1] * n))
                scope.add((x + d[0] * n, y + d[1] * n))
                break

    return opt, scope


def queen(x, y, board):
    bishop_opt, bishop_scope = bishop(x, y, board)
    rook_opt, rook_scope = rook(x, y, board)
    return bishop_opt | rook_opt, bishop_scope | rook_scope


def knight(x, y, board):
    return {(x+i, y+j) for i, j in zip([1, 2, -1, -2, 1, 2, -1, -2], [2, 1, 2, 1, -2, -1, -2, -1])  # opt
            if (0 <= x + i < 8) and (0 <= y + j < 8) and (board[x+i, y+j]) * board[x, y] <= 0}, \
           {(x+i, y+j) for i, j in zip([1, 2, -1, -2, 1, 2, -1, -2], [2, 1, 2, 1, -2, -1, -2, -1])  # scope
            if (0 <= x + i < 8) and (0 <= y + j < 8)}
# if inside the board and square is not occupied by same colored piece


def king(x, y, board, history):
    return {(x + i, y + j) for i, j in zip([-1, 0, 1, -1, 1, -1, 0, 1], [-1, -1, -1, 0, 0, 1, 1, 1])  # opt
            if (0 <= x + i < 8) and (0 <= y + j < 8) and (board[x + i, y + j]) * board[x, y] <= 0}, \
           {(x + i, y + j) for i, j in zip([-1, 0, 1, -1, 1, -1, 0, 1], [-1, -1, -1, 0, 0, 1, 1, 1])  # scope
            if (0 <= x + i < 8) and (0 <= y + j < 8)}


def wpawn(x, y, board, history):
    out = set()
    enp = set()
    prom = set()
    scope = set()

# start move and normal move

    if board[x-1, y] == 0 and (x-1 > 0):
        out.add((x - 1, y))
        if x == 6 and board[x-2, y] == 0:
            out.add((x - 2, y))

# capture

    if (x-1 > 0) and (y+1 <= 7):
        scope.add((x - 1, y + 1))
        if (board[x-1, y+1]) * board[x, y] < 0:
            out.add((x-1, y+1))

    if (x-1 > 0) and (y-1 >= 0):
        scope.add((x - 1, y - 1))
        if (board[x-1, y-1]) * board[x, y] < 0:
            out.add((x-1, y-1))

# en passant
    if x == 3:
        if history:
            last_move = history[-1]
            if (abs(last_move.moved_piece) == 10) and \
               (abs(last_move.to_sq[0] - last_move.from_sq[0]) == 2):

                if last_move.from_sq[1] == y+1:
                    enp.add((x-1, y+1))

                elif last_move.from_sq[1] == y-1:
                    enp.add((x-1, y-1))


# promotion

    if x == 1:
        if board[0, y] == 0:
            prom.add((0, y))  # normal move forward

        if y + 1 <= 7:
            scope.add((0, y + 1))
            if (board[0, y + 1]) * board[x, y] < 0:
                prom.add((0, y + 1))

        if y - 1 >= 0:
            scope.add((0, y - 1))
            if (board[0, y - 1]) * board[x, y] < 0:
                prom.add((0, y - 1))

    return out, enp, prom, scope


def bpawn(x, y, board, history):
    out = set()
    enp = set()
    prom = set()
    scope = set()

    # start move and normal move

    if board[x + 1, y] == 0 and (x+1 < 7):
        out.add((x + 1, y))
        if x == 1 and board[x + 2, y] == 0:
            out.add((x + 2, y))

    # capture

    if (x+1 < 7) and (y+1 <= 7):
        scope.add((x + 1, y + 1))
        if (board[x + 1, y + 1]) * board[x, y] < 0:
            out.add((x + 1, y + 1))

    if (x+1 < 7) and (y-1 >= 0):
        scope.add((x + 1, y - 1))
        if (board[x + 1, y - 1]) * board[x, y] < 0:
            out.add((x + 1, y - 1))

    # en passant
    if x == 4:
        if history:
            last_move = history[-1]
            if (abs(last_move.moved_piece) == 10) and \
               (abs(last_move.to_sq[0] - last_move.from_sq[0]) == 2):

                if last_move.from_sq[1] == y+1:
                    enp.add((x+1, y+1))

                elif last_move.from_sq[1] == y-1:
                    enp.add((x+1, y-1))

    # promotion

    if x == 6:
        if board[7, y] == 0:
            prom.add((7, y))  # normal move forward

        if y + 1 <= 7:
            scope.add((7, y + 1))
            if (board[7, y + 1]) * board[x, y] < 0:
                prom.add((7, y + 1))

        if y - 1 >= 0:
            scope.add((7, y - 1))
            if (board[7, y - 1]) * board[x, y] < 0:
                prom.add((7, y - 1))

    return out, enp, prom, scope
