import pygame
import os

from board import Board


# resources -------------------------------------------------
from flowingconfig import *
raw_board = pygame.image.load("res/images/eq_chessboard.png")
# -----------------------------------------------------------

board = pygame.transform.scale(raw_board, (width - margin_abs, height - margin_abs))


def redraw_gamewindow():
    global win, bo
    win.blit(board, (margin_abs_half, margin_abs_half))
    bo.draw(win)
    pygame.display.update()


def click(pos):
    x = pos[0]
    y = pos[1]
    if top_left_corner[0] < x < top_left_corner[0] + bot_right_corner[0]:
        if top_left_corner[1] < y < top_left_corner[1] + bot_right_corner[1]:
            divx = x - top_left_corner[0]
            divy = y - top_left_corner[0]
            i = int(divx / (bot_right_corner[0] / 8))
            j = int(divy / (bot_right_corner[1] / 8))
            return i, j


def main():
    global bo
    bo = Board(8, 8)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(24)
        redraw_gamewindow()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                bo.update_moves()
                if margin_abs_half < pos[0] < width - margin_abs_half and margin_abs_half < pos[1] < width - margin_abs_half:
                    i, j = click(pos)
                    bo.select(i, j)
                    bo.update_moves()



win = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyChess")
main()
