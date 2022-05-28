import copy
from random import choice
from math import inf


class Solution:
    def __init__(self, board):
        self.bo = board
        self.evaluation = 0

    def random_choice(self):
        all_pieces = []
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0:
                    if self.bo.board[row][col].color == "b":
                        all_pieces.append(self.bo.board[row][col])
        while True:
            random_piece = choice(all_pieces)
            if len(random_piece.move_list) > 0:
                random_move = choice(random_piece.move_list)
                random_move = ((random_piece.row, random_piece.col), (random_move[0], random_move[1]))
                break
        return random_move

    def tier3_choice(self):
        best_value = -inf
        self.evaluation = outer_board_estimation(self.bo)
        best_move = self.random_choice()
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0 and self.bo.board[row][col].color == "b":
                    for move in self.bo.board[row][col].move_list:
                        was_checked = self.bo.is_checked("b")
                        self.bo.simple_move((row, col), (move[1], move[0]), "b")
                        if self.evaluation - outer_board_estimation(self.bo) > best_value:
                            best_value = self.evaluation - outer_board_estimation(self.bo)
                            best_move = ((row, col), (move[0], move[1]))
                        self.bo.simple_move((move[1], move[0]), (row, col), "b")

                        """if was_checked:
                            if not self.bo.is_checked("b"):
                                print("was checked")
                                if self.evaluation - outer_board_estimation(self.bo) > best_value:
                                    best_value = outer_board_estimation(self.bo)
                                    best_move = ((row, col), (move[0], move[1]))
                            self.bo.simple_move((move[1], move[0]), (row, col), "b")
                        else:
                            if self.evaluation - outer_board_estimation(self.bo) > best_value:
                                best_value = outer_board_estimation(self.bo)
                                best_move = ((row, col), (move[0], move[1]))
                            self.bo.simple_move((move[1], move[0]), (row, col), "b")"""
        if best_value == 0:
            return self.random_choice()
        return best_move


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
    print(black_score - white_score)
    return black_score - white_score
