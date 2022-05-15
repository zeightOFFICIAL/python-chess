from board import Board
from random import choice
import piece


class Solution:
    def __init__(self, board):
        self.bo = board
        self.figure = None
        self.rgmove = None
        self.amoves = []

    def random_choice(self):
        all_pieces = []
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0:
                    if self.bo.board[row][col].color == "w":
                        all_pieces.append(self.bo.board[row][col])
        random_piece = choice(all_pieces)
        self.figure = self.bo.board[random_piece.row][random_piece.col]
        while True:
            random_piece = choice(all_pieces)
            self.figure = self.bo.board[random_piece.row][random_piece.col]
            if len(self.figure.move_list) > 0:
                break
        random_move = choice(self.figure.move_list)
        return random_piece.col, random_piece.row, random_move

