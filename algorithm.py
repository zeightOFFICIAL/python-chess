from random import choice
from board import Board
import copy

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


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
        self.board_estimated = outer_board_estimation(self.bo)
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
        best_value = -99999
        best_value_return = 1
        self.board_estimated = outer_board_estimation(self.bo)
        best_move = self.random_choice()
        new_bo = copy.deepcopy(self.bo)
        for row in range(0, 8):
            for col in range(0, 8):
                if new_bo.board[row][col] != 0 and new_bo.board[row][col].color == "b":
                    for move in new_bo.board[row][col].move_list:
                        if self.board_estimated[move[1]][move[0]] >= best_value:
                            best_value = self.board_estimated[move[1]][move[0]]
                            best_move = (row, col, (move[1], move[0]))
                    value = best_value
                    new_bo.move((best_move[0], best_move[1]), (best_move[2][1], best_move[2][0]), "b")
                    board_estimated = outer_board_estimation(new_bo)
                    for row2 in range(0, 8):
                        for col2 in range(0, 8):
                            if new_bo.board[row2][col2] != 0 and new_bo.board[row2][col2].color == "w":
                                for move2 in new_bo.board[row2][col2].move_list:
                                    if board_estimated[move2[1]][move2[0]] < best_value_return:
                                        best_value_return = board_estimated[move2[1]][move2[0]]
                                        best_move = (row2, col2, (move2[1], move2[0]))
                                    value += best_value_return
                                    if value > best_value:
                                        best_value = value
                                        best_move = (row, col, (move[1], move[0]))
                    new_bo = copy.deepcopy(self.bo)
        if best_value == 0:
            best_move = self.random_choice()
        print(best_value)
        return best_move


def outer_board_estimation(board):
    board_estimated = [[0 for _ in range(8)] for _ in range(8)]
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        board_estimated[row][col] = 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        board_estimated[row][col] = 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        board_estimated[row][col] = 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        board_estimated[row][col] = 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        board_estimated[row][col] = 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        board_estimated[row][col] = 900
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        board_estimated[row][col] = -50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        board_estimated[row][col] = -10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        board_estimated[row][col] = -30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        board_estimated[row][col] = -30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        board_estimated[row][col] = -90
                    elif board.board[row][col].__class__.__name__ == "King":
                        board_estimated[row][col] = -900
    return board_estimated
