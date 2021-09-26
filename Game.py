import pickle

from Board import Board
from Solver import Solver

class Game:
    @staticmethod
    def enter():
        print("Choose the option:")
        print("1. Run default settings.")
        print("2. Enter board size and amount of bombs.")
        print("3. Load existing game (should be saved before).")

        board = Board(5,5,5)

        inp = input()
        if inp == '2':
            print("Enter values:")
            w, h, n_bombs = map(int, input().split())
            board = Board(w, h, n_bombs)
        elif inp == '3':
            with open('saved.pkl', 'rb') as f:
                board = pickle.load(f)

        print()
        print("Do you want to solve it automatically? (y/n)", end=" ")
        inp = input()
        print()
        if inp == 'y':
            Solver.solve(board)
            return


        print()
        print("List of actions:")
        print("Flag - mark cell with flag.")
        print("Open - open cell.")
        print("Save - save the current game.")
        print()

        Game.main_loop(board)


    @staticmethod
    def main_loop(board):
        board.print_cells()
        while (True):

            print("Make the input in the form [x y Action]:", end=" ")
            inp = input()
            # Save the game if user ascs to
            if inp == 'Save':
                with open('saved.pkl', 'wb') as f:
                    pickle.dump(board, f, protocol=5)
                continue

            x, y, command = inp.split()
            x = int(x) - 1
            y = int(y) - 1

            # Update the board and check whether the game should end
            is_end = False
            if board.coords_in_range(x, y):
                is_end = board.update(x, y, command)

            board.print_cells()

            if is_end:
                break

        print("Game is over")
