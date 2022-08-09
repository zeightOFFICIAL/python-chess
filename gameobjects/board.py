# ver 904
# board.py
# project libraries ====================================================================================================
from gameobjects.piece import Bishop, King, Knight, Rook, Queen, Pawn


# chessboard class =====================================================================================================
# noinspection PyTypeChecker (PyCharm throws a warning considering unexpected value in 2d array. Class instead of '0' being integer)
class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.set_start_normal()

    def set_start_normal(self):
        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")
        for line in range(0, 8):
            self.board[1][line] = Pawn(1, line, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")
        for line in range(0, 8):
            self.board[6][line] = Pawn(6, line, "w")

# functions ============================================================================================================
    def update_moves(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)

    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win)

    def get_danger_moves(self, color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        for move in self.board[i][j].move_list:
                            danger_moves.append(move)
        return danger_moves

    def is_attheend(self, color):
        if color == "w":
            i = 0
            for j in range(0, 8):
                if self.board[i][j] != 0:
                    if self.board[i][j].pawn:
                        self.board[i][j] = 0
                        self.board[i][j] = Queen(i, j, color)
                        print("log: pawn to queen", color)
        if color == "b":
            i = 7
            for j in range(0, 8):
                if self.board[i][j] != 0:
                    if self.board[i][j].pawn:
                        self.board[i][j] = 0
                        self.board[i][j] = Queen(i, j, color)
                        print("log: pawn to queen", color)

    def is_checked(self, color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].king and self.board[i][j].color == color:
                        king_pos = (j, i)
        if king_pos in danger_moves:
            print("log: checked", color)
            return True
        return False

    def select(self, col, row, color):
        previous_select = (-1, -1)
        changed = False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        previous_select = (i, j)
        if self.board[row][col] == 0 and previous_select != (-1, -1):
            moves = self.board[previous_select[0]
                               ][previous_select[1]].move_list
            if (col, row) in moves:
                changed = self.move(previous_select, (row, col), color)
            self.reset_selected()
        else:
            if previous_select == (-1, -1):
                self.reset_selected()
                if self.board[row][col] != 0 and self.board[row][col].color == color:
                    self.board[row][col].selected = True
            else:
                if self.board[previous_select[0]][previous_select[1]].color != self.board[row][col].color:
                    moves = self.board[previous_select[0]
                                       ][previous_select[1]].move_list
                    if (col, row) in moves:
                        changed = self.move(previous_select, (row, col), color)
                    self.reset_selected()
                    if self.board[row][col].color == color:
                        self.board[row][col].selected = True
                else:
                    self.reset_selected()
                    if self.board[row][col].color == color:
                        self.board[row][col].selected = True
        return changed

    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

# 'move' for player ----------------------------------------------------------------------------------------------------
    def move(self, src, dst, color):
        checked_before = self.is_checked(color)
        changed = True
        new_board = self.board[:]
        if self.is_checked(color) and not (checked_before and self.is_checked(color)):
            changed = False
            new_board = self.board[:]
            new_board[dst[0]][dst[1]].change_pos((src[0], src[1]))
            if new_board[dst[0]][dst[1]].pawn:
                new_board[dst[0]][dst[1]].first = True
            new_board[dst[0]][dst[1]].change_pos((src[0], src[1]))
            new_board[src[0]][src[1]] = new_board[dst[0]][dst[1]]
            new_board[dst[0]][dst[1]] = 0
            self.board = new_board
        else:
            self.reset_selected()
        if new_board[src[0]][src[1]].pawn:
            new_board[src[0]][src[1]].first = False
        new_board[src[0]][src[1]].change_pos((dst[0], dst[1]))
        new_board[dst[0]][dst[1]] = new_board[src[0]][src[1]]
        new_board[src[0]][src[1]] = 0
        self.board = new_board
        self.is_attheend(color)
        self.update_moves()
        return changed

# 'move' for chess algorithm -------------------------------------------------------------------------------------------
    def simple_move(self, src, dst, color):
        new_board = self.board[:]
        if new_board[src[0]][src[1]].pawn:
            new_board[src[0]][src[1]].first = False
        new_board[src[0]][src[1]].change_pos((dst[0], dst[1]))
        new_board[dst[0]][dst[1]] = new_board[src[0]][src[1]]
        new_board[src[0]][src[1]] = 0
        self.board = new_board
        self.is_attheend(color)
        self.update_moves()
