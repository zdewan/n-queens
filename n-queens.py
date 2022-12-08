from random import randint


class Board:
    def __init__(self, n:int, board:str = None):
        self.n = n
        self.conflicts = []
        self.queens = {}

        
    def __str__(self):
        sb = []
        sb.append("-" * (self.n+2) + "\n")
        for line in self.board:
            sb.append("|" + "".join(line)+"|")
            sb.append("\n")
        sb.append("-" * (self.n+2))
        return "".join(sb)
    
    def get_queens(self):
        return self.queens

    def get_random_queen(self):
        i = randint(0, self.n-1)
        return self.queens[i]

    def move_queen(self, queen, new_location):
        newX, newY = new_location[0], new_location[1]

        if self.board[newX][newY] == "Q":
            return

        self.board[newX][newY] = "Q"
        self.board[queen[0]][queen[1]] = "."
        self.queens.remove(queen)
        self.queens.append((newX, newY))
        
    def conflicts_at_pos(self, row:int, col:int) -> int:
        """
        Returns number of conflicts at a position
        """
        conflicts = 0

        for r, c in self.queens:
            if (r, c) != (row, col):
                if r == row or c == col or (r+c) == (row+col) or (r-c) == (row-col):
                    conflicts +=1

        return conflicts

    def check_conflicts(self, q):
        for q2 in self.queens:
            if(q == q2):
                continue
            x, y = q
            x2, y2 = q2
            if(x == x2):
                return True
            if(y == y2):
                return True
            if (x+y) == (x2+y2):
                return True
            if (x-y) == (x2-y2):
                return True
        return False
    
    def is_solved(self):
        for q in self.queens:
            if(self.check_conflicts(q)):
                return False
        return True

    def row_conflicts(self):
        print("test")

    def left_diag_conflicts(self):
        print("test")

    def right_diag_conflicts(self):
        print("test")



n = 1_000_000
board = Board(n)

print("Initial board:")
print(board)
num_moves = 0
# while board is not solved
while not board.is_solved():
    q = board.get_random_queen()

    # get set of positions
    pos = []
    for c in range(n):
        if c != q[1]:
            pos.append((q[0], c))

    # calculate set of min conflicts for each position
    num_min_conflicts = n+1
    pos_min_conflicts = (q[0], q[1])
    orig_pos = q
    for r, c in pos:
        if board.board[r][c] == "Q":
            continue
        num_conflicts = board.conflicts_at_pos(r, c)
        if num_conflicts < num_min_conflicts:
            num_min_conflicts = num_conflicts
            pos_min_conflicts = (r, c)
        #print("Conflicts at ({}, {}): {}".format(r, c, num_conflicts))

    board.move_queen(q, pos_min_conflicts)
    num_moves += 1
    #print("Moved queen ({}, {}) -> ({}, {})".format(q[0], q[1], pos_min_conflicts[0], pos_min_conflicts[1]))

print("Solved board:")
print(board)
print("Moves: {}".format(num_moves))