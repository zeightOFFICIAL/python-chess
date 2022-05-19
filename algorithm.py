from random import choice
from board import Board
from math import inf
import copy


class Solution:
    def __init__(self, board):
        self.bo = board
        self.figure = None
        self.board_estimated = [[0 for _ in range(8)] for _ in range(8)]

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
        best_value = -inf
        self.board_estimated = outer_board_estimation(self.bo)[0]
        best_move = self.random_choice()
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0 and self.bo.board[row][col].color == "b":
                    for move in self.bo.board[row][col].move_list:
                        if self.board_estimated[move[1]][move[0]] >= best_value:
                            best_value = self.board_estimated[move[1]][move[0]]
                            best_move = (row, col, (move[1], move[0]))
                        if self.bo.is_checked("b"):
                            self.bo.simple_move((row, col), (move[1], move[0]), "b")
                            if not self.bo.is_checked("b"):
                                best_move = (row, col, (move[1], move[0]))
                                self.bo.simple_move((move[1], move[0]), (row, col), "b")
                                return best_move
                            self.bo.simple_move((move[1], move[0]), (row, col), "b")
        return best_move

    def tier2_choice(self):
        def minimax(board, depth, alpha, beta, maximizing):
            if depth == 0:
                return None, outer_board_estimation(board)[1]
            best_move_minmax = self.random_choice()
            board.update_moves()
            if maximizing:
                max_value = -inf
                moves = get_all_moves(board, "b")
                for move in moves:
                    new_board = board
                    board.simple_move((move[0][0], move[0][1]), (move[1][1], move[1][0]), "b")
                    current_value = minimax(board, depth - 1, alpha, beta, False)[1]
                    #board.simple_move((move[1][0], move[1][1]), (move[0][1], move[0][0]), "b")
                    board = new_board
                    if current_value > max_value:
                        max_value = current_value
                        best_move_minmax = (move[0][0], move[0][1], (move[1][0], move[1][1]))
                    alpha = max(alpha, current_value)
                    if beta <= alpha:
                        break
                return best_move_minmax, max_value
            else:
                min_value = inf
                moves = get_all_moves(board, "w")
                for move in moves:
                    new_board = board
                    board.simple_move((move[0][0], move[0][1]), (move[1][1], move[1][0]), "w")
                    current_value = minimax(board, depth - 1, alpha, beta, True)[1]
                    #board.simple_move((move[1][1], move[1][0]), (move[0][0], move[0][1]), "b")
                    board = new_board
                    if current_value < min_value:
                        min_value = current_value
                        print()
                        best_move_minmax = (move[0][0], move[0][1], (move[1][1], move[1][0]))
                    beta = min(beta, current_value)
                    if beta <= alpha:
                        break
                return best_move_minmax, min_value
        best_move, best_value = minimax(copy.deepcopy(self.bo), 3, inf, -inf, True)
        return best_move


def get_all_moves(board, color):
    all_moves = []
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0 and board.board[row][col].color == color:
                for move in board.board[row][col].move_list:
                    all_moves.append(((row, col), (move[0], move[1])))
    return all_moves


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
    return board_estimated, black_score - white_score
