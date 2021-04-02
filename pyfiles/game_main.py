import pygame as p
from pyfiles.game_session import *

width = height = 640
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
    # clock = p.time.Clock
    screen.fill(p.Color("white"))
    gs = GameSession()
    load_images()
    running = True
    sq_selected = ()  # last click of a user
    player_clicks = []  # sq selected and destination sq
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                print('\n\nNICE GAME:\n\n')
                [print(move) for move in gs.notation]

            elif e.type == p.MOUSEBUTTONDOWN:
                l_click, m_click, r_click = p.mouse.get_pressed(3)
                if l_click:
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
                        move = Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.generate_move_notation())
                        gs.make_move(move)
                        sq_selected = ()  # deselect
                        player_clicks = []

                elif r_click:
                    sq_selected = ()  # deselect
                    player_clicks = []
                    gs.undo_move()

        draw_game(screen, gs, player_clicks)
        # clock.tick(max_fps)
        p.display.flip()


def draw_game(screen, gs, fields):
    draw_board(screen)
    draw_selected(screen, fields)
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
            piece = GameSession.piece_name(board[r, c])
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


def draw_selected(screen, fields):
    for field in fields:
        p.draw.rect(screen, p.Color(242, 153, 244), p.Rect(field[1] * sq_size, field[0] * sq_size, sq_size, sq_size))


if __name__ == '__main__':
    main()
