# ver 904
# game.py
# python libraries =====================================================================================================
import sys
import pygame
import time
import logging

# project libraries ====================================================================================================
from gameobjects.board import Board
from scripts.algorithm import Solution

# resources ============================================================================================================
from configuration.flowingconfig import *
raw_board = pygame.image.load("resources/images/eq_chessboard.png")
icon = pygame.image.load("resources/icons/icon.png")
if visual_set != 0:
    try:
        raw_board = pygame.image.load(
            "resources/images/"+str(visual_set)+"/eq_chessboard.png")
    except (FileNotFoundError, FileExistsError) as e:
        logging.warning("(game.py in resources loading): Custom visual set cannot be loaded. Partly or entirely.")
scaled_board = pygame.transform.smoothscale(
    raw_board, (width - padding_absolute, height - padding_absolute))

# setting up fonts and logging =========================================================================================
pygame.font.init()
player_time_font = pygame.font.SysFont("console", int(width*0.022))
king_condition_font = pygame.font.SysFont("console", int(width*0.033))
main_text_font = pygame.font.SysFont("arial", int(width*0.093), bold=True)
time_text_font = pygame.font.SysFont("arial", int(width*0.04), bold=True)
help_text_font = pygame.font.SysFont("arial", int(width*0.026), bold=True)
secondary_help_font = pygame.font.SysFont("arial", int(width*0.04), bold=True)
primal_help_font = pygame.font.SysFont("arial", int(width*0.053), bold=True)
logging.basicConfig(format='log:%(levelname)s:%(message)s', level=logging.DEBUG)

# functions ============================================================================================================
# FUNCTION to redraw the gamewindow. renders the new one from scrap, and updates
def redraw_gamewindow(board_to_render, player1_time, player2_time, state_white, state_black):
    pygame.draw.rect(win, (0, 0, 0), (0, 0, width, width))
    win.blit(scaled_board, (padding_abs_half, padding_abs_half))
    board_to_render.draw(win)
    format_time_p1 = f'{player1_time // 60:d}:{player1_time % 60:02d}'
    format_time_p2 = f'{player2_time // 60:d}:{player2_time % 60:02d}'
    text_time1 = player_time_font.render(
        "Player 1 Time: " + str(format_time_p1), True, (255, 255, 255), (0, 0, 0))
    text_time2 = player_time_font.render(
        "Player 2 Time: " + str(format_time_p2), True, (255, 255, 255), (0, 0, 0))
    if state_white == 1:
        text_state1 = king_condition_font.render(
            "White King is under check!", True, (255, 255, 255), (0, 0, 0))
        win.blit(text_state1, (padding_abs_half,
                 width - padding_abs_half / 1.5))
    if state_black == 1:
        text_state2 = king_condition_font.render(
            "Black King is under check!", True, (255, 255, 255), (0, 0, 0))
        win.blit(text_state2, (width - padding_abs_half - text_state2.get_width(),
                               padding_abs_half - text_state2.get_height() * 1.5))
    win.blit(text_time1, (width - padding_abs_half - text_time1.get_width(),
                          width - padding_abs_half + text_time1.get_height()))
    win.blit(text_time2, (padding_abs_half,
             padding_abs_half - text_time2.get_height() * 2))
    pygame.display.update()


# FUNCTION to render last (end) screen. Displays time of game and the winner.
def end_screen(text, total_time):
    total_time = int(total_time)
    format_time = str(total_time // 60) + ":" + str(total_time % 60)
    format_time = f'{total_time // 60:d}:{total_time % 60:02d}'
    text_render = main_text_font.render(text, True, (255, 0, 0))
    text_time = time_text_font.render(format_time, True, (255, 0, 0))
    text_help = help_text_font.render(
        "Press q - to quit and r - to restart", True, (255, 255, 255))
    pygame.draw.rect(win, (0, 0, 0), (-1, width / 2 -
                     text_render.get_height(), width + 1, width - width/1.3))
    win.blit(text_render, (width / 2 - text_render.get_width() /
             2, width / 2 - text_render.get_height()))
    win.blit(text_time, (width / 2 - text_time.get_width() / 2, width / 2))
    win.blit(text_help, (width / 2 - text_help.get_width() /
             2, width / 2 + text_time.get_height()*1.2))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    logging.debug("(game.py in end_screen): Quit button is pressed.")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    logging.debug("(game.py in end_screen): Restart button is pressed.")
                    main()


# FUNCTION to render first (start) screen.
def start_screen():
    primal_help_text = primal_help_font.render("Hotkeys", True, (255, 0, 0))
    first_help_line = secondary_help_font.render(
        "q - to quit", True, (255, 255, 255))
    second_help_line = secondary_help_font.render(
        "s - to surrender", True, (255, 255, 255))
    surrender_button_line = secondary_help_font.render(
        "p - to vote for draw", True, (255, 255, 255))
    pygame.draw.rect(win, (0, 0, 0), (-1, -1, width + 1, width + 1))
    win.blit(primal_help_text,
             ((width - primal_help_text.get_width()) / 2, width * 0.3))
    win.blit(first_help_line, (width * 0.4, width * 0.4))
    win.blit(second_help_line, (width * 0.4, width * 0.45))
    if game_mode != 1:
        win.blit(surrender_button_line, (width * 0.4, width * 0.5))
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
    if top_left_corner[0] < x < top_left_corner[0] + bottom_right_corner[0]:
        if top_left_corner[1] < y < top_left_corner[1] + bottom_right_corner[1]:
            divx = x - top_left_corner[0]
            divy = y - top_left_corner[0]
            i = int(divx / (bottom_right_corner[0] / 8))
            j = int(divy / (bottom_right_corner[1] / 8))
            logging.debug("(game.py in click): Clicked at position: (x=%d, y=%d), at cell (w=%d, h=%d)", x, y, i, j)
            return i, j
    else:
        logging.debug("(game.py in click): Clicked at position: (x=%d, y=%d). Not at the cell.", x, y)


# main -----------------------------------------------------------------------------------------------------------------
def main():
    logging.info("(game.py in main at start): Game started: %d, %d, %d", game_mode, difficulty, time_restriction)
    white_time, black_time = time_restriction_seconds, time_restriction_seconds
    wide_timer, start_time = time.time(), time.time()
    statewhite, stateblack = 0, 0
    white_wants_draw, black_wants_draw = 0, 0
    turn = "w"
    turn_number = 0
    game_board = Board(8, 8)
    game_board.update_moves()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(fps_max)
        
        if turn == "w":
            white_time -= (time.time() - wide_timer)
            if white_time <= 0:
                end_screen("Black Wins!", time.time() - start_time)
                logging.info("(game.py in main): White out of time.")
        else:
            black_time -= (time.time() - wide_timer)
            if black_time <= 0:
                end_screen("White Wins!", time.time() - start_time)
                logging.info("(game.py in main): Black out of time.")
        wide_timer = time.time()
        redraw_gamewindow(game_board, int(white_time), int(
            black_time), statewhite, stateblack)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    logging.debug("(game.py in main): Quit button is pressed.")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    logging.debug("(game.py in main): Surrender button is pressed by %c", turn)
                    if turn == "w":
                        end_screen("Black Wins!", time.time() - start_time)
                    else:
                        end_screen("White Wins!", time.time() - start_time)
                if event.key == pygame.K_p:
                    if turn == "w":
                        white_wants_draw = 1 if white_wants_draw == 0 else 0
                    if turn == "b":
                        black_wants_draw = 1 if black_wants_draw == 0 else 0
                    logging.info("(game.py in main): White wants draw? - %b", bool(white_wants_draw))
                    logging.info("(game.py in main): White wants draw? - %b", bool(black_wants_draw))
                    if black_wants_draw and white_wants_draw:
                        logging.debug("(game.py in main): Draw.")
                        end_screen("Draw!", time.time() - start_time)
# game mode = 1. BLACK - AI, WHITE - PLAYER. ---------------------------------------------------------------------------
            if turn == "b" and game_mode == 1:
                if statewhite == 1:
                    end_screen("Black Wins!", time.time() - start_time)
                    logging.debug("game.py in main): Black wins. White ended its turn with checked king.")                    
                change = False
                solve = Solution(game_board)
                try:
                    (piecex, piecey), choice = solve.random_choice(turn)
                    if difficulty == 1:
                        (piecex, piecey), choice = solve.tier3_choice(turn)
                    elif difficulty == 2:
                        (piecex, piecey), choice = solve.tier2_choice(turn)
                    elif difficulty == 3:
                        (piecex, piecey), choice = solve.tier1_choice(turn)
                    game_board.simple_move(
                        (piecex, piecey), (choice[1], choice[0]), "b")
                    change = True
                except TypeError:
                    logging.warning("(game.py in main): Type error. It's either critical script failure or true winning condition. Typical crutch)))")
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
# ----------------------------------------------------------------------------------------------------------------------
            elif (turn == "w" and game_mode == 1) or game_mode == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_position = pygame.mouse.get_pos()
                    game_board.update_moves()
                    try:
                        i, j = click(clicked_position)
                        change = game_board.select(i, j, turn)
                        game_board.update_moves()
                    except AttributeError:
                        logging.warning("(game.py in main): Non-terminal script error. Selection error lead to game_board.select(i, j, turn)")
                        change = False
                    except TypeError:
                        logging.debug("(game.py in main): Non-terminal TypeError originated at click(clicked_position)")
                        change = False
                    if change:
                        turn_number += 1
                        wide_timer = time.time()
                        if turn == "w":
                            game_board.reset_selected()
                            if game_board.is_checked("w") and statewhite == 1:
                                end_screen("Black Wins!",
                                           time.time() - start_time)
                            if game_board.is_checked("b") and stateblack == 1:
                                end_screen("White Wins!",
                                           time.time() - start_time)
                            turn = "b"
                        else:
                            game_board.reset_selected()
                            if game_board.is_checked("b") and stateblack == 1:
                                end_screen("White Wins!",
                                           time.time() - start_time)
                            if game_board.is_checked("w") and statewhite == 1:
                                end_screen("Black Wins!",
                                           time.time() - start_time)
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
