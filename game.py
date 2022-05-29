# python libraries ------------------------------------------
import sys
import pygame
import time

# project libraries -----------------------------------------
from board import Board
from algorithm import Solution

# resources -------------------------------------------------
from flowingconfig import *
raw_board = pygame.image.load("res/images/eq_chessboard.png")
icon = pygame.image.load("res/images/icon.png")
board = pygame.transform.scale(raw_board, (width - padding_absolute, height - padding_absolute))


# functions -------------------------------------------------
def redraw_gamewindow(bo, player1_time, player2_time, state_white, state_black):
    pygame.font.init()
    pygame.draw.rect(win, (0, 0, 0), (0, 0, width, width))
    font = pygame.font.SysFont("console", 17)
    font2 = pygame.font.SysFont("console", 25)
    win.blit(board, (padding_abs_half, padding_abs_half))
    bo.draw(win)
    f1time = str(player1_time // 60) + ":" + str(player1_time % 60)
    f2time = str(player2_time // 60) + ":" + str(player2_time % 60)
    if player1_time % 60 < 10:
        f1time = str(player1_time // 60) + ":" + "0" + str(player1_time % 60)
    elif player1_time % 60 == 0:
        f1time += "0"
    if player2_time % 60 < 10:
        f2time = str(player2_time // 60) + ":" + "0" + str(player2_time % 60)
    elif player2_time % 60 == 0:
        f2time += "0"
    txttime1 = font.render("Player 1 Time: " + str(f1time), True, (255, 255, 255), (0, 0, 0))
    txttime2 = font.render("Player 2 Time: " + str(f2time), True, (255, 255, 255), (0, 0, 0))
    if state_white == 1:
        txtstate1 = font2.render("White King is under check!", True, (255, 255, 255), (0, 0, 0))
    else:
        txtstate1 = font2.render("White King is under check!", True, (0, 0, 0), (0, 0, 0))
    if state_black == 1:
        txtstate2 = font2.render("Black King is under check!", True, (255, 255, 255), (0, 0, 0))
    else:
        txtstate2 = font2.render("Black King is under check!", True, (0, 0, 0), (0, 0, 0))
    win.blit(txttime1, (width - padding_abs_half - txttime1.get_width(),
                        width - padding_abs_half + txttime1.get_height()))
    win.blit(txttime2, (padding_abs_half, padding_abs_half - txttime2.get_height() * 2))
    win.blit(txtstate1, (padding_abs_half, width - padding_abs_half / 1.5))
    win.blit(txtstate2, (width - padding_abs_half - txtstate2.get_width(),
                         padding_abs_half - txtstate2.get_height() * 1.5))
    pygame.display.update()


def end_screen(text, total_time):
    pygame.font.init()
    total_time = int(total_time)
    ftime = str(total_time // 60) + ":" + str(total_time % 60)
    if total_time % 60 < 10:
        ftime = str(total_time // 60) + ":" + "0" + str(total_time % 60)
    elif total_time % 60 == 0:
        ftime += "0"
    font = pygame.font.SysFont("arial", 70, bold=True)
    font2 = pygame.font.SysFont("arial", 35, bold=True)
    font3 = pygame.font.SysFont("arial", 20, bold=True)
    txt = font.render(text, True, (255, 0, 0))
    txttime = font2.render(ftime, True, (255, 0, 0))
    txthelp = font3.render("Press q - to quit and r - to restart", True, (255, 255, 255))
    pygame.draw.rect(win, (0, 0, 0), (-1, width / 2 - txt.get_height(), width + 1, width - width/1.3))
    win.blit(txt, (width / 2 - txt.get_width() / 2, width / 2 - txt.get_height()))
    win.blit(txttime, (width / 2 - txttime.get_width() / 2, width / 2))
    win.blit(txthelp, (width / 2 - txthelp.get_width() / 2, width / 2 + txttime.get_height()*1.2))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    run = False
                    sys.exit()
                if event.key == pygame.K_r:
                    main()


def start_screen():
    pygame.font.init()
    font4 = pygame.font.SysFont("arial", 30, bold=True)
    font5 = pygame.font.SysFont("arial", 40, bold=True)
    txt0 = font5.render("Hotkeys", True, (255, 0, 0))
    txt1 = font4.render("q - to quit", True, (255, 255, 255))
    txt2 = font4.render("s - to surrender", True, (255, 255, 255))
    txt3 = font4.render("p - to vote for draw", True, (255, 255, 255))
    pygame.draw.rect(win, (0, 0, 0), (-1, -1, width + 1, width + 1))
    win.blit(txt0, ((width - txt0.get_width()) / 2, width * 0.3))
    win.blit(txt1, (width * 0.4, width * 0.4))
    win.blit(txt2, (width * 0.4, width * 0.45))
    if game_mode != 1:
        win.blit(txt3, (width * 0.4, width * 0.5))
    pygame.time.set_timer(pygame.USEREVENT + 1, freeze_time * 1000 + 1)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
            if event.type == pygame.USEREVENT + 1:
                run = False


def click(pos):
    x = pos[0]
    y = pos[1]
    if top_left_corner[0] < x < top_left_corner[0] + bottom_right_corner[0]:
        if top_left_corner[1] < y < top_left_corner[1] + bottom_right_corner[1]:
            divx = x - top_left_corner[0]
            divy = y - top_left_corner[0]
            i = int(divx / (bottom_right_corner[0] / 8))
            j = int(divy / (bottom_right_corner[1] / 8))
            return i, j


# main ------------------------------------------------------
def main():
    player1_time = time_restriction_seconds
    player2_time = time_restriction_seconds
    wide_timer = time.time()
    start_time = time.time()
    turn = "w"
    bo = Board(8, 8)
    bo.update_moves()
    clock = pygame.time.Clock()
    run = True
    statewhite = 0
    stateblack = 0
    white_wants_draw = 0
    black_wants_draw = 0
    while run:
        clock.tick(fps_max)
        if turn == "w":
            player1_time -= (time.time() - wide_timer)
            if player1_time <= 0:
                end_screen("Black Wins!", time.time() - start_time)
        else:
            player2_time -= (time.time() - wide_timer)
            if player2_time <= 0:
                end_screen("White Wins!", time.time() - start_time)
        wide_timer = time.time()
        redraw_gamewindow(bo, int(player1_time), int(player2_time), statewhite, stateblack)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    run = False
                    sys.exit()
                if event.key == pygame.K_s:
                    if turn == "w":
                        end_screen("Black Wins!", time.time() - start_time)
                    else:
                        end_screen("White Wins!", time.time() - start_time)
                if event.key == pygame.K_p:
                    if turn == "w" and white_wants_draw == 0:
                        white_wants_draw = 1
                    elif turn == "w" and white_wants_draw == 1:
                        white_wants_draw = 0
                    if turn == "b" and black_wants_draw == 0:
                        black_wants_draw = 1
                    elif turn == "b" and black_wants_draw == 1:
                        black_wants_draw = 0
                    if black_wants_draw and white_wants_draw:
                        end_screen("Draw!", time.time() - start_time)
            if turn == "b" and game_mode == 1:
                change = False
                bo.update_moves()
                solve = Solution(bo)
                try:
                    (piecex, piecey), choice = solve.random_choice(turn)
                    if difficulty == 1:
                        (piecex, piecey), choice = solve.tier3_choice()
                    elif difficulty == 2:
                        (piecex, piecey), choice = solve.tier2_choice()
                    elif difficulty == 3:
                        pass
                    bo.simple_move((piecex, piecey), (choice[1], choice[0]), "b")
                    change = True
                except TypeError:
                    print("type")
                    end_screen("White Wins!", time.time() - start_time)
                if change:
                    wide_timer = time.time()
                    bo.reset_selected()
                    if bo.is_checked("b") and stateblack == 1:
                        end_screen("White Wins!", time.time() - start_time)
                    if bo.is_checked("w") and statewhite == 1:
                        end_screen("Black Wins!", time.time() - start_time)
                    turn = "w"
                if bo.is_checked("b"):
                    stateblack = 1
                else:
                    stateblack = 0
                if bo.is_checked("b"):
                    stateblack = 1
                else:
                    stateblack = 0
            elif (turn == "w" and game_mode == 1) or game_mode == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    bo.update_moves()
                    if padding_abs_half < pos[0] < width - padding_abs_half \
                            and padding_abs_half < pos[1] < width - padding_abs_half:
                        i, j = click(pos)
                        try:
                            change = bo.select(i, j, turn)
                            bo.update_moves()
                        except AttributeError:
                            change = False
                        if change:
                            wide_timer = time.time()
                            if turn == "w":
                                bo.reset_selected()
                                if bo.is_checked("w") and statewhite == 1:
                                    end_screen("Black Wins!", time.time() - start_time)
                                if bo.is_checked("b") and stateblack == 1:
                                    end_screen("White Wins!", time.time() - start_time)
                                turn = "b"
                            else:
                                bo.reset_selected()
                                if bo.is_checked("b") and stateblack == 1:
                                    end_screen("White Wins!", time.time() - start_time)
                                if bo.is_checked("w") and statewhite == 1:
                                    end_screen("Black Wins!", time.time() - start_time)
                                turn = "w"
                    if bo.is_checked("w"):
                        statewhite = 1
                    else:
                        statewhite = 0
                    if bo.is_checked("b"):
                        stateblack = 1
                    else:
                        stateblack = 0


win = pygame.display.set_mode((width, height), vsync=True)
pygame.display.set_caption("PyChess")
pygame.display.set_icon(icon)
start_screen()
main()
