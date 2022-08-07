# piece.py
# python libraries =====================================================================================================
import pygame

# resources ============================================================================================================
from flowingconfig import *
b_bishop = pygame.image.load("res/images/b_bishop.png")
b_king = pygame.image.load("res/images/b_king.png")
b_knight = pygame.image.load("res/images/b_knight.png")
b_pawn = pygame.image.load("res/images/b_pawn.png")
b_queen = pygame.image.load("res/images/b_queen.png")
b_rook = pygame.image.load("res/images/b_rook.png")
w_bishop = pygame.image.load("res/images/w_bishop.png")
w_king = pygame.image.load("res/images/w_king.png")
w_knight = pygame.image.load("res/images/w_knight.png")
w_pawn = pygame.image.load("res/images/w_pawn.png")
w_queen = pygame.image.load("res/images/w_queen.png")
w_rook = pygame.image.load("res/images/w_rook.png")
raw_select = pygame.image.load("res/images/b_select.png")
raw_select2 = pygame.image.load("res/images/b2_select.png")
if visual_set != 0:
    try:
        b_bishop = pygame.image.load(
            "res/images/"+str(visual_set)+"/b_bishop.png")
        b_king = pygame.image.load("res/images/"+str(visual_set)+"/b_king.png")
        b_knight = pygame.image.load(
            "res/images/"+str(visual_set)+"/b_knight.png")
        b_pawn = pygame.image.load("res/images/"+str(visual_set)+"/b_pawn.png")
        b_queen = pygame.image.load(
            "res/images/"+str(visual_set)+"/b_queen.png")
        b_rook = pygame.image.load("res/images/"+str(visual_set)+"/b_rook.png")
        w_bishop = pygame.image.load(
            "res/images/"+str(visual_set)+"/w_bishop.png")
        w_king = pygame.image.load("res/images/"+str(visual_set)+"/w_king.png")
        w_knight = pygame.image.load(
            "res/images/"+str(visual_set)+"/w_knight.png")
        w_pawn = pygame.image.load("res/images/"+str(visual_set)+"/w_pawn.png")
        w_queen = pygame.image.load(
            "res/images/"+str(visual_set)+"/w_queen.png")
        w_rook = pygame.image.load("res/images/"+str(visual_set)+"/w_rook.png")
        raw_select = pygame.image.load(
            "res/images/"+str(visual_set)+"/b_select.png")
        raw_select2 = pygame.image.load(
            "res/images/"+str(visual_set)+"/b2_select.png")
    except FileNotFoundError or FileExistsError:
        print("log: custom visual set cannot be loaded")
black_all = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
white_all = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]
black_all_scaled = []
white_all_scaled = []

# scaling --------------------------------------------------------------------------------------------------------------
for piece_img in black_all:
    black_all_scaled.append(pygame.transform.smoothscale(
        piece_img, (cell_size_x, cell_size_y)))
for piece_img in white_all:
    white_all_scaled.append(pygame.transform.smoothscale(
        piece_img, (cell_size_x, cell_size_y)))
scaled_select = pygame.transform.smoothscale(
    raw_select, (cell_size_x, cell_size_y))
scaled_select2 = pygame.transform.smoothscale(
    raw_select2, (cell_size_x, cell_size_y))


# piece class ==========================================================================================================
class Piece:
    piece_img = -1
    start_x = top_left_corner[0]
    start_y = top_left_corner[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False
        self.queen = False

    def is_selected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def draw(self, win):
        if self.color == "w":
            this_piece_img = white_all_scaled[self.piece_img]
        else:
            this_piece_img = black_all_scaled[self.piece_img]
        if self.selected:
            moves = self.move_list
            for move in moves:
                x = self.start_x + \
                    (move[0] * bottom_right_corner[0] / 8) + (cell_size_y // 2)
                y = self.start_y + \
                    (move[1] * bottom_right_corner[1] / 8) + (cell_size_y // 2)
                if self.color == "w":
                    win.blit(scaled_select,
                             (x - cell_size_x / 2, y - cell_size_y / 2))
                if self.color == 'b':
                    win.blit(scaled_select2,
                             (x - cell_size_x / 2, y - cell_size_y / 2))
        x = self.start_x + (self.col * bottom_right_corner[0] / 8)
        y = self.start_y + (self.row * bottom_right_corner[1] / 8)
        if self.selected:
            if self.color == "w":
                this_piece_img = pygame.transform.smoothscale(white_all[self.piece_img],
                                                              (cell_size_y + pop_increasing_size,
                                                               cell_size_y + pop_increasing_size))
            if self.color == 'b':
                this_piece_img = pygame.transform.smoothscale(black_all[self.piece_img],
                                                              (cell_size_y + pop_increasing_size,
                                                               cell_size_y + pop_increasing_size))
            win.blit(this_piece_img, (x - pop_increasing_size /
                     2, y - pop_increasing_size / 2))
        else:
            win.blit(this_piece_img, (x, y))

    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def __str__(self):
        return str(self.col) + str(self.row)

    def valid_moves(self, board):
        pass


# pieces' implementations, inherited ===================================================================================
class Bishop(Piece):
    piece_img = 0

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        left_strafe = j + 1
        right_strafe = j - 1
        for distance in range(i - 1, -1, -1):
            if left_strafe < 8:
                p = board[distance][left_strafe]
                if p == 0:
                    moves.append((left_strafe, distance))
                elif p.color != self.color:
                    moves.append((left_strafe, distance))
                    break
                else:
                    break
            else:
                break
            left_strafe += 1
        for distance in range(i - 1, -1, -1):
            if right_strafe > -1:
                p = board[distance][right_strafe]
                if p == 0:
                    moves.append((right_strafe, distance))
                elif p.color != self.color:
                    moves.append((right_strafe, distance))
                    break
                else:
                    break
            else:
                break
            right_strafe -= 1
        left_strafe = j + 1
        right_strafe = j - 1
        for distance in range(i + 1, 8):
            if left_strafe < 8:
                p = board[distance][left_strafe]
                if p == 0:
                    moves.append((left_strafe, distance))
                elif p.color != self.color:
                    moves.append((left_strafe, distance))
                    break
                else:
                    break
            else:
                break
            left_strafe += 1
        for distance in range(i + 1, 8):
            if right_strafe > -1:
                p = board[distance][right_strafe]
                if p == 0:
                    moves.append((right_strafe, distance))
                elif p.color != self.color:
                    moves.append((right_strafe, distance))
                    break
                else:
                    break
            else:
                break
            right_strafe -= 1
        return moves


# ----------------------------------------------------------------------------------------------------------------------
class King(Piece):
    piece_img = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        if i > 0:
            if j > 0:
                p = board[i - 1][j - 1]
                if p == 0:
                    moves.append((j - 1, i - 1,))
                elif p.color != self.color:
                    moves.append((j - 1, i - 1,))
            p = board[i - 1][j]
            if p == 0:
                moves.append((j, i - 1))
            elif p.color != self.color:
                moves.append((j, i - 1))
            if j < 7:
                p = board[i - 1][j + 1]
                if p == 0:
                    moves.append((j + 1, i - 1,))
                elif p.color != self.color:
                    moves.append((j + 1, i - 1,))
        if i < 7:
            if j > 0:
                p = board[i + 1][j - 1]
                if p == 0:
                    moves.append((j - 1, i + 1,))
                elif p.color != self.color:
                    moves.append((j - 1, i + 1,))
            p = board[i + 1][j]
            if p == 0:
                moves.append((j, i + 1))
            elif p.color != self.color:
                moves.append((j, i + 1))
            if j < 7:
                p = board[i + 1][j + 1]
                if p == 0:
                    moves.append((j + 1, i + 1))
                elif p.color != self.color:
                    moves.append((j + 1, i + 1))
        if j > 0:
            p = board[i][j - 1]
            if p == 0:
                moves.append((j - 1, i))
            elif p.color != self.color:
                moves.append((j - 1, i))
        if j < 7:
            p = board[i][j + 1]
            if p == 0:
                moves.append((j + 1, i))
            elif p.color != self.color:
                moves.append((j + 1, i))
        return moves


# ----------------------------------------------------------------------------------------------------------------------
class Knight(Piece):
    piece_img = 2

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        if i < 6 and j > 0:
            p = board[i + 2][j - 1]
            if p == 0:
                moves.append((j - 1, i + 2))
            elif p.color != self.color:
                moves.append((j - 1, i + 2))
        if i > 1 and j > 0:
            p = board[i - 2][j - 1]
            if p == 0:
                moves.append((j - 1, i - 2))
            elif p.color != self.color:
                moves.append((j - 1, i - 2))
        if i < 6 and j < 7:
            p = board[i + 2][j + 1]
            if p == 0:
                moves.append((j + 1, i + 2))
            elif p.color != self.color:
                moves.append((j + 1, i + 2))
        if i > 1 and j < 7:
            p = board[i - 2][j + 1]
            if p == 0:
                moves.append((j + 1, i - 2))
            elif p.color != self.color:
                moves.append((j + 1, i - 2))
        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            if p == 0:
                moves.append((j - 2, i - 1))
            elif p.color != self.color:
                moves.append((j - 2, i - 1))
        if i > 0 and j < 6:
            p = board[i - 1][j + 2]
            if p == 0:
                moves.append((j + 2, i - 1))
            elif p.color != self.color:
                moves.append((j + 2, i - 1))
        if i < 7 and j > 1:
            p = board[i + 1][j - 2]
            if p == 0:
                moves.append((j - 2, i + 1))
            elif p.color != self.color:
                moves.append((j - 2, i + 1))
        if i < 7 and j < 6:
            p = board[i + 1][j + 2]
            if p == 0:
                moves.append((j + 2, i + 1))
            elif p.color != self.color:
                moves.append((j + 2, i + 1))
        return moves


# ----------------------------------------------------------------------------------------------------------------------
# noinspection PyBroadException
class Pawn(Piece):
    piece_img = 3

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.queen = False
        self.pawn = True

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        try:
            if self.color == "b":
                if i < 7:
                    p = board[i + 1][j]
                    if p == 0:
                        moves.append((j, i + 1))
                    if j < 7:
                        p = board[i + 1][j + 1]
                        if p != 0:
                            if p.color != self.color:
                                moves.append((j + 1, i + 1))
                    if j > 0:
                        p = board[i + 1][j - 1]
                        if p != 0:
                            if p.color != self.color:
                                moves.append((j - 1, i + 1))
                if self.first:
                    if i < 6:
                        p = board[i + 2][j]
                        p1 = board[i + 1][j]
                        if p1 == 0:
                            moves.append((j, i + 1))
                        if p == 0 and p1 == 0:
                            moves.append((j, i + 2))
            else:
                if i > 0:
                    p = board[i - 1][j]
                    if p == 0:
                        moves.append((j, i - 1))
                if j < 7:
                    p = board[i - 1][j + 1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((j + 1, i - 1))
                if j > 0:
                    p = board[i - 1][j - 1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((j - 1, i - 1))
                if self.first:
                    if i > 1:
                        p = board[i - 2][j]
                        p1 = board[i - 1][j]
                        if p1 == 0:
                            moves.append((j, i - 1))
                        if p == 0 and p1 == 0:
                            moves.append((j, i - 2))
        except:
            print("log: unknown pawn problem")
            return []
        return moves


# ----------------------------------------------------------------------------------------------------------------------
class Queen(Piece):
    piece_img = 4

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        left_strafe = j + 1
        right_strafe = j - 1
        for distance in range(i - 1, -1, -1):
            if left_strafe < 8:
                p = board[distance][left_strafe]
                if p == 0:
                    moves.append((left_strafe, distance))
                elif p.color != self.color:
                    moves.append((left_strafe, distance))
                    break
                else:
                    left_strafe = 9
            left_strafe += 1
        for distance in range(i - 1, -1, -1):
            if right_strafe > -1:
                p = board[distance][right_strafe]
                if p == 0:
                    moves.append((right_strafe, distance))
                elif p.color != self.color:
                    moves.append((right_strafe, distance))
                    break
                else:
                    right_strafe = -1
            right_strafe -= 1
        left_strafe = j + 1
        right_strafe = j - 1
        for distance in range(i + 1, 8):
            if left_strafe < 8:
                p = board[distance][left_strafe]
                if p == 0:
                    moves.append((left_strafe, distance))
                elif p.color != self.color:
                    moves.append((left_strafe, distance))
                    break
                else:
                    left_strafe = 9
            left_strafe += 1
        for distance in range(i + 1, 8):
            if right_strafe > -1:
                p = board[distance][right_strafe]
                if p == 0:
                    moves.append((right_strafe, distance))
                elif p.color != self.color:
                    moves.append((right_strafe, distance))
                    break
                else:
                    right_strafe = -1
            right_strafe -= 1
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        for x in range(j + 1, 8, 1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        return moves


# ----------------------------------------------------------------------------------------------------------------------
class Rook(Piece):
    piece_img = 5

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        for x in range(j + 1, 8, 1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        return moves
