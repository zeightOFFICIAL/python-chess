# ver 908
# evaluate.py
# libraries ============================================================================================================
from numpy import flipud


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
                        black_score += 500 + flipud(rook_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        black_score += 100 + flipud(pawn_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        black_score += 330 + flipud(bishop_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        black_score += 320 + flipud(knight_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        black_score += 900 + flipud(queen_list)[row][col]
                    elif board.board[row][col].__class__.__name__ == "King":
                        black_score += 20000 + flipud(king_list)[row][col]
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        white_score += 500 + rook_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        white_score += 100 + pawn_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        white_score += 330 + bishop_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        white_score += 320 + knight_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        white_score += 900 + queen_list[row][col]
                    elif board.board[row][col].__class__.__name__ == "King":
                        white_score += 20000 + king_list[row][col]
    if color == "w":
        return white_score - black_score
    else:
        return black_score - white_score


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
