import pygame
import sys
from constants import *
from Binairo import Binairo

# def new_game():
#     """Placeholder function for starting a new game."""
#     print("New Game clicked! Resetting the grid...")
#     # You can reset the grid or add any logic here
#     global board
#     board = create_board(DEFAULT_GRID_SIZE)  # Reset the board

if __name__ == "__main__":
    game = Binairo()
    game.run()
