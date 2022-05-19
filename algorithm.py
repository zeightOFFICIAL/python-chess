from random import choice
from board import Board
from math import inf
import copy


class Solution:
    def __init__(self, board):
        self.bo = board
        self.figure = None
        self.rgmove = None
        self.amoves = []
        self.board_estimated = [[0 for _ in range(8)] for _ in range(8)]

        self.w_pawn = 0
        self.b_pawn = 0
        self.w_knight = 0
        self.b_knight = 0
        self.w_bishop = 0
        self.b_bishop = 0
        self.w_rook = 0
        self.b_rook = 0
        self.w_queen = 0
        self.b_queen = 0

    def random_choice(self):
        all_pieces = []
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0:
                    if self.bo.board[row][col].color == "b":
                        all_pieces.append(self.bo.board[row][col])
        random_piece = choice(all_pieces)
        self.figure = self.bo.board[random_piece.row][random_piece.col]
        while True:
            random_piece = choice(all_pieces)
            self.figure = self.bo.board[random_piece.row][random_piece.col]
            if len(self.figure.move_list) > 0:
                break
        random_move = (random_piece.row, random_piece.col, (choice(self.figure.move_list)[1], choice(self.figure.move_list)[0]))
        return random_move

    def tier3_choice(self):
        best_value = -1
        self.board_estimated = outer_board_estimation(self.bo)[0]
        best_move = self.random_choice()
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0 and self.bo.board[row][col].color == "b":
                    for move in self.bo.board[row][col].move_list:
                        if self.board_estimated[move[1]][move[0]] >= best_value:
                            best_value = self.board_estimated[move[1]][move[0]]
                            best_move = (row, col, (move[1], move[0]))
        return best_move

    def tier2_choice(self):
        def minimax(board, depth, alpha, beta, maximazing):
            if depth == 0:
                return None, outer_board_estimation(board)[2]
            minimax_best_move = self.random_choice()
            if maximazing:
                max_value = -inf
                for row1 in range(0, 8):
                    for col1 in range(0, 8):
                        board.update_moves()
                        if board.board[row1][col1] != 0 and board.board[row1][col1].color == "b":
                            for move in board.board[row1][col1].move_list:
                                print(board.board[row1][col1].move_list)
                                board.simple_move((row1, col1), (move[1], move[0]), "b")
                                current_eval = minimax(board, depth - 1, alpha, beta, False)[1]
                                board.simple_move((move[1], move[0]), (row1, col1), "b")
                                board.update_moves()
                                if current_eval > max_value:
                                    max_value = current_eval
                                    minimax_best_move = (row1, col1, (move[1], move[0]))
                                alpha = max(alpha, current_eval)
                                if beta <= alpha:
                                    break
                        return minimax_best_move, max_value
            else:
                min_value = inf
                for row2 in range(0, 8):
                    for col2 in range(0, 8):
                        board.update_moves()
                        if board.board[row2][col2] != 0 and board.board[row2][col2].color == "w":
                            for move2 in board.board[row2][col2].move_list:
                                board.simple_move((row2, col2), (move2[1], move2[0]), "w")
                                current_eval = minimax(board, depth - 1, alpha, beta, True)[1]
                                board.simple_move((move2[1], move2[0]), (row2, col2), "w")
                                board.update_moves()
                                if current_eval < min_value:
                                    min_value = current_eval
                                    minimax_best_move = (row2, col2, (move2[1], move2[0]))
                                beta = min(beta, current_eval)
                                if beta <= alpha:
                                    break
                        return minimax_best_move, min_value
        board_copy = copy.deepcopy(self.bo)
        best_move, best_value = minimax(self.bo, 3, inf, -inf, True)
        return best_move


def outer_board_estimation(board):
    board_estimated = [[0 for _ in range(8)] for _ in range(8)]
    white_score = 0
    black_score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        board_estimated[row][col] = 50
                        white_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        board_estimated[row][col] = 10
                        white_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        board_estimated[row][col] = 30
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        board_estimated[row][col] = 30
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        board_estimated[row][col] = 90
                        white_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        board_estimated[row][col] = 900
                        white_score += 900
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        board_estimated[row][col] = -50
                        black_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        board_estimated[row][col] = -10
                        black_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        board_estimated[row][col] = -30
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        board_estimated[row][col] = -30
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        board_estimated[row][col] = -90
                        black_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        board_estimated[row][col] = -900
                        black_score += 900
    return board_estimated, white_score, black_score
