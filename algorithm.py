from random import choice
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
        print(self.tier2_choice())
        return best_move

    def tier2_choice(self):
        def converttype(string):
            if string == "a":
                return 0
            elif string == "b":
                return 1
            elif string == "c":
                return 2
            elif string == "d":
                return 3
            elif string == "e":
                return 4
            elif string == "f":
                return 5
            elif string == "g":
                return 6
            elif string == "h":
                return 7

        def evaluation(board):
            def getpiecevalue(piece):
                if piece is None:
                    return 0
                _value = 0
                if piece == "P" or piece == "p":
                    _value = 10
                if piece == "N" or piece == "n":
                    _value = 30
                if piece == "B" or piece == "b":
                    _value = 30
                if piece == "R" or piece == "r":
                    _value = 50
                if piece == "Q" or piece == "q":
                    _value = 90
                if piece == 'K' or piece == 'k':
                    _value = 900
                return _value
            i = 0
            evaluation_value = 0
            valuation = True
            try:
                valuation = bool(chess_board.piece_at(i).color)
            except AttributeError as e:
                valuation = x
            while i < 63:
                i += 1
                evaluation_value += getpiecevalue(str(chess_board.piece_at(i))) if valuation else -getpiecevalue(
                    str(chess_board.piece_at(i)))
            return evaluation_value

        def minimax(board, depth, maximizing):
            if depth == 0:
                return evaluation(board)
            moves = chess_board.legal_moves
            if maximizing:
                best_value = -inf
                for move2 in moves:
                    move2 = chess.Move.from_uci(str(move2))
                    chess_board.push(move2)
                    best_value = max(best_value, minimax(board, depth - 1, not maximizing))
                    chess_board.pop()
                return best_value
            else:
                best_value = inf
                for move2 in moves:
                    move2 = chess.Move.from_uci(str(move2))
                    chess_board.push(move2)
                    best_value = min(best_value, minimax(board, depth - 1, not maximizing))
                    chess_board.pop()
                return best_value

        chess_board = chess.Board(convertboard(self.bo))
        possibleMoves = chess_board.legal_moves
        bestMove = -inf
        secondBest = -inf
        thirdBest = -inf
        bestMoveFinal = None
        chess_board = chess.Board(convertboard(self.bo))
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            chess_board.push(move)
            value = max(bestMove, minimax(chess_board, 2, False))
            chess_board.pop()
            if (value > bestMove):
                thirdBest = secondBest
                secondBest = bestMove
                bestMove = value
                bestMoveFinal = move
        best_move = bestMoveFinal.uci()
        best_move = ((int(best_move[1])-1, converttype(best_move[0])), (converttype(best_move[2]), int(best_move[3])-1))
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
    result = ""
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        result += "R"
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        result += "P"
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        result += "B"
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        result += "N"
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        result += "Q"
                    elif board.board[row][col].__class__.__name__ == "King":
                        result += "K"
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        result += "r"
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        result += "p"
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        result += "b"
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        result += "n"
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        result += "q"
                    elif board.board[row][col].__class__.__name__ == "King":
                        result += "k"
            else:
                count_spaces += 1
                if col + 1 > 7:
                    result += str(count_spaces)
                    count_spaces = 0
                elif board.board[row][col+1] != 0:
                    result += str(count_spaces)
                    count_spaces = 0
        if row < 7:
            result += "/"
    return str(result)

