import pygame
import os
import time

from board import Board


# resources -------------------------------------------------
from flowingconfig import *
pygame.font.init()
raw_board = pygame.image.load("res/images/eq_chessboard.png")
# -----------------------------------------------------------

board = pygame.transform.scale(raw_board, (width - margin_abs, height - margin_abs))


def redraw_gamewindow(win, bo, p1time, p2time):
    win.blit(board, (margin_abs_half, margin_abs_half))
    bo.draw(win)
    font = pygame.font.SysFont("console", 20)
    f1time = str(p1time//60)+":"+str(p1time%60)
    f2time = str(p2time//60)+":"+str(p2time%60)
    if p1time % 60 == 0: f1time += "0"
    elif p1time < 10: f1time = str(p1time//60) + ":" + "0" + str(p1time%60)
    if p2time % 60 == 0: f2time += "0"
    elif p2time < 10: f2time = str(p2time//60) + ":" + "0" + str(p2time%60)
    txttime1 = font.render("Player 1 Time: " + str(f1time), True, (255, 255, 255), (0, 0, 0))
    txttime2 = font.render("Player 2 Time: " + str(f2time), True, (255, 255, 255), (0, 0, 0))
    win.blit(txttime1, (20, 700))
    win.blit(txttime2, (20, 20))
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
    p1time = player_time
    p2time = player_time
    wide_timer = time.time()
    turn = "w"
    bo = Board(8, 8)
    bo.update_moves()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps_max)
        time_gone = int(time.time() - wide_timer)
        if turn == "w":
            p1time -= (time.time() - wide_timer)
        else:
            p2time -= (time.time() - wide_timer)
        wide_timer = time.time()
        redraw_gamewindow(win, bo, int(p1time), int(p2time))
        for event in pygame.event.get():
            timer = time.time() - wide_timer
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                bo.update_moves()
                if margin_abs_half < pos[0] < width - margin_abs_half and margin_abs_half < pos[1] < width - margin_abs_half:
                    i, j = click(pos)
                    change = bo.select(i, j, turn)
                    bo.update_moves()
                    if change:
                        wide_timer = time.time()
                        if turn == "w":
                            turn = "b"
                        else:
                            turn = "w"
            if bo.is_checked("w"):
                print("White check")
            if bo.is_checked("b"):
                print("Black check")


win = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyChess")
main()
