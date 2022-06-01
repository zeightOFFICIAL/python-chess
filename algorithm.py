import copy
import random
from math import inf
from threading import Thread
from typing import List, Any


class Solution:
    def __init__(self, board):
        self.bo = board
        self.evaluation = outer_board_estimation(self.bo, "b")

    def random_choice(self, color):
        all_moves = []
        was_checked = self.bo.is_checked(color)
        self.bo.update_moves()
        new_board = copy.deepcopy(self.bo)
        all_pieces = get_all_pieces(new_board, color)
        for piece in all_pieces:
            for move in piece.move_list:
                if was_checked:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        return (piece.row, piece.col), (move[0], move[1])
                else:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        all_moves.append(((piece.row, piece.col), (move[0], move[1])))
        if was_checked:
            return -1
        else:
            if len(all_moves) <= 0:
                return -1
            return random.choice(all_moves)

    def tier3_choice(self, color):
        best_value = -inf
        was_checked = self.bo.is_checked(color)
        self.bo.update_moves()
        new_board = copy.deepcopy(self.bo)
        best_move = -1
        all_pieces = get_all_pieces(new_board, color)
        for piece in all_pieces:
            for move in piece.move_list:
                if was_checked:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if best_move == -1:
                            best_move = (piece.row, piece.col), (move[0], move[1])
                            best_value = outer_board_estimation(new_board, color)
                        elif outer_board_estimation(new_board, color) > best_value:
                            best_move = (piece.row, piece.col), (move[0], move[1])
                            best_value = outer_board_estimation(new_board, color)
                else:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if outer_board_estimation(new_board, color) > best_value:
                            best_value = outer_board_estimation(new_board, color)
                            best_move = (piece.row, piece.col), (move[0], move[1])
        if best_value == self.evaluation and not was_checked:
            return self.random_choice(color)
        return best_move

    def tier2_choice(self, color):
        def minimaxdepth2(color_inminimax):
            maxed_value = -inf
            maxed_move = -1
            new_board1 = copy.deepcopy(self.bo)
            all_pieces1 = get_all_pieces(new_board1, color_inminimax)
            for piece1 in all_pieces1:
                for move1 in piece1.move_list:
                    new_board1 = copy.deepcopy(self.bo)
                    new_board1.simple_move((piece1.row, piece1.col), (move1[1], move1[0]), color_inminimax)
                    if not new_board1.is_checked(color_inminimax):
                        all_pieces2 = get_all_pieces(new_board1, "w" if color_inminimax == "b" else "b")
                        min_value = inf
                        for piece2 in all_pieces2:
                            for move2 in piece2.move_list:
                                new_board2 = copy.deepcopy(new_board1)
                                new_board2.simple_move((piece2.row, piece2.col), (move2[1], move2[0]),
                                                       "w" if color_inminimax == "b" else "b")
                                if outer_board_estimation(new_board2, color_inminimax) < min_value:
                                    min_value = outer_board_estimation(new_board2, color_inminimax)
                        total_value = outer_board_estimation(new_board1, color_inminimax) + min_value
                        if total_value > maxed_value:
                            maxed_value = total_value
                            maxed_move = (piece1.row, piece1.col), (move1[0], move1[1])
            if self.evaluation == maxed_value:
                return self.random_choice(color_inminimax)
            return maxed_move
        was_checked = self.bo.is_checked(color)
        if was_checked:
            all_pieces = get_all_pieces(self.bo, color)
            best_move = self.random_choice(color)
            best_value = -inf
            for piece in all_pieces:
                for move in piece.move_list:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if best_value == -inf:
                            best_move = (piece.row, piece.col), (move[0], move[1])
                            best_value = outer_board_estimation(new_board, color)
                        elif outer_board_estimation(new_board, color) > best_value:
                            best_move = (piece.row, piece.col), (move[0], move[1])
                            best_value = outer_board_estimation(new_board, color)
            return best_move
        else:
            best_move = minimaxdepth2(color)
            return best_move

    def tier1_choice(self, color):
        def minimaxdepth3(board, color_inminimax, this_depth=0):
            next_board = copy.deepcopy(board)
            if this_depth == 0:
                max_value = -inf
                max_move = self.random_choice(color_inminimax)
                all_pieces1 = get_all_pieces(next_board, color_inminimax)
                for piece1 in all_pieces1:
                    for move1 in piece1.move_list:
                        next_board2 = copy.deepcopy(next_board)
                        next_board2.simple_move((piece1.row, piece1.col), (move1[1], move1[0]), color_inminimax)
                        if not next_board2.is_checked(color_inminimax):
                            value = minimaxdepth3(next_board2, "w" if color_inminimax == "b" else "b", this_depth+1)
                            if value > max_value:
                                max_value = value
                                max_move = (piece1.row, piece1.col), (move1[0], move1[1])
                return max_move
            if this_depth == 1:
                min_value = inf
                all_pieces1 = get_all_pieces(next_board, color_inminimax)
                for piece1 in all_pieces1:
                    for move1 in piece1.move_list:
                        next_board2 = copy.deepcopy(next_board)
                        next_board2.simple_move((piece1.row, piece1.col), (move1[1], move1[0]), color_inminimax)
                        if not next_board2.is_checked(color_inminimax):
                            #value = minimaxdepth3(next_board2, "w" if color_inminimax == "b" else "b", this_depth + 1)
                            if outer_board_estimation(next_board2, color_inminimax) < min_value:
                                min_value = outer_board_estimation(next_board2, color_inminimax)
                return min_value
            if this_depth == 2:
                max_value = -inf
                all_pieces1 = get_all_pieces(next_board, color_inminimax)
                for piece1 in all_pieces1:
                    for move1 in piece1.move_list:
                        next_board2 = copy.deepcopy(next_board)
                        next_board2.simple_move((piece1.row, piece1.col), (move1[1], move1[0]), color_inminimax)
                        if not next_board2.is_checked(color_inminimax):
                            if outer_board_estimation(next_board2, color_inminimax) > max_value:
                                max_value = outer_board_estimation(next_board2, color_inminimax)
                return max_value



        was_checked = self.bo.is_checked(color)
        if was_checked:
            all_pieces = get_all_pieces(self.bo, color)
            best_move = self.random_choice(color)
            best_value = -inf
            for piece in all_pieces:
                for move in piece.move_list:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if best_value == -inf:
                            best_move = (piece.row, piece.col), (move[0], move[1])
                            best_value = outer_board_estimation(new_board, color)
                        elif outer_board_estimation(new_board, color) > best_value:
                            best_move = (piece.row, piece.col), (move[0], move[1])
                            best_value = outer_board_estimation(new_board, color)
            return best_move
        else:
            best_move = minimaxdepth3(self.bo, color)
            return best_move


def get_all_pieces(board, color):
    all_pieces = []
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == color:
                    if len(board.board[row][col].move_list) > 0:
                        all_pieces.append(board.board[row][col])
    return all_pieces


def outer_board_estimation(board, color):
    white_score = 0
    black_score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        white_score += 500
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        white_score += 100
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        white_score += 330
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        white_score += 320
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        white_score += 900
                    elif board.board[row][col].__class__.__name__ == "King":
                        white_score += 20000
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        black_score += 500
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        black_score += 100
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        black_score += 330
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        black_score += 320
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        black_score += 900
                    elif board.board[row][col].__class__.__name__ == "King":
                        black_score += 20000
    if color == "w":
        return white_score - black_score
    else:
        return black_score - white_score


def outer_board_advanced_estimation(board, color):
    pawn_list = [[0,  0,  0,  0,  0,  0,  0,  0],
                 [50, 50, 50, 50, 50, 50, 50, 50],
                 [10, 10, 20, 30, 30, 20, 10, 10],
                 [5,  5, 10, 25, 25, 10,  5,  5],
                 [0,  0,  0, 20, 20,  0,  0,  0],
                 [5, -5, -10,  0,  0, -10, -5,  5],
                 [5, 10, 10, -20, -20, 10, 10,  5],
                 [0,  0,  0,  0,  0,  0,  0,  0]]
    knight_list = [[-50, -40, -30, -30, -30, -30, -40, -50],
                   [-40, -20,  0,  0,  0,  0, -20, -40],
                   [-30,  0, 10, 15, 15, 10,  0, -30],
                   [-30,  5, 15, 20, 20, 15,  5, -30],
                   [-30,  0, 15, 20, 20, 15,  0, -30],
                   [-30,  5, 10, 15, 15, 10,  5, -30],
                   [-40, -20,  0,  5,  5,  0, -20, -40],
                   [-50, -40, -30, -30, -30, -30, -40, -50]]
    bishop_list = [[-20, -10, -10, -10, -10, -10, -10, -20],
                   [-10,  0,  0,  0,  0,  0,  0, -10],
                   [-10,  0,  5, 10, 10,  5,  0, -10],
                   [-10,  5,  5, 10, 10,  5,  5, -10],
                   [-10,  0, 10, 10, 10, 10,  0, -10],
                   [-10, 10, 10, 10, 10, 10, 10, -10],
                   [-10,  5,  0,  0,  0,  0,  5, -10],
                   [-20, -10, -10, -10, -10, -10, -10, -20]]
    white_score = 0
    black_score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        white_score += 500
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        white_score += 100
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        white_score += 330 + bishop_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        white_score += 320 + knight_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        white_score += 900
                    elif board.board[row][col].__class__.__name__ == "King":
                        white_score += 20000
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        black_score += 500
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        black_score += 100
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        black_score += 330 + bishop_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        black_score += 320 + knight_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        black_score += 900
                    elif board.board[row][col].__class__.__name__ == "King":
                        black_score += 20000
    if color == "w":
        return white_score - black_score
    else:
        return black_score - white_score
