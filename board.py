from piece import Bishop, King, Knight, Rook, Queen, Pawn


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for x in range(8)] for y in range(8)]
        self.set_start()

    def set_start(self):
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
            return True
        return False

    def select(self, col, row, color):
        prev = (-1, -1)
        changed = False
        # print("log:", col, row)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        prev = (i, j)
        if self.board[row][col] == 0:
            try:
                _ = self.board[prev[0]][prev[1]].move_list
            except AttributeError:
                # print("board.select: warning(0) attribute error")
                prev = (-1, -1)
                changed = False
                self.reset_selected()
                return changed
            moves = self.board[prev[0]][prev[1]].move_list
            if (col, row) in moves:
                changed = self.move(prev, (row, col), color)
            self.reset_selected()
        else:
            try:
                _ = self.board[prev[0]][prev[1]].color != self.board[row][col].color
            except AttributeError:
                prev = (-1, -1)
                changed = False
                self.reset_selected()
                return changed
            if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                moves = self.board[prev[0]][prev[1]].move_list
                if (col, row) in moves:
                    changed = self.move(prev, (row, col), color)
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

    def move(self, src, dst, color):
        checked_before = self.is_checked(color)
        changed = True
        new_board = self.board[:]
        try:
            _ = new_board[src[0]][src[1]].pawn
            new_board[src[0]][src[1]].change_pos((dst[0], dst[1]))
        except AttributeError:
            return
        if new_board[src[0]][src[1]].pawn:
            new_board[src[0]][src[1]].first = False
        new_board[dst[0]][dst[1]] = new_board[src[0]][src[1]]
        new_board[src[0]][src[1]] = 0
        self.board = new_board

        if self.is_checked(color) or (checked_before and self.is_checked(color)):
            changed = False
            new_board = self.board
            try:
                _ = new_board[dst[0]][dst[1]].pawn
                new_board[dst[0]][dst[1]].change_pos((src[0], src[1]))
            except AttributeError:
                return
            if new_board[dst[0]][dst[1]].pawn:
                new_board[dst[0]][dst[1]].first = True
            new_board[src[0]][src[1]] = new_board[dst[0]][dst[1]]
            new_board[dst[0]][dst[1]] = 0
            self.board = new_board
        else:
            self.reset_selected()
        self.update_moves()
        return changed
