from piece import Bishop, King, Knight, Rook, Queen, Pawn


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for x in range(8)] for y in range(8)]
        self.anyselected = False
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
        #for line in range(0, 7):
        #    self.board[6][line] = Pawn(6, line, "w")

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

    def select(self, col, row):
        prev = (-1, -1)
        # print("log:", self.anyselected, col, row)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        prev = (i, j)
        if self.board[row][col] == 0:
            moves = self.board[prev[0]][prev[1]].move_list
            if (col, row) in moves:
                self.move(prev, (row, col))
            self.reset_selected()
        else:
            if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                moves = self.board[prev[0]][prev[1]].move_list
                if (col, row) in moves:
                    self.move(prev, (row, col))
                self.reset_selected()
                self.board[row][col].selected = True
                self.anyselected = True
            else:
                self.reset_selected()
                self.board[row][col].selected = True
                self.anyselected = True


    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False
        self.anyselected = False

    def move(self, src, dst):
        nBoard = self.board[:]
        nBoard[src[0]][src[1]].change_pos((dst[0], dst[1]))
        nBoard[dst[0]][dst[1]] = nBoard[src[0]][src[1]]
        nBoard[src[0]][src[1]] = 0
        self.board = nBoard
