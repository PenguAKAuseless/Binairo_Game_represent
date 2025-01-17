import pygame
import sys
from game_screen import draw_board
from binairo_generator import generate_binairo_board
from constants import *

# def handle_click(pos, button, grid_size):
#     """Handle the user click to toggle between 0 and 1 based on the mouse button."""
#     x, y = pos
#     # Calculate grid offsets
#     grid_width = CELL_SIZE * grid_size + BORDER_THICKNESS * 2
#     grid_height = CELL_SIZE * grid_size + BORDER_THICKNESS * 2
#     grid_x_offset = (SCREEN_WIDTH - grid_width) // 2
#     grid_y_offset = (SCREEN_HEIGHT - grid_height - button_height - 20) // 2

#     # Adjust position to account for the border
#     x -= grid_x_offset + BORDER_THICKNESS
#     y -= grid_y_offset + BORDER_THICKNESS
#     grid_x = x // CELL_SIZE
#     grid_y = y // CELL_SIZE

#     # Check if the click is inside the grid
#     if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
#         if button == 1:  # Left click
#             board[grid_y][grid_x] = 1 - board[grid_y][grid_x]  # Toggle between 0 and 1
#         elif button == 3:  # Right click
#             board[grid_y][grid_x] = 0  # Set to 0 (black)
    
#     # Check if the click is inside the "NEW GAME" button area
#     if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
#         if button == 1:  # Left click
#             new_game()  # Placeholder for button functionality

# def new_game():
#     """Placeholder function for starting a new game."""
#     print("New Game clicked! Resetting the grid...")
#     # You can reset the grid or add any logic here
#     global board
#     board = create_board(DEFAULT_GRID_SIZE)  # Reset the board

def main():
    """Main game loop."""
    # Initialize pygame
    pygame.init()


    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Binairo")
    board_size = 10  # Start with a 10x10 grid size
    
    # Create the board with the current grid size
    board = generate_binairo_board(board_size)

    while True:
        draw_board(screen, board_size, board)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button in [1, 3]:  # Left or right mouse button
            #         handle_click(event.pos, event.button, grid_size)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
