# game.py
# python libraries =====================================================================================================
import sys
import pygame
import time

# project libraries ====================================================================================================
from board import Board
from algorithm import Solution

# resources ============================================================================================================
from flowingconfig import *
raw_board = pygame.image.load("res/images/eq_chessboard.png")
icon = pygame.image.load("res/images/icon.png")
if visual_set != 0:
    try:
        raw_board = pygame.image.load("res/images/"+str(visual_set)+"/eq_chessboard.png")
    except FileNotFoundError or FileExistsError:
        print("log: custom visual set cannot be loaded")
board = pygame.transform.smoothscale(raw_board, (width - padding_absolute, height - padding_absolute))


# functions ============================================================================================================
def redraw_gamewindow(board_to_render, player1_time, player2_time, state_white, state_black):
    pygame.draw.rect(win, (0, 0, 0), (0, 0, width, width))
    win.blit(board, (padding_abs_half, padding_abs_half))
    board_to_render.draw(win)
    pygame.font.init()
    font_1 = pygame.font.SysFont("console", 17)
    font_2 = pygame.font.SysFont("console", 25)
    format_time_p1 = str(player1_time // 60) + ":" + str(player1_time % 60)
    format_time_p2 = str(player2_time // 60) + ":" + str(player2_time % 60)
    if player1_time % 60 < 10:
        format_time_p1 = str(player1_time // 60) + ":" + "0" + str(player1_time % 60)
    elif player1_time % 60 == 0:
        format_time_p1 += "0"
    if player2_time % 60 < 10:
        format_time_p2 = str(player2_time // 60) + ":" + "0" + str(player2_time % 60)
    elif player2_time % 60 == 0:
        format_time_p2 += "0"
    text_time1 = font_1.render("Player 1 Time: " + str(format_time_p1), True, (255, 255, 255), (0, 0, 0))
    text_time2 = font_1.render("Player 2 Time: " + str(format_time_p2), True, (255, 255, 255), (0, 0, 0))
    if state_white == 1:
        text_state1 = font_2.render("White King is under check!", True, (255, 255, 255), (0, 0, 0))
    else:
        text_state1 = font_2.render("White King is under check!", True, (0, 0, 0), (0, 0, 0))
    if state_black == 1:
        text_state2 = font_2.render("Black King is under check!", True, (255, 255, 255), (0, 0, 0))
    else:
        text_state2 = font_2.render("Black King is under check!", True, (0, 0, 0), (0, 0, 0))
    win.blit(text_time1, (width - padding_abs_half - text_time1.get_width(),
                          width - padding_abs_half + text_time1.get_height()))
    win.blit(text_state2, (width - padding_abs_half - text_state2.get_width(),
                           padding_abs_half - text_state2.get_height() * 1.5))
    win.blit(text_time2, (padding_abs_half, padding_abs_half - text_time2.get_height() * 2))
    win.blit(text_state1, (padding_abs_half, width - padding_abs_half / 1.5))
    pygame.display.update()


def end_screen(text, total_time):
    pygame.font.init()
    font_1 = pygame.font.SysFont("arial", 70, bold=True)
    font_2 = pygame.font.SysFont("arial", 35, bold=True)
    font_3 = pygame.font.SysFont("arial", 20, bold=True)
    total_time = int(total_time)
    format_time = str(total_time // 60) + ":" + str(total_time % 60)
    if total_time % 60 < 10:
        format_time = str(total_time // 60) + ":" + "0" + str(total_time % 60)
    elif total_time % 60 == 0:
        format_time += "0"
    text_render = font_1.render(text, True, (255, 0, 0))
    text_time = font_2.render(format_time, True, (255, 0, 0))
    text_help = font_3.render("Press q - to quit and r - to restart", True, (255, 255, 255))
    pygame.draw.rect(win, (0, 0, 0), (-1, width / 2 - text_render.get_height(), width + 1, width - width/1.3))
    win.blit(text_render, (width / 2 - text_render.get_width() / 2, width / 2 - text_render.get_height()))
    win.blit(text_time, (width / 2 - text_time.get_width() / 2, width / 2))
    win.blit(text_help, (width / 2 - text_help.get_width() / 2, width / 2 + text_time.get_height()*1.2))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("log: quit is pressed")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    print("log: restart is pressed")
                    main()


def start_screen():
    pygame.font.init()
    font_1 = pygame.font.SysFont("arial", 30, bold=True)
    font_2 = pygame.font.SysFont("arial", 40, bold=True)
    text_0 = font_2.render("Hotkeys", True, (255, 0, 0))
    text_1 = font_1.render("q - to quit", True, (255, 255, 255))
    text_2 = font_1.render("s - to surrender", True, (255, 255, 255))
    text_3 = font_1.render("p - to vote for draw", True, (255, 255, 255))
    pygame.draw.rect(win, (0, 0, 0), (-1, -1, width + 1, width + 1))
    win.blit(text_0, ((width - text_0.get_width()) / 2, width * 0.3))
    win.blit(text_1, (width * 0.4, width * 0.4))
    win.blit(text_2, (width * 0.4, width * 0.45))
    if game_mode != 1:
        win.blit(text_3, (width * 0.4, width * 0.5))
    pygame.time.set_timer(pygame.USEREVENT + 1, freeze_time * 1000 + 1)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT + 1:
                run = False


def click(pos):
    x = pos[0]
    y = pos[1]
    print("log: clicked at position: ", pos)
    if top_left_corner[0] < x < top_left_corner[0] + bottom_right_corner[0]:
        if top_left_corner[1] < y < top_left_corner[1] + bottom_right_corner[1]:
            divx = x - top_left_corner[0]
            divy = y - top_left_corner[0]
            i = int(divx / (bottom_right_corner[0] / 8))
            j = int(divy / (bottom_right_corner[1] / 8))
            print("log: clicked at cell: ", i, j)
            return i, j


# main -----------------------------------------------------------------------------------------------------------------
def main():
    player1_time = time_restriction_seconds
    player2_time = time_restriction_seconds
    wide_timer = time.time()
    start_time = time.time()
    turn = "w"
    turn_number = 0
    game_board = Board(8, 8)
    game_board.update_moves()
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
        redraw_gamewindow(game_board, int(player1_time), int(player2_time), statewhite, stateblack)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("log: clicked quit")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    print("log: clicked surrender")
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
                    print("log: white wants draw", white_wants_draw)
                    print("log: black wants draw", black_wants_draw)
                    if black_wants_draw and white_wants_draw:
                        print("log: draw")
                        end_screen("Draw!", time.time() - start_time)
# ----------------------------------------------------------------------------------------------------------------------
            if turn == "b" and game_mode == 1:
                if statewhite == 1:
                    end_screen("Black Wins!", time.time() - start_time)
                change = False
                game_board.update_moves()
                solve = Solution(game_board)
                try:
                    (piecex, piecey), choice = solve.random_choice(turn)
                    if difficulty == 1:
                        (piecex, piecey), choice = solve.tier3_choice(turn)
                    elif difficulty == 2:
                        (piecex, piecey), choice = solve.tier2_choice(turn)
                    elif difficulty == 3:
                        (piecex, piecey), choice = solve.tier1_choice(turn)
                    game_board.simple_move((piecex, piecey), (choice[1], choice[0]), "b")
                    change = True
                except TypeError:
                    print("log: type error, it's either critical script problem or true winning condition")
                    end_screen("White Wins!", time.time() - start_time)
                if change:
                    turn_number += 1
                    wide_timer = time.time()
                    game_board.reset_selected()
                    if game_board.is_checked("b") and stateblack == 1:
                        end_screen("White Wins!", time.time() - start_time)
                    if game_board.is_checked("w") and statewhite == 1:
                        end_screen("Black Wins!", time.time() - start_time)
                    turn = "w"
                if game_board.is_checked("b"):
                    stateblack = 1
                else:
                    stateblack = 0
# ----------------------------------------------------------------------------------------------------------------------
            elif (turn == "w" and game_mode == 1) or game_mode == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = pygame.mouse.get_pos()
                    game_board.update_moves()
                    if padding_abs_half < clicked_position[0] < width - padding_abs_half \
                            and padding_abs_half < clicked_position[1] < width - padding_abs_half:
                        i, j = click(clicked_position)
                        try:
                            change = game_board.select(i, j, turn)
                            game_board.update_moves()
                        except AttributeError:
                            print("log: non-terminal skript error")
                            change = False
                        if change:
                            turn_number += 1
                            wide_timer = time.time()
                            if turn == "w":
                                game_board.reset_selected()
                                if game_board.is_checked("w") and statewhite == 1:
                                    end_screen("Black Wins!", time.time() - start_time)
                                if game_board.is_checked("b") and stateblack == 1:
                                    end_screen("White Wins!", time.time() - start_time)
                                turn = "b"
                            else:
                                game_board.reset_selected()
                                if game_board.is_checked("b") and stateblack == 1:
                                    end_screen("White Wins!", time.time() - start_time)
                                if game_board.is_checked("w") and statewhite == 1:
                                    end_screen("Black Wins!", time.time() - start_time)
                                turn = "w"
                    if game_board.is_checked("w"):
                        statewhite = 1
                    else:
                        statewhite = 0
                    if game_board.is_checked("b"):
                        stateblack = 1
                    else:
                        stateblack = 0


# ----------------------------------------------------------------------------------------------------------------------
win = pygame.display.set_mode((width, height), vsync=True)
pygame.display.set_caption("PyChess")
pygame.display.set_icon(icon)
start_screen()
main()
