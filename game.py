import pygame
import os
import time

from board import Board


# resources -------------------------------------------------
from flowingconfig import *
raw_board = pygame.image.load("res/images/eq_chessboard.png")
icon = pygame.image.load("res/images/icon.png")
board = pygame.transform.scale(raw_board, (width - margin_abs, height - margin_abs))
# -----------------------------------------------------------


def redraw_gamewindow(win, bo, p1time, p2time, statewhite, stateblack):
    pygame.font.init()
    pygame.draw.rect(win, (0, 0, 0), (0, 0, width, width))
    win.blit(board, (margin_abs_half, margin_abs_half))
    bo.draw(win)
    font = pygame.font.SysFont("console", 17)
    font2 = pygame.font.SysFont("console", 25)
    f1time = str(p1time//60)+":"+str(p1time%60)
    f2time = str(p2time//60)+":"+str(p2time%60)
    if p1time % 60 < 10:
        f1time = str(p1time // 60) + ":" + "0" + str(p1time % 60)
    elif p1time % 60 == 0:
        f1time += "0"
    if p2time % 60 < 10:
        f2time = str(p2time // 60) + ":" + "0" + str(p2time % 60)
    elif p2time % 60 == 0:
        f2time += "0"
    txttime1 = font.render("Player 1 Time: " + str(f1time), True, (255, 255, 255), (0, 0, 0))
    txttime2 = font.render("Player 2 Time: " + str(f2time), True, (255, 255, 255), (0, 0, 0))
    if statewhite == 1:
        txtstate1 = font2.render("White King is under check!", True, (255, 255, 255), (0, 0, 0))
    else:
        txtstate1 = font2.render("White King is under check!", True, (0, 0, 0), (0, 0, 0))
    if stateblack == 1:
        txtstate2 = font2.render("Black King is under check!", True, (255, 255, 255), (0, 0, 0))
    else:
        txtstate2 = font2.render("Black King is under check!", True, (0, 0, 0), (0, 0, 0))
    win.blit(txttime1, (width - margin_abs_half - txttime1.get_width(), width - margin_abs_half + txttime1.get_height()))
    win.blit(txttime2, (margin_abs_half, margin_abs_half - txttime2.get_height()*2))
    win.blit(txtstate1, (margin_abs_half, width - margin_abs_half / 1.5))
    win.blit(txtstate2, (width - margin_abs_half - txtstate2.get_width(), margin_abs_half - txtstate2.get_height()*1.5))
    pygame.display.update()


def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("console", 40)
    txt = font.render(text, True, (255, 0, 0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT+1, 3000)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT + 1:
                run = False


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
    statewhite = 0
    stateblack = 0
    while run:
        clock.tick(fps_max)
        if turn == "w":
            p1time -= (time.time() - wide_timer)
        else:
            p2time -= (time.time() - wide_timer)
        wide_timer = time.time()
        redraw_gamewindow(win, bo, int(p1time), int(p2time), statewhite, stateblack)
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
                    change = bo.select(i, j, turn)
                    bo.update_moves()
                    if change:
                        wide_timer = time.time()
                        if turn == "w":
                            if bo.is_checked("w") and statewhite == 1:
                                end_screen(win, "Black Wins!")
                            if bo.is_checked("b") and stateblack == 1:
                                end_screen(win, "White Wins!")
                            turn = "b"
                        else:
                            if bo.is_checked("b") and stateblack == 1:
                                end_screen(win, "White Wins!")
                            if bo.is_checked("w") and statewhite == 1:
                                end_screen(win, "Black Wins!")
                            turn = "w"

                if bo.is_checked("w"):
                    print("log: White check")
                    statewhite = 1
                else:
                    statewhite = 0
                if bo.is_checked("b"):
                    print("log: Black check")
                    stateblack = 1
                else:
                    stateblack = 0


win = pygame.display.set_mode((width, height), vsync=True)
pygame.display.set_caption("PyChess")
pygame.display.set_icon(icon)
main()
