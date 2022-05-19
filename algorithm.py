from random import choice
from board import Board
from math import inf
import chess


class Solution:
    def __init__(self, board):
        self.bo = board
        self.board_estimated = [[0 for _ in range(8)] for _ in range(8)]

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
        self.board_estimated = outer_board_estimation(self.bo)[0]
        best_move = self.random_choice()
        for row in range(0, 8):
            for col in range(0, 8):
                if self.bo.board[row][col] != 0 and self.bo.board[row][col].color == "b":
                    for move in self.bo.board[row][col].move_list:
                        if self.board_estimated[move[1]][move[0]] >= best_value:
                            best_value = self.board_estimated[move[1]][move[0]]
                            best_move = ((row, col), (move[0], move[1]))
                        if self.bo.is_checked("b"):
                            self.bo.simple_move((row, col), (move[1], move[0]), "b")
                            if not self.bo.is_checked("b"):
                                best_move = ((row, col), (move[0], move[1]))
                                self.bo.simple_move((move[1], move[0]), (row, col), "b")
                                return best_move
                            self.bo.simple_move((move[1], move[0]), (row, col), "b")
        return best_move

    """def tier2_choice(self):
        def minimax(board):
            best_move_minmax = self.random_choice()
            max_value = -inf
            min_value = inf
            board.update_moves()
            max_moves = get_all_moves(board, "b")
            for move in max_moves:
                board.simple_move((move[0][0], move[0][1]), (move[1][1], move[1][0]), "b")
                value = 0
                transfer_board = copy.deepcopy(board)
                transfer_board.update_moves()
                min_moves = get_all_moves(transfer_board, "w")
                print(move)
                for move_2 in min_moves:
                    if transfer_board.board[move_2[0][0]][move_2[0][1]] != 0:
                        transfer_board.simple_move((move_2[0][0], move_2[0][1]), (move_2[1][1], move_2[1][0]), "w")
                        value = outer_board_estimation(transfer_board)[1]
                        transfer_board = copy.deepcopy(board)
                        if value < min_value:
                            min_value = value
                            best_move_minmax = move_2
                board = copy.deepcopy(self.bo)
                if value > max_value:
                    max_value = value
                    best_move_minmax = move
            return best_move_minmax

        best_move = minimax(copy.deepcopy(self.bo))
        # = self.random_choice()
        return best_move"""


def get_all_moves(board, color):
    all_moves = []
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0 and board.board[row][col].color == color:
                for move in board.board[row][col].move_list:
                    all_moves.append(((row, col), (move[1], move[0])))
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

def convertboard(board):
    count_spaces = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if
