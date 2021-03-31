import pygame as p
from pyfiles import game_session

width = height = 512
dimension = 8
sq_size = height // dimension
max_fps = 15
images = {}


def load_images():
    pieces = ['bB', 'bK', 'bQ', 'bN', 'bp', 'bR', 'wB', 'wK', 'wQ', 'wN', 'wp', 'wR']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock
    screen.fill(p.Color("white"))
    gs = game_session.GameSession()
    load_images()
    running = True
    sq_selected = ()  # last click of a user
    player_clicks = []  # sq selected and destination sq
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // sq_size
                row = location[1] // sq_size
                if sq_selected == (row, col):  # twice clicked same square
                    sq_selected = ()  # deselect
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    pass

        draw_game(screen, gs)
        # clock.tick(max_fps)
        p.display.flip()


def draw_game(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


def draw_pieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = piece_name(board[r, c])
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


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


if __name__ == '__main__':
    main()
