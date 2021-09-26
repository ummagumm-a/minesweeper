import random

from Board import Board
from Cell import Cell

def flatten(l):
    return [item for sublist in l for item in sublist]

# Note: Solver obtains info only about open cells
# and doesn't read info about closed cells except for their existence 
class Solver:
    @staticmethod
    def solve(board):
        while (True):
            board.print_cells()
            # List of open cells
            observed_cells = [t 
                    for t in flatten(board.cells)
                    if t.is_open] 
            # List of closed cells
            closed_cells = [t 
                    for t in flatten(board.cells)
                    if not t.is_open] 
            # List of open cells which have non-zero number 
            # of neighboring bombs
            num_cells = [t 
                    for t in observed_cells 
                    if t.n_bombs != 0]
            # Neighbors of these cells
            num_cells_neighbors = [board.neighbors(t.x, t.y)
                    for t in num_cells]
            # Closed neighbors of these cells
            num_cells_closed_neighbors = [[t 
                    for t in single_cell
                    if not board.cells[t[0]][t[1]].is_open]
                        for single_cell in num_cells_neighbors]
            # Flagged neighbors of these cells
            num_cells_f_neighbors = [[t 
                    for t in single_cell
                    if board.cells[t[0]][t[1]].is_flag]
                        for single_cell in num_cells_neighbors]

            is_end = False
            was_action = False
            # Go through each numbered cell
            for t in range(len(num_cells)):
                # If number of neighboring bombs is equal to number of closed neighbors
                # Flag them all.
                if num_cells[t].n_bombs == len(num_cells_closed_neighbors[t]):
                    for cell in num_cells_closed_neighbors[t]:
                        if not board.cells[cell[0]][cell[1]].is_flag:
                            was_action = True
                            is_end = board.update(cell[0], cell[1], 'Flag')

                # If number of neighboring bombs is equal to number of flagged neighbors
                # open all non-flagged ones
                if num_cells[t].n_bombs == len(num_cells_f_neighbors[t]):
                    for cell in num_cells_closed_neighbors[t]:
                        if not cell in num_cells_f_neighbors[t]:
                            was_action = True
                            is_end = board.update(cell[0], cell[1], 'Open')
            # If we couldn't flag or open a cell on this iteration - 
            # open some randomly chosen closed cell
            if not was_action:
                closed_cells = [t 
                    for t in flatten(board.cells)
                    if not t.is_open and not t.is_flag] 
                cell = random.sample(closed_cells, 1)[0]
                
                is_end = board.update(cell.x, cell.y, "Open")

            # If it is the end of the game
            if is_end:
                print("Game is over!")
                board.print_cells()
                return

