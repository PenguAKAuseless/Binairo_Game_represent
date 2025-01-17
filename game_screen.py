import pygame
from constants import *

def draw_board(screen: pygame.Surface, board_size: int, board: list[list[int]]):
    """Draw the grid based on the board state."""
    # Fill background color
    screen.fill(BACKGROUND_COLOR)

    # Calculate the grid's top-left corner position to center it on the screen
    board_width = board_height = board_size * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS
    board_x_offset = (SCREEN_WIDTH - board_width) // 2
    board_y_offset = (SCREEN_HEIGHT - board_height - BUTTON_HEIGHT - 40) // 2

    # Fill board color
    pygame.draw.rect(screen, BOARD_COLOR, pygame.Rect(
        board_x_offset, board_y_offset, board_width, board_height
    ))

    # Calculate the border position and size
    border_x_offset = board_x_offset - BORDER_THICKNESS
    border_y_offset = board_y_offset - BORDER_THICKNESS
    border_width = board_width + BORDER_THICKNESS * 2
    border_height = board_height + BORDER_THICKNESS * 2

    # Draw the outside border
    pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(
        border_x_offset, border_y_offset, border_width, border_height
    ), BORDER_THICKNESS)

    # Draw grid lines inside the board (green)
    for y in range(board_size + 1):
        pygame.draw.line(screen, GRID_COLOR, 
                         (board_x_offset, board_y_offset + y * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS // 2), 
                         (board_x_offset + board_width - 1, board_y_offset + y * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS // 2), GRID_THICKNESS)
    for x in range(board_size + 1):
        pygame.draw.line(screen, GRID_COLOR, 
                         (board_x_offset + x * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS // 2, board_y_offset), 
                         (board_x_offset + x * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS // 2, board_y_offset + board_height - 1), GRID_THICKNESS)