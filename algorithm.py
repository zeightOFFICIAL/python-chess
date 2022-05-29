import copy
from random import choice
from math import inf


class Solution:
    def __init__(self, board):
        self.bo = board
        self.evaluation = 0

    def random_choice(self):
        all_pieces = []
        was_checked = self.bo.is_checked("b")
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0:
                    if self.bo.board[row][col].color == "b":
                        all_pieces.append(self.bo.board[row][col])
        if was_checked:
            for piece in all_pieces:
                for move in piece.move_list:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[0], move[1]), "b")
                    if not new_board.is_checked("b"):
                        return (piece.row, piece.col), (move[0], move[1])
            return -1
        else:
            while True:
                random_piece = choice(all_pieces)
                if len(random_piece.move_list) > 0:
                    random_move = choice(random_piece.move_list)
                    random_move = ((random_piece.row, random_piece.col), (random_move[0], random_move[1]))
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((random_move[0][0], random_move[0][1]),
                                          (random_move[1][1], random_move[1][0]), "b")
                    if not new_board.is_checked("b"):
                        return random_move

    def tier3_choice(self):
        best_value = -inf
        best_move = self.random_choice()
        salvation = False
        self.evaluation = outer_board_estimation(self.bo)
        was_checked = self.bo.is_checked("b")
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0 and self.bo.board[row][col].color == "b":
                    for move in self.bo.board[row][col].move_list:
                        new_board = copy.deepcopy(self.bo)
                        if was_checked:
                            new_board.simple_move((row, col), (move[1], move[0]), "b")
                            if not new_board.is_checked("b"):
                                if outer_board_estimation(new_board) > best_value:
                                    best_value = outer_board_estimation(new_board)
                                    best_move = ((row, col), (move[0], move[1]))
                                    salvation = True
                        else:
                            salvation = True
                            new_board.simple_move((row, col), (move[1], move[0]), "b")
                            if not new_board.is_checked("b"):
                                if outer_board_estimation(new_board) > best_value:
                                    best_value = outer_board_estimation(new_board)
                                    best_move = ((row, col), (move[0], move[1]))
        if not salvation:
            return -1
        if best_value == self.evaluation and not was_checked:
            return self.random_choice()
        return best_move

    def tier2_choice(self):

        return self.random_choice()


def get_all_moves(board, color):
    all_moves = []
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0 and board.board[row][col].color == color:
                for move in board.board[row][col].move_list:
                    all_moves.append(((row, col), (move[1], move[0])))
    return all_moves


def outer_board_estimation(board):
    white_score = 0
    black_score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        white_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        white_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        white_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        white_score += 900
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        black_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        black_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        black_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        black_score += 900
    return black_score - white_score


def outer_board_advanced_estimation(board):
    white_score = 0
    black_score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        white_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        white_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        white_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        white_score += 900
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        black_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        black_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        black_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        black_score += 900
    return black_score - white_score
