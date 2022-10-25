# ver 912
# piece.py


# libraries ============================================================================================================
import pygame

# resources ============================================================================================================
from configuration.flowingconfig import *

b_bishop = pygame.image.load("resources/images/b_bishop.png")
b_king = pygame.image.load("resources/images/b_king.png")
b_knight = pygame.image.load("resources/images/b_knight.png")
b_pawn = pygame.image.load("resources/images/b_pawn.png")
b_queen = pygame.image.load("resources/images/b_queen.png")
b_rook = pygame.image.load("resources/images/b_rook.png")
w_bishop = pygame.image.load("resources/images/w_bishop.png")
w_king = pygame.image.load("resources/images/w_king.png")
w_knight = pygame.image.load("resources/images/w_knight.png")
w_pawn = pygame.image.load("resources/images/w_pawn.png")
w_queen = pygame.image.load("resources/images/w_queen.png")
w_rook = pygame.image.load("resources/images/w_rook.png")
raw_select = pygame.image.load("resources/images/b_select.png")
raw_select_inv = pygame.image.load("resources/images/b2_select.png")
if visual_set != 0:
    try:
        b_bishop = pygame.image.load("resources/images/" + str(visual_set) + "/b_bishop.png")
        b_king = pygame.image.load("resources/images/" + str(visual_set) + "/b_king.png")
        b_knight = pygame.image.load("resources/images/" + str(visual_set) + "/b_knight.png")
        b_pawn = pygame.image.load("resources/images/" + str(visual_set) + "/b_pawn.png")
        b_queen = pygame.image.load("resources/images/" + str(visual_set) + "/b_queen.png")
        b_rook = pygame.image.load("resources/images/" + str(visual_set) + "/b_rook.png")
        w_bishop = pygame.image.load("resources/images/" + str(visual_set) + "/w_bishop.png")
        w_king = pygame.image.load("resources/images/" + str(visual_set) + "/w_king.png")
        w_knight = pygame.image.load("resources/images/" + str(visual_set) + "/w_knight.png")
        w_pawn = pygame.image.load("resources/images/" + str(visual_set) + "/w_pawn.png")
        w_queen = pygame.image.load("resources/images/" + str(visual_set) + "/w_queen.png")
        w_rook = pygame.image.load("resources/images/" + str(visual_set) + "/w_rook.png")
        raw_select = pygame.image.load("resources/images/" + str(visual_set) + "/b_select.png")
        raw_select_inv = pygame.image.load("resources/images/" + str(visual_set) + "/b2_select.png")
    except (FileNotFoundError, FileExistsError, TypeError) as e:
        logging.debug("Load visual set: custom visual set cannot be loaded")
black_all_images = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
white_all_images = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]
black_all_scaled = []
white_all_scaled = []

# scaling --------------------------------------------------------------------------------------------------------------
for piece_img in black_all_images:
    black_all_scaled.append(pygame.transform.smoothscale(piece_img, (CELL_SIZE_X, CELL_SIZE_Y)))
for piece_img in white_all_images:
    white_all_scaled.append(pygame.transform.smoothscale(piece_img, (CELL_SIZE_X, CELL_SIZE_Y)))
scaled_select = pygame.transform.smoothscale(raw_select, (CELL_SIZE_X, CELL_SIZE_Y))
scaled_select2 = pygame.transform.smoothscale(raw_select_inv, (CELL_SIZE_X, CELL_SIZE_Y))


# piece class ==========================================================================================================
class Piece:
    piece_img = -1
    start_x = TOP_LEFT[0]
    start_y = TOP_LEFT[1]

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
                x = self.start_x + (move[0] * BOTTOM_RIGHT[0] / 8) + (CELL_SIZE_Y // 2)
                y = self.start_y + (move[1] * BOTTOM_RIGHT[1] / 8) + (CELL_SIZE_Y // 2)
                if self.color == "w":
                    win.blit(scaled_select, (x - CELL_SIZE_X / 2, y - CELL_SIZE_Y / 2))
                if self.color == 'b':
                    win.blit(scaled_select2, (x - CELL_SIZE_X / 2, y - CELL_SIZE_Y / 2))
        x = self.start_x + (self.col * BOTTOM_RIGHT[0] / 8)
        y = self.start_y + (self.row * BOTTOM_RIGHT[1] / 8)
        if self.selected:
            if self.color == "w":
                this_piece_img = pygame.transform.smoothscale(white_all_images[self.piece_img],
                                                              (CELL_SIZE_Y + POP_INCREASING_SIZE,
                                                               CELL_SIZE_Y + POP_INCREASING_SIZE))
            if self.color == 'b':
                this_piece_img = pygame.transform.smoothscale(black_all_images[self.piece_img],
                                                              (CELL_SIZE_Y + POP_INCREASING_SIZE,
                                                               CELL_SIZE_Y + POP_INCREASING_SIZE))
            win.blit(this_piece_img, (x - POP_INCREASING_SIZE / 2, y - POP_INCREASING_SIZE / 2))
        else:
            win.blit(this_piece_img, (x, y))

    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def valid_moves(self, board):
        pass


# pieces' implementations, inherited ===================================================================================
class Bishop(Piece):
    piece_img = 0

    def valid_moves(self, board):
        to_row = self.row
        to_col = self.col
        moves = []
        left_strafe = to_col + 1
        right_strafe = to_col - 1
        for distance in range(to_row - 1, -1, -1):
            if left_strafe < 8:
                next_point = board[distance][left_strafe]
                if next_point == 0:
                    moves.append((left_strafe, distance))
                elif next_point.color != self.color:
                    moves.append((left_strafe, distance))
                    break
                else:
                    break
            else:
                break
            left_strafe += 1
        for distance in range(to_row - 1, -1, -1):
            if right_strafe > -1:
                next_point = board[distance][right_strafe]
                if next_point == 0:
                    moves.append((right_strafe, distance))
                elif next_point.color != self.color:
                    moves.append((right_strafe, distance))
                    break
                else:
                    break
            else:
                break
            right_strafe -= 1
        left_strafe = to_col + 1
        right_strafe = to_col - 1
        for distance in range(to_row + 1, 8):
            if left_strafe < 8:
                next_point = board[distance][left_strafe]
                if next_point == 0:
                    moves.append((left_strafe, distance))
                elif next_point.color != self.color:
                    moves.append((left_strafe, distance))
                    break
                else:
                    break
            else:
                break
            left_strafe += 1
        for distance in range(to_row + 1, 8):
            if right_strafe > -1:
                next_point = board[distance][right_strafe]
                if next_point == 0:
                    moves.append((right_strafe, distance))
                elif next_point.color != self.color:
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
        to_row = self.row
        to_col = self.col
        moves = []
        if to_row > 0:
            if to_col > 0:
                next_point = board[to_row - 1][to_col - 1]
                if next_point == 0:
                    moves.append((to_col - 1, to_row - 1,))
                elif next_point.color != self.color:
                    moves.append((to_col - 1, to_row - 1,))
            next_point = board[to_row - 1][to_col]
            if next_point == 0:
                moves.append((to_col, to_row - 1))
            elif next_point.color != self.color:
                moves.append((to_col, to_row - 1))
            if to_col < 7:
                next_point = board[to_row - 1][to_col + 1]
                if next_point == 0:
                    moves.append((to_col + 1, to_row - 1,))
                elif next_point.color != self.color:
                    moves.append((to_col + 1, to_row - 1,))
        if to_row < 7:
            if to_col > 0:
                next_point = board[to_row + 1][to_col - 1]
                if next_point == 0:
                    moves.append((to_col - 1, to_row + 1,))
                elif next_point.color != self.color:
                    moves.append((to_col - 1, to_row + 1,))
            next_point = board[to_row + 1][to_col]
            if next_point == 0:
                moves.append((to_col, to_row + 1))
            elif next_point.color != self.color:
                moves.append((to_col, to_row + 1))
            if to_col < 7:
                next_point = board[to_row + 1][to_col + 1]
                if next_point == 0:
                    moves.append((to_col + 1, to_row + 1))
                elif next_point.color != self.color:
                    moves.append((to_col + 1, to_row + 1))
        if to_col > 0:
            next_point = board[to_row][to_col - 1]
            if next_point == 0:
                moves.append((to_col - 1, to_row))
            elif next_point.color != self.color:
                moves.append((to_col - 1, to_row))
        if to_col < 7:
            next_point = board[to_row][to_col + 1]
            if next_point == 0:
                moves.append((to_col + 1, to_row))
            elif next_point.color != self.color:
                moves.append((to_col + 1, to_row))
        return moves


# ----------------------------------------------------------------------------------------------------------------------
class Knight(Piece):
    piece_img = 2

    def valid_moves(self, board):
        to_row = self.row
        to_col = self.col
        moves = []
        if to_row < 6 and to_col > 0:
            next_point = board[to_row + 2][to_col - 1]
            if next_point == 0:
                moves.append((to_col - 1, to_row + 2))
            elif next_point.color != self.color:
                moves.append((to_col - 1, to_row + 2))
        if to_row > 1 and to_col > 0:
            next_point = board[to_row - 2][to_col - 1]
            if next_point == 0:
                moves.append((to_col - 1, to_row - 2))
            elif next_point.color != self.color:
                moves.append((to_col - 1, to_row - 2))
        if to_row < 6 and to_col < 7:
            next_point = board[to_row + 2][to_col + 1]
            if next_point == 0:
                moves.append((to_col + 1, to_row + 2))
            elif next_point.color != self.color:
                moves.append((to_col + 1, to_row + 2))
        if to_row > 1 and to_col < 7:
            next_point = board[to_row - 2][to_col + 1]
            if next_point == 0:
                moves.append((to_col + 1, to_row - 2))
            elif next_point.color != self.color:
                moves.append((to_col + 1, to_row - 2))
        if to_row > 0 and to_col > 1:
            next_point = board[to_row - 1][to_col - 2]
            if next_point == 0:
                moves.append((to_col - 2, to_row - 1))
            elif next_point.color != self.color:
                moves.append((to_col - 2, to_row - 1))
        if to_row > 0 and to_col < 6:
            next_point = board[to_row - 1][to_col + 2]
            if next_point == 0:
                moves.append((to_col + 2, to_row - 1))
            elif next_point.color != self.color:
                moves.append((to_col + 2, to_row - 1))
        if to_row < 7 and to_col > 1:
            next_point = board[to_row + 1][to_col - 2]
            if next_point == 0:
                moves.append((to_col - 2, to_row + 1))
            elif next_point.color != self.color:
                moves.append((to_col - 2, to_row + 1))
        if to_row < 7 and to_col < 6:
            next_point = board[to_row + 1][to_col + 2]
            if next_point == 0:
                moves.append((to_col + 2, to_row + 1))
            elif next_point.color != self.color:
                moves.append((to_col + 2, to_row + 1))
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
        to_row = self.row
        to_col = self.col
        moves = []
        try:
            if self.color == "b":
                if to_row < 7:
                    next_point = board[to_row + 1][to_col]
                    if next_point == 0:
                        moves.append((to_col, to_row + 1))
                    if to_col < 7:
                        next_point = board[to_row + 1][to_col + 1]
                        if next_point != 0:
                            if next_point.color != self.color:
                                moves.append((to_col + 1, to_row + 1))
                    if to_col > 0:
                        next_point = board[to_row + 1][to_col - 1]
                        if next_point != 0:
                            if next_point.color != self.color:
                                moves.append((to_col - 1, to_row + 1))
                if self.first:
                    if to_row < 6:
                        next_point = board[to_row + 2][to_col]
                        next_point_two = board[to_row + 1][to_col]
                        if next_point_two == 0:
                            moves.append((to_col, to_row + 1))
                        if next_point == 0 and next_point_two == 0:
                            moves.append((to_col, to_row + 2))
            else:
                if to_row > 0:
                    next_point = board[to_row - 1][to_col]
                    if next_point == 0:
                        moves.append((to_col, to_row - 1))
                if to_col < 7:
                    next_point = board[to_row - 1][to_col + 1]
                    if next_point != 0:
                        if next_point.color != self.color:
                            moves.append((to_col + 1, to_row - 1))
                if to_col > 0:
                    next_point = board[to_row - 1][to_col - 1]
                    if next_point != 0:
                        if next_point.color != self.color:
                            moves.append((to_col - 1, to_row - 1))
                if self.first:
                    if to_row > 1:
                        next_point = board[to_row - 2][to_col]
                        next_point_two = board[to_row - 1][to_col]
                        if next_point_two == 0:
                            moves.append((to_col, to_row - 1))
                        if next_point == 0 and next_point_two == 0:
                            moves.append((to_col, to_row - 2))
        except:
            logging.warning("pawn class: Unresolved pawn problem.")
            return []
        return moves


# ----------------------------------------------------------------------------------------------------------------------
class Queen(Piece):
    piece_img = 4

    def valid_moves(self, board):
        to_row = self.row
        to_col = self.col
        moves = []
        left_strafe = to_col + 1
        right_strafe = to_col - 1
        for distance in range(to_row - 1, -1, -1):
            if left_strafe < 8:
                next_point = board[distance][left_strafe]
                if next_point == 0:
                    moves.append((left_strafe, distance))
                elif next_point.color != self.color:
                    moves.append((left_strafe, distance))
                    break
                else:
                    left_strafe = 9
            left_strafe += 1
        for distance in range(to_row - 1, -1, -1):
            if right_strafe > -1:
                next_point = board[distance][right_strafe]
                if next_point == 0:
                    moves.append((right_strafe, distance))
                elif next_point.color != self.color:
                    moves.append((right_strafe, distance))
                    break
                else:
                    right_strafe = -1
            right_strafe -= 1
        left_strafe = to_col + 1
        right_strafe = to_col - 1
        for distance in range(to_row + 1, 8):
            if left_strafe < 8:
                next_point = board[distance][left_strafe]
                if next_point == 0:
                    moves.append((left_strafe, distance))
                elif next_point.color != self.color:
                    moves.append((left_strafe, distance))
                    break
                else:
                    left_strafe = 9
            left_strafe += 1
        for distance in range(to_row + 1, 8):
            if right_strafe > -1:
                next_point = board[distance][right_strafe]
                if next_point == 0:
                    moves.append((right_strafe, distance))
                elif next_point.color != self.color:
                    moves.append((right_strafe, distance))
                    break
                else:
                    right_strafe = -1
            right_strafe -= 1
        for x in range(to_row - 1, -1, -1):
            next_point = board[x][to_col]
            if next_point == 0:
                moves.append((to_col, x))
            elif next_point.color != self.color:
                moves.append((to_col, x))
                break
            else:
                break
        for x in range(to_row + 1, 8, 1):
            next_point = board[x][to_col]
            if next_point == 0:
                moves.append((to_col, x))
            elif next_point.color != self.color:
                moves.append((to_col, x))
                break
            else:
                break
        for x in range(to_col - 1, -1, -1):
            next_point = board[to_row][x]
            if next_point == 0:
                moves.append((x, to_row))
            elif next_point.color != self.color:
                moves.append((x, to_row))
                break
            else:
                break
        for x in range(to_col + 1, 8, 1):
            next_point = board[to_row][x]
            if next_point == 0:
                moves.append((x, to_row))
            elif next_point.color != self.color:
                moves.append((x, to_row))
                break
            else:
                break
        return moves


# ----------------------------------------------------------------------------------------------------------------------
class Rook(Piece):
    piece_img = 5

    def valid_moves(self, board):
        to_row = self.row
        to_col = self.col
        moves = []
        for x in range(to_row - 1, -1, -1):
            next_point = board[x][to_col]
            if next_point == 0:
                moves.append((to_col, x))
            elif next_point.color != self.color:
                moves.append((to_col, x))
                break
            else:
                break
        for x in range(to_row + 1, 8, 1):
            next_point = board[x][to_col]
            if next_point == 0:
                moves.append((to_col, x))
            elif next_point.color != self.color:
                moves.append((to_col, x))
                break
            else:
                break
        for x in range(to_col - 1, -1, -1):
            next_point = board[to_row][x]
            if next_point == 0:
                moves.append((x, to_row))
            elif next_point.color != self.color:
                moves.append((x, to_row))
                break
            else:
                break
        for x in range(to_col + 1, 8, 1):
            next_point = board[to_row][x]
            if next_point == 0:
                moves.append((x, to_row))
            elif next_point.color != self.color:
                moves.append((x, to_row))
                break
            else:
                break
        return moves
