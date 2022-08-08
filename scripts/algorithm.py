# ver 901
# python libraries =====================================================================================================
import copy
import random
from math import inf
from numpy import flipud


# class for algorithmic solution =======================================================================================
class Solution:
    def __init__(self, board):
        self.board = board
        self.evaluation = evaluate_board(self.board, "b")

# diff. 0 random choice ------------------------------------------------------------------------------------------------
    def random_choice(self, color):
        all_moves = []
        was_checked = self.board.is_checked(color)
        self.board.update_moves()
        new_board = copy.deepcopy(self.board)
        all_pieces = get_all_pieces(new_board, color)
        for piece in all_pieces:
            for move in piece.move_list:
                if was_checked:
                    new_board = copy.deepcopy(self.board)
                    new_board.simple_move(
                        (piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        return (piece.row, piece.col), (move[0], move[1])
                else:
                    new_board = copy.deepcopy(self.board)
                    new_board.simple_move(
                        (piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        all_moves.append(
                            ((piece.row, piece.col), (move[0], move[1])))
        if was_checked:
            return -1
        else:
            if len(all_moves) <= 0:
                return -1
            return random.choice(all_moves)

# diff. 1 evaluation ---------------------------------------------------------------------------------------------------
    def tier3_choice(self, color):
        best_value = -inf
        best_move = -1
        was_checked = self.board.is_checked(color)
        new_board = copy.deepcopy(self.board)
        all_pieces = get_all_pieces(new_board, color)
        for piece in all_pieces:
            for move in piece.move_list:
                if was_checked:
                    new_board = copy.deepcopy(self.board)
                    new_board.simple_move(
                        (piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if best_move == -1:
                            best_move = (
                                piece.row, piece.col), (move[0], move[1])
                            best_value = evaluate_board(new_board, color)
                        elif evaluate_board(new_board, color) > best_value:
                            best_move = (
                                piece.row, piece.col), (move[0], move[1])
                            best_value = evaluate_board(new_board, color)
                else:
                    new_board = copy.deepcopy(self.board)
                    new_board.simple_move(
                        (piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if evaluate_board(new_board, color) > best_value:
                            best_value = evaluate_board(new_board, color)
                            best_move = (
                                piece.row, piece.col), (move[0], move[1])
        if best_value == self.evaluation and not was_checked:
            return self.random_choice(color)
        return best_move

# diff. 2 minimax depth 2, advanced evaluation -------------------------------------------------------------------------
    def tier2_choice(self, color):
        def minimaxdepth2(original_color):
            max_value = -inf
            maxed_move = -1
            new_board_1 = copy.deepcopy(self.board)
            all_pieces_1 = get_all_pieces(new_board_1, original_color)
            for piece_1 in all_pieces_1:
                for move_1 in piece_1.move_list:
                    new_board_1 = copy.deepcopy(self.board)
                    new_board_1.simple_move(
                        (piece_1.row, piece_1.col), (move_1[1], move_1[0]), original_color)
                    if not new_board_1.is_checked(original_color):
                        all_pieces_2 = get_all_pieces(
                            new_board_1, "w" if original_color == "b" else "b")
                        min_value = inf
                        for piece_2 in all_pieces_2:
                            for move_2 in piece_2.move_list:
                                new_board_2 = copy.deepcopy(new_board_1)
                                new_board_2.simple_move((piece_2.row, piece_2.col), (move_2[1], move_2[0]),
                                                        "w" if original_color == "b" else "b")
                                if evaluate_board_advanced(new_board_2, original_color) < min_value:
                                    min_value = evaluate_board_advanced(
                                        new_board_2, original_color)
                        total_value = evaluate_board_advanced(
                            new_board_1, original_color) + min_value
                        if total_value > max_value:
                            max_value = total_value
                            maxed_move = (
                                piece_1.row, piece_1.col), (move_1[0], move_1[1])
            if self.evaluation == max_value:
                return self.random_choice(original_color)
            return maxed_move
        was_checked = self.board.is_checked(color)
        if was_checked:
            all_pieces = get_all_pieces(self.board, color)
            best_move = self.random_choice(color)
            best_value = -inf
            for piece in all_pieces:
                for move in piece.move_list:
                    new_board = copy.deepcopy(self.board)
                    new_board.simple_move(
                        (piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if best_value == -inf:
                            best_move = (
                                piece.row, piece.col), (move[0], move[1])
                            best_value = evaluate_board_advanced(new_board, color)
                        elif evaluate_board_advanced(new_board, color) > best_value:
                            best_move = (
                                piece.row, piece.col), (move[0], move[1])
                            best_value = evaluate_board_advanced(new_board, color)
            return best_move
        else:
            best_move = minimaxdepth2(color)
            return best_move

# diff. 3 minimax depth 3, advanced evaluation -------------------------------------------------------------------------
    def tier1_choice(self, color):
        def root_minimax(board, depth, maximizing):
            best_value_root = -inf
            maxed_move_root = self.random_choice(color)
            all_pieces_1 = get_all_pieces(board, color)
            for piece_1 in all_pieces_1:
                for move_1 in piece_1.move_list:
                    next_board = copy.deepcopy(board)
                    next_board.simple_move(
                        (piece_1.row, piece_1.col), (move_1[1], move_1[0]), color)
                    if not next_board.is_checked("b"):
                        value = minimax(next_board, depth -
                                        1, -inf, inf, not maximizing)
                        if value >= best_value_root:
                            best_value_root = value
                            maxed_move_root = (
                                piece_1.row, piece_1.col), (move_1[0], move_1[1])
            return maxed_move_root

        def minimax(board, depth, alpha, beta, maximizing):
            if depth == 0:
                return evaluate_board_advanced(board, "b")
            new_board_1 = copy.deepcopy(board)
            if maximizing:
                all_pieces_1 = get_all_pieces(new_board_1, "b")
                best_value_1 = -inf
                for piece_1 in all_pieces_1:
                    for move_1 in piece_1.move_list:
                        new_board_1 = copy.deepcopy(board)
                        new_board_1.simple_move(
                            (piece_1.row, piece_1.col), (move_1[1], move_1[0]), color)
                        best_value_1 = max(
                            minimax(new_board_1, depth - 1, alpha, beta, not maximizing), best_value_1)
                        alpha = max(alpha, best_value_1)
                        if beta <= alpha:
                            return best_value_1
                return best_value_1
            else:
                all_pieces_1 = get_all_pieces(new_board_1, "w")
                best_value_1 = inf
                for piece_1 in all_pieces_1:
                    for move_1 in piece_1.move_list:
                        new_board_1 = copy.deepcopy(board)
                        new_board_1.simple_move(
                            (piece_1.row, piece_1.col), (move_1[1], move_1[0]), color)
                        best_value_1 = min(
                            minimax(new_board_1, depth - 1, alpha, beta, not maximizing), best_value_1)
                        beta = min(beta, best_value_1)
                        if beta <= alpha:
                            return best_value_1
                return best_value_1

        was_checked = self.board.is_checked(color)
        if was_checked:
            all_pieces = get_all_pieces(self.board, color)
            best_move = self.random_choice(color)
            best_value = -inf
            for piece in all_pieces:
                for move in piece.move_list:
                    new_board = copy.deepcopy(self.board)
                    new_board.simple_move(
                        (piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if best_value == -inf:
                            best_move = (
                                piece.row, piece.col), (move[0], move[1])
                            best_value = evaluate_board_advanced(new_board, color)
                        elif evaluate_board_advanced(new_board, color) > best_value:
                            best_move = (
                                piece.row, piece.col), (move[0], move[1])
                            best_value = evaluate_board_advanced(new_board, color)
            return best_move
        else:
            best_move = root_minimax(self.board, 3, True)
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


# simple evaluation ----------------------------------------------------------------------------------------------------
def evaluate_board(board, color):
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


# advanced evaluation --------------------------------------------------------------------------------------------------
def evaluate_board_advanced(board, color):
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
    rook_list = [[0,  0,  0,  0,  0,  0,  0,  0],
                 [5, 10, 10, 10, 10, 10, 10,  5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [0,  0,  0,  5,  5,  0,  0,  0]]
    queen_list = [[-20, -10, -10, -5, -5, -10, -10, -20],
                  [-10,  0,  0,  0,  0,  0,  0, -10],
                  [-10,  0,  5,  5,  5,  5,  0, -10],
                  [-5,  0,  5,  5,  5,  5,  0, -5],
                  [0,  0,  5,  5,  5,  5,  0, -5],
                  [-10,  5,  5,  5,  5,  5,  0, -10],
                  [-10,  0,  5,  0,  0,  0,  0, -10],
                  [-20, -10, -10, -5, -5, -10, -10, -20]]
    king_list = [[-30, -40, -40, -50, -50, -40, -40, -30],
                 [-30, -40, -40, -50, -50, -40, -40, -30],
                 [-30, -40, -40, -50, -50, -40, -40, -30],
                 [-30, -40, -40, -50, -50, -40, -40, -30],
                 [-20, -30, -30, -40, -40, -30, -30, -20],
                 [-10, -20, -20, -20, -20, -20, -20, -10],
                 [20, 20,  0,  0,  0,  0, 20, 20],
                 [20, 30, 10,  0,  0, 10, 30, 20]]
    white_score = 0
    black_score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "b":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        white_score += 500 + flipud(rook_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        white_score += 100 + flipud(pawn_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        white_score += 330 + flipud(bishop_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        white_score += 320 + flipud(knight_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        white_score += 900 + flipud(queen_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "King":
                        white_score += 20000 + flipud(king_list)[row][col]
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        black_score += 500 + rook_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        black_score += 100 + pawn_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        black_score += 330 + bishop_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        black_score += 320 + knight_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        black_score += 900 + queen_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "King":
                        black_score += 20000 + king_list[row][col]
    if color == "w":
        return white_score - black_score
    else:
        return black_score - white_score
