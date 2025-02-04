import pygame
import sys
import random

from constants import *
from Circle import Circle


class Binairo:
    class BinairoCircle(Circle): 
        def __init__(self, radius : int = CELL_SIZE // 2, position: tuple[int] = (0, 0), color : tuple[int] = TRANSPARENT, canUpdate : bool = False) -> None:
            super().__init__(radius, position, color)
            self.canUpdate = canUpdate

            if not canUpdate:
                # Draw a small middle square at the circle center
                square_size = SQUARE_CONCRETE_SIZE

                # Calculate the square's position
                square_x = square_y = radius - square_size // 2

                # Draw the square
                pygame.draw.rect(self.image, SQUARE_CONCRETE_COLOR, (square_x, square_y, square_size, square_size))


        def update(self, pos: tuple[int] = None, color: tuple[int] = None) -> None:
            """Update the circle's position and color."""
            if self.canUpdate:
                super().update(pos, color)

    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Binairo")

        self._running = True

        self.board_size = MIN_BOARD_SIZE
        self.board = self.generate_binairo_board(self.board_size)
        self.remove_cells(self.board_size - self.board_size // 4 - 1)

        self.draw_board()

        # INSERT BOARD ERASING CODE HERE

        self.circle_board = []
        self.all_sprites = pygame.sprite.Group()
        for i in range(self.board_size):
            temp = []
            for j in range(self.board_size):
                # Calculate the circle position
                circle_x_offset = self.board_x_offset + j * (CELL_SIZE + GRID_THICKNESS) + CELL_SIZE // 2 + GRID_THICKNESS // 2 + 2
                circle_y_offset = self.board_y_offset + i * (CELL_SIZE + GRID_THICKNESS) + CELL_SIZE // 2 + GRID_THICKNESS // 2 + 2
                if self.board[i][j] == 1:
                    temp.append(self.BinairoCircle(position=(circle_x_offset, circle_y_offset), color=WHITE))
                    self.all_sprites.add(temp[-1])
                elif self.board[i][j] == 0:
                    temp.append(self.BinairoCircle(position=(circle_x_offset, circle_y_offset), color=BLACK))
                    self.all_sprites.add(temp[-1])
                else:
                    temp.append(self.BinairoCircle(position=(circle_x_offset, circle_y_offset), canUpdate=True))
                    self.all_sprites.add(temp[-1])
            self.circle_board.append(temp)

    def generate_binairo_board(self, n: int) -> list[list[int]]:
        # Init board
        board = [[None for _ in range(n)] for _ in range(n)]

        # Init trace board
        trace_board = [[False for _ in range(n)] for _ in range(n)]

        # Init counter to keep track of board constructor
        count = 0

        # Function to check streak of 0s 1s
        def check_streak(i, j, board) -> bool:
            if j >= 2 and board[i][j - 2] == board[i][j - 1] and board[i][j - 1] == board[i][j]:
                return False
            if i >= 2 and board[i - 2][j] == board[i - 1][j] and board[i - 1][j] == board[i][j]:
                return False
            return True

        def check_count(i, j, board) -> bool:
            if j == n - 1 and sum(board[i]) != n // 2:
                return False
            if i == n - 1 and sum(board[row][j] for row in range(n)) != n // 2:
                return False
            return True
        
        def check_unique(i, j, board) -> bool:
            # Check row
            if j == n - 1 and i != 0:
                for row in range(i):
                    if board[i] == board[row]:
                        return False

            # Check col
            if i == n - 1 and j != 0:
                for col in range(j):
                    if [board[row][j] for row in range(n)] == [board[row][col] for row in range(n)]:
                        return False
            
            # Passed both, return True
            return True
        
        while count < n * n:
            i, j = count // n, count % n
            # If trace True, erase trace and board, then go back one cell
            if trace_board[i][j] == True:
                trace_board[i][j] = False
                board[i][j] = None
                count -= 1
                continue

            # If board[i][j] already has a value, flip it and mark trace True, else random it
            if board[i][j] != None:
                board[i][j] = 1 - board[i][j]
                trace_board[i][j] = True
            else:
                board[i][j] = random.randint(0, 1)

            # Check all condition
            if check_streak(i, j, board) and check_count(i, j, board) and check_unique(i, j, board):
                count += 1

        return board

    def draw_board(self) -> None:
        """Draw the grid based on the board state."""
        # Fill background color
        self.screen.fill(BACKGROUND_COLOR)

        # Calculate the grid's top-left corner position to center it on the screen
        self.board_width = self.board_height = self.board_size * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS
        self.board_x_offset = (SCREEN_WIDTH - self.board_width) // 2
        self.board_y_offset = (SCREEN_HEIGHT - self.board_height - BUTTON_HEIGHT - 40) // 2

        # Fill board color
        pygame.draw.rect(self.screen, BOARD_COLOR, pygame.Rect(
            self.board_x_offset, self.board_y_offset, self.board_width, self.board_height
        ))

        # Calculate the border position and size
        border_x_offset = self.board_x_offset - BORDER_THICKNESS
        border_y_offset = self.board_y_offset - BORDER_THICKNESS
        border_width = self.board_width + BORDER_THICKNESS * 2
        border_height = self.board_height + BORDER_THICKNESS * 2

        # Draw the outside border
        pygame.draw.rect(self.screen, BORDER_COLOR, pygame.Rect(
            border_x_offset, border_y_offset, border_width, border_height
        ), BORDER_THICKNESS)

        # Draw grid lines inside the board (green)
        for y in range(self.board_size + 1):
            pygame.draw.line(self.screen, GRID_COLOR, 
                            (self.board_x_offset, self.board_y_offset + y * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS // 2), 
                            (self.board_x_offset + self.board_width - 1, self.board_y_offset + y * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS // 2), GRID_THICKNESS)
        for x in range(self.board_size + 1):
            pygame.draw.line(self.screen, GRID_COLOR, 
                            (self.board_x_offset + x * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS // 2, self.board_y_offset), 
                            (self.board_x_offset + x * (CELL_SIZE + GRID_THICKNESS) + GRID_THICKNESS // 2, self.board_y_offset + self.board_height - 1), GRID_THICKNESS)
            
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle the event based on the event type."""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in [1, 3]:  # Left or right mouse button
                self.handle_click(event.pos, event.button)

    def handle_click(self, pos : tuple[int], button: int) -> None:
        """Handle the user click to toggle between 0 and 1 based on the mouse button."""
        x, y = pos

        # Adjust position to account for the border
        x -= self.board_x_offset + GRID_THICKNESS // 2
        y -= self.board_y_offset + GRID_THICKNESS // 2
        grid_x = x // (CELL_SIZE + GRID_THICKNESS)
        grid_y = y // (CELL_SIZE + GRID_THICKNESS)

        # Check if the click is inside the grid
        if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size and self.circle_board[grid_y][grid_x].canUpdate:
            if button == 1:  # Left click
                if self.circle_board[grid_y][grid_x].color == WHITE:
                    self.circle_board[grid_y][grid_x].set_color = TRANSPARENT
                else:
                    self.circle_board[grid_y][grid_x].color = WHITE
            elif button == 3:  # Right click
                if self.circle_board[grid_y][grid_x].color == BLACK:
                    self.circle_board[grid_y][grid_x].color = TRANSPARENT
                else:
                    self.circle_board[grid_y][grid_x].color = WHITE

    def validate(self):
        # Check consecutive streaks of 1s or 0s
        for i in range(self.board_size - 2):
            for j in range(self.board_size - 2):
                if self.board[i][j] == self.board[i + 1][j] and self.board[i + 1][j] == self.board[i + 2][j]:
                    return False
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j + 1] == self.board[i][j + 2]:
                    return False
        
        # Check row and col validity
        row_set = set()
        col_set = set()
        for i in range(self.board_size):
                if sum(self.board[i]) != self.board_size // 2:
                    return False
                row_num = int(''.join(map(str, self.board[i])), 2)
                if row_num in row_set:
                    print(row_num)
                    return False
                else:
                    row_set.add(row_num)

        for j in range(self.board_size):
                if sum(self.board[row][j] for row in range(self.board_size)) != self.board_size // 2:
                    return False
                col_num = int(''.join(map(str, [self.board[row][j] for row in range(self.board_size)])), 2)
                if col_num in col_set:
                    print("Col ", i)
                    return False
                else:
                    col_set.add(col_num)
        
        return True

    def update_display(self) -> None:
        """Update the display with the current state of the board."""
        pass
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.circle_board[y][x].canUpdate:
                    color = WHITE if self.board[y][x] == 1 else BLACK
                    self.circle_board[y][x].set_color(color)
        self.all_sprites.draw(self.screen)

    def is_valid_move(self, row: int, col: int) -> bool:
        
        # Check if exist streak 3 in a row at the placement
        for i in range(3):
            if col + i < 2 or col + i >= self.board_size:
                continue
            if self.board[row][col + i - 2] == self.board[row][col + i - 1] and self.board[row][col + i - 1] == self.board[row][col + i]:
                return False
        
        # Check if exist streak 3 in a col at the placement
        for i in range(3):
            if row + i < 2 or row + i >= self.board_size:
                continue
            if self.board[row + i - 2][col] == self.board[row + i - 1][col] and self.board[row + i - 1][col] == self.board[row + i][col]:
                return False
            
        # Check if the row contains None, if not, check if the row is valid
        if None not in self.board[row]:
            if sum(self.board[row]) != self.board_size // 2:
                return False
            for row in range(self.board_size):
                if self.board[row] == self.board[row]:
                    return False
        
        # Check if the col contains None, if not, check if the col is valid
        if None not in [self.board[row][col] for row in range(self.board_size)]:
            if sum([self.board[row][col] for row in range(self.board_size)]) != self.board_size // 2:
                return False
            for col in range(self.board_size):
                if [self.board[row][col] for row in range(self.board_size)] == [self.board[row][col] for row in range(self.board_size)]:
                    return False

        # If all checks passed, return True
        return True

    def solve_binairo(self) -> bool:  
        def dfs(row, col):
            if row == self.board_size:  # If we've reached past the last row, solution found
                return True
            
            next_row, next_col = (row, col + 1) if col + 1 < self.board_size else (row + 1, 0)
            
            if self.temp_board[row][col] != None:  # Skip pre-filled cells
                return dfs(next_row, next_col)
            
            for num in [0, 1]:
                self.temp_board[row][col] = num
                if self.is_valid_move(row, col) and dfs(next_row, next_col):
                    return True
                self.temp_board[row][col] = None  # Undo move if it didn't lead to a solution
            
            return False
        
        # Copy the board to avoid modifying the original board
        self.temp_board = [row[:] for row in self.board]
        return dfs(0, 0)

    def remove_cells(self, n: int) -> None:
        """Remove n cells from the board."""
        removed = 0
        while removed < n:
            row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            if self.board[row][col] != None:
                self.board[row][col] = 1 - self.board[row][col]
                if not self.is_valid_move(row, col):
                    self.board[row][col] = None
                    removed += 1
                    continue
                if not self.solve_binairo():
                    self.board[row][col] = None
                    removed += 1
                    continue

    def run(self) -> None:
        """Main game loop."""

        for row in self.board:
            print(row)

        while self._running:
            events = pygame.event.get()
            for event in events:
                self.handle_events(event)
            self.update_display()
            pygame.display.flip()
