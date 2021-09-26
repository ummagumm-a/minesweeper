import random

from Cell import Cell

class Board:
    # Constructor for board
    # Specifies width, height, and number of bombs
    def __init__(self, w, h, n_bombs):
        self.cells = [[Cell(y, x) for x in range(w)] for y in range(h)]
        self.w = w
        self.h = h
        self.n_bombs = n_bombs
        self.open_cells = 0
        # place bombs
        self.gen_bombs(n_bombs)
        # calculate amount of bomb-neighbors for each cell
        self.bomb_neighbors()

    # Place bombs on the board
    def gen_bombs(self, n_bombs):
        sample = [[i,j] for i in range(self.w) for j in range(self.h)]

        cells = random.sample(sample, n_bombs)

        for cell in cells:
            self.cells[cell[0]][cell[1]].is_bomb = True

    # find for each cell how much bombs it has as neighbors
    def bomb_neighbors(self):
        for i in range(self.w):
            for j in range(self.h):
                # retrieve neighbors
                neighs = self.neighbors(i, j)

                # list of bomb-neighbors
                ns_with_bombs = [t 
                        for t in neighs 
                        if self.cells[t[0]][t[1]].is_bomb
                            and not (t[0] == i and t[1] == j)]

                # write number of bomb-neighbors in the cell
                self.cells[i][j].n_bombs = len(ns_with_bombs)

    # return neighbors of this cell
    def neighbors(self, i, j):
        neighbors = [
                (max(0, i - 1), j),
                (max(0, i - 1), max(0, j - 1)),
                (max(0, i - 1), min(self.w - 1, j + 1)),
                (i, min(self.w - 1, j + 1)),
                (i, max(0, j - 1)),
                (min(self.h - 1, i + 1), j),
                (min(self.h - 1, i + 1), min(self.w - 1, j + 1)),
                (min(self.h - 1, i + 1), max(0, j - 1))
            ]

        # remove duplicates
        return list(set(neighbors))

    # Recursively open all adjacent blank cells
    def open_blank(self, x, y, first):
        # If it is already open or marked with flag
        if (self.cells[x][y].is_open
            or self.cells[x][y].is_flag):
            return 
        
        # Obtain neighbors of this cell
        neighs = self.neighbors(x, y)

        # Obtain list of open zero neighbors
        zero_neighs = [t
                for t in neighs
                if self.cells[t[0]][t[1]].is_open and 
                    self.cells[t[0]][t[1]].n_bombs == 0
                ]

        # If it is not a bomb and has at least 1 open zero neighbor
        if (not self.cells[x][y].is_bomb 
                and (first or len(zero_neighs) != 0)):
            self.cells[x][y].is_open = True
            self.open_cells += 1

            self.cells[x][y].update_char()
        else:
            return

        # recursively open all neighbors of this cell
        for t in neighs:
            self.open_blank(t[0], t[1], False);

    # Update state of the board
    def update(self, x, y, command):
        if (command == 'Flag'):
            self.cells[x][y].is_flag = True
        elif (command == 'Unflag'):
            self.cells[x][y].is_flag = False
        elif (self.cells[x][y].is_bomb):
            self.cells[x][y].is_open = True
            print("here")
            self.cells[x][y].update_char()
            return True
        elif (command == 'Open'):
            self.open_blank(x, y, True)
        else: 
            print("Unknown command")

        self.cells[x][y].update_char()
        return self.end_game()

    # Check if input coordinates are in the range of the board
    def coords_in_range(self, x, y):
        return not (x < 0 or x >= self.w or y < 0 or y >= self.h)

    # Check whether number of closed cells is equal to number of bombs
    def end_game(self):
        return self.w * self.h - self.open_cells == self.n_bombs

    # Print board to console
    def print_cells(self):
        print("board")
        print(" " + (1 + 2 * self.w) * "_")
        
        for i in range(self.w):
            print("|", end=" ")
            for j in range(self.h):
                print(self.cells[i][j].char, end=" ")
            print("|")

        print("|" + (1 + 2 * self.w) * "_" + "|")


    # print info about each cell in the board
    def print_info(self):
        for i in range(self.w):
            for j in range(self.h):
                self.cells[i][j].print_info()
            print()


