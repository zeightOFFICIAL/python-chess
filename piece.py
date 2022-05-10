import pygame
import os

# resources -------------------------------------------------
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
# -----------------------------------------------------------

black_all = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
white_all = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]
black_all_scaled = []
white_all_scaled = []


for img in black_all:
    black_all_scaled.append(pygame.transform.smoothscale(img, (scalex_size, scaley_size)))
for img in white_all:
    white_all_scaled.append(pygame.transform.smoothscale(img, (scalex_size, scaley_size)))


class Piece:
    img = -1
    startX = top_left_corner[0]
    startY = top_left_corner[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False
        self.queen = False

    def move(self):
        pass

    def is_selected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def draw(self, win):
        if self.color == "w":
            drawthis = white_all_scaled[self.img]
        else:
            drawthis = black_all_scaled[self.img]
        if self.selected:
            moves = self.move_list
            for move in moves:
                x = self.startX + (move[0] * bot_right_corner[0] / 8) + (scaley_size // 2)
                y = self.startY + (move[1] * bot_right_corner[1] / 8) + (scaley_size // 2)
                pygame.draw.circle(win, (255,0,0), (x,y), 10,)
        x = self.startX + (self.col * bot_right_corner[0]/8)
        y = self.startY + (self.row * bot_right_corner[1]/8)
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x, y, scalex_size, scaley_size), 2)
        win.blit(drawthis, (x, y))

    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def __str__(self):
        return str(self.col) + str(self.row)


class Bishop(Piece):
    img = 0

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []

        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break
            djL += 1
        for di in range(i - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break
            djR -= 1
        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break
            djL += 1
        for di in range(i + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break
            djR -= 1
        return moves


class King(Piece):
    img = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []

        if i > 0:
            # TOP LEFT
            if j > 0:
                p = board[i - 1][j - 1]
                if p == 0:
                    moves.append((j - 1, i - 1,))
                elif p.color != self.color:
                    moves.append((j - 1, i - 1,))
            # TOP MIDDLE
            p = board[i - 1][j]
            if p == 0:
                moves.append((j, i - 1))
            elif p.color != self.color:
                moves.append((j, i - 1))
            # TOP RIGHT
            if j < 7:
                p = board[i - 1][j + 1]
                if p == 0:
                    moves.append((j + 1, i - 1,))
                elif p.color != self.color:
                    moves.append((j + 1, i - 1,))
        if i < 7:
            # BOTTOM LEFT
            if j > 0:
                p = board[i + 1][j - 1]
                if p == 0:
                    moves.append((j - 1, i + 1,))
                elif p.color != self.color:
                    moves.append((j - 1, i + 1,))
            # BOTTOM MIDDLE
            p = board[i + 1][j]
            if p == 0:
                moves.append((j, i + 1))
            elif p.color != self.color:
                moves.append((j, i + 1))
            # BOTTOM RIGHT
            if j < 7:
                p = board[i + 1][j + 1]
                if p == 0:
                    moves.append((j + 1, i + 1))
                elif p.color != self.color:
                    moves.append((j + 1, i + 1))
        # MIDDLE LEFT
        if j > 0:
            p = board[i][j - 1]
            if p == 0:
                moves.append((j - 1, i))
            elif p.color != self.color:
                moves.append((j - 1, i))
        # MIDDLE RIGHT
        if j < 7:
            p = board[i][j + 1]
            if p == 0:
                moves.append((j + 1, i))
            elif p.color != self.color:
                moves.append((j + 1, i))
        return moves


class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []

        # DOWN LEFT
        if i < 6 and j > 0:
            p = board[i + 2][j - 1]
            if p == 0:
                moves.append((j - 1, i + 2))
            elif p.color != self.color:
                moves.append((j - 1, i + 2))
        # UP LEFT
        if i > 1 and j > 0:
            p = board[i - 2][j - 1]
            if p == 0:
                moves.append((j - 1, i - 2))
            elif p.color != self.color:
                moves.append((j - 1, i - 2))
        # DOWN RIGHT
        if i < 6 and j < 7:
            p = board[i + 2][j + 1]
            if p == 0:
                moves.append((j + 1, i + 2))
            elif p.color != self.color:
                moves.append((j + 1, i + 2))
        # UP RIGHT
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


class Pawn(Piece):
    img = 3

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
                    # DIAGONAL
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
                        if p == 0:
                            if board[i + 1][j] == 0:
                                moves.append((j, i + 2))
                        elif p.color != self.color:
                            moves.append((j, i + 2))
            # WHITE
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
                        if p == 0:
                            if board[i - 1][j] == 0:
                                moves.append((j, i - 2))
                        elif p.color != self.color:
                            moves.append((j, i - 2))
        except:
            pass
        return moves


class Queen(Piece):
    img = 4

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []

        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    djL = 9
            djL += 1
        for di in range(i - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    djR = -1
            djR -= 1
        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == 0:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    djL = 9
            djL += 1
        for di in range(i + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    djR = -1
            djR -= 1
        # UP
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        # DOWN
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        # LEFT
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        # RIGHT
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


class Rook(Piece):
    img = 5

    def valid_moves(self, board):
        i = self.row
        j = self.col
        moves = []

        # UP
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        # DOWN
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break
        # LEFT
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break
        # RIGHT
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
