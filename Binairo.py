import pygame
import sys
import random
import time
import tracemalloc

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
        self.remove_cells(self.board_size * self.board_size * 3 // 4 + 1)

        self.draw_board()

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
        if n % 2 != 0:
            raise ValueError("Board size must be even.")

        # Init board with -1 to indicate empty cells
        board = [[-1 for _ in range(n)] for _ in range(n)]

        # Function to check streak of 0s and 1s
        def check_streak(i, j, board) -> bool:
            # Check row streaks
            if j >= 2 and board[i][j] == board[i][j-1] == board[i][j-2]:
                return False
            if j < n - 2 and board[i][j] == board[i][j+1] == board[i][j+2]:
                return False
            if 0 < j < n - 1 and board[i][j] == board[i][j-1] == board[i][j+1]:
                return False
            
            # Check column streaks
            if i >= 2 and board[i][j] == board[i-1][j] == board[i-2][j]:
                return False
            if i < n - 2 and board[i][j] == board[i+1][j] == board[i+2][j]:
                return False
            if 0 < i < n - 1 and board[i][j] == board[i-1][j] == board[i+1][j]:
                return False
            
            return True

        # Function to check count of 0s and 1s
        def check_count(i, j, board) -> bool:
            # Check row counts
            if board[i].count(0) > n // 2 or board[i].count(1) > n // 2:
                return False
            
            # Check column counts
            col_count_0 = sum(board[row][j] == 0 for row in range(n))
            col_count_1 = sum(board[row][j] == 1 for row in range(n))
            if col_count_0 > n // 2 or col_count_1 > n // 2:
                return False
            
            return True

        # Function to check uniqueness of rows and columns
        def check_unique(i, j, board) -> bool:
            # Check row uniqueness if row is fully filled
            if -1 not in board[i]:
                for row in range(n):
                    if row != i and board[row] == board[i]:
                        return False
            
            # Check column uniqueness if column is fully filled
            current_col = [board[row][j] for row in range(n)]
            if -1 not in current_col:
                for col in range(n):
                    if col != j:
                        other_col = [board[row][col] for row in range(n)]
                        if other_col == current_col:
                            return False
            
            return True

        # Backtracking function to fill the board
        def backtrack(i, j):
            # If reached end of board, solution is found
            if i == n:
                return True
            
            # Determine next cell to fill
            next_i = i + (j + 1) // n
            next_j = (j + 1) % n
            
            # Try placing 0 and 1
            num = random.randint(0, 1)
            board[i][j] = num
            
            # Check all conditions
            if check_streak(i, j, board) and check_count(i, j, board) and check_unique(i, j, board):
                if backtrack(next_i, next_j):
                    return True
            
            # Choose the other way and check
            board[i][j] = 1 - num
            if check_streak(i, j, board) and check_count(i, j, board) and check_unique(i, j, board):
                if backtrack(next_i, next_j):
                    return True
            
            # Undo choice (backtrack)
            board[i][j] = -1
            
            return False

        # Start backtracking from the first cell
        if not backtrack(0, 0):
            raise ValueError("No solution found for the given board size.")
        
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

        # Draw new game buttons for 6x6, 8x8, 10x10, 14x14, 20x20; SOLVE DFS, SOLVE HEURISTIC, COMPARE
        # Define button properties
        button_width = 200
        button_height = BUTTON_HEIGHT
        button_margin = 10
        button_x = (SCREEN_WIDTH - (button_width * 5 + button_margin * 4)) // 2
        button_y = self.board_y_offset + self.board_height + 20

        # Define button labels and actions
        self.buttons = [
            ("6x6", 6),
            ("8x8", 8),
            ("10x10", 10),
            ("14x14", 14),
            ("20x20", 20),
            ("SOLVE DFS", "solve_dfs"),
            ("SOLVE HEU", "solve_heuristic"),
            ("STEP DFS", "step_dfs"),
            ("STEP HEU", "step_heuristic"),
            ("COMPARE", "compare")
        ]

        # Draw the first line of buttons (6x6, 8x8, 10x10, 14x14, 20x20)
        for i, (label, action) in enumerate(self.buttons[:5]):
            rect = pygame.Rect(button_x + i * (button_width + button_margin), button_y, button_width, button_height)
            pygame.draw.rect(self.screen, BUTTON_COLOR, rect)
            pygame.draw.rect(self.screen, BUTTON_COLOR, rect, 2)

            font = pygame.font.Font(None, 36)
            text = font.render(label, True, BUTTON_TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

            # Store button rect and action for event handling
            setattr(self, f"button_{label}", (rect, action))

        # Draw the second line of buttons (SOLVE DFS, SOLVE HEU, STEP DFS, STEP HEU, COMPARE)
        for i, (label, action) in enumerate(self.buttons[5:]):
            rect = pygame.Rect(button_x + i * (button_width + button_margin), button_y + button_height + button_margin, button_width, button_height)
            pygame.draw.rect(self.screen, BUTTON_COLOR, rect)
            pygame.draw.rect(self.screen, BUTTON_COLOR, rect, 2)

            font = pygame.font.Font(None, 36)
            text = font.render(label, True, BUTTON_TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

            # Store button rect and action for event handling
            setattr(self, f"button_{label}", (rect, action))
            
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle the event based on the event type."""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in [1, 3]:  # Left or right mouse button
                self.handle_click(event.pos, event.button)

    def handle_button_click(self, pos: tuple[int]) -> bool:
        """Handle the button click event."""
        for label, action in self.buttons:
            rect, action = getattr(self, f"button_{label}")
            if rect.collidepoint(pos):
                if action in ["solve_dfs", "solve_heuristic", "compare", "step_dfs", "step_heuristic"]:
                    if action == "solve_dfs":
                        print("Solving using dfs...")
                        if self.solve_binairo(trace = True, measure = True, mode = "dfs"):
                            print("Solution found")
                            print("Current board state:")
                            for r in self.temp_board:
                                print(r)
                            print(f"Time used: {self.end_time - self.start_time}")
                            print(f"Current memory usage: {self.current / 10**6} MB")
                            print(f"Peak memory usage: {self.peak / 10**6} MB")
                            self.update_board_sprite(self.temp_board)
                            self.draw_board()
                            self.update_display()
                        else:
                            print("No solution")
                        return True
                    if action == "solve_heuristic":
                        print("Solving using heuristic...")
                        if self.solve_binairo(trace = True, measure = True, mode = "heuristic"):
                            print("Solution found")
                            print("Current board state:")
                            for r in self.temp_board:
                                print(r)
                            print(f"Time used: {self.end_time - self.start_time}")
                            print(f"Current memory usage: {self.current / 10**6} MB")
                            print(f"Peak memory usage: {self.peak / 10**6} MB")
                            self.update_board_sprite(self.temp_board)
                            self.draw_board()
                            self.update_display()
                        else:
                            print("No solution")    
                        return True
                    if action == "step_dfs":
                        print("Solving step by step using dfs...")
                        if self.solve_binairo_step_by_step(t = 100, mode = "dfs"):
                            print("Solution found")
                            print("Current board state:")
                            for r in self.temp_board:
                                print(r)
                            self.update_board_sprite(self.temp_board)
                            self.draw_board()
                            self.update_display()
                        else:
                            print("No solution") 
                        return True
                    if action == "step_heuristic":
                        print("Solving step by step using heuristic...")
                        if self.solve_binairo_step_by_step(t = 100, mode = "heuristic"):
                            print("Solution found")
                            print("Current board state:")
                            for r in self.temp_board:
                                print(r)
                            self.update_board_sprite(self.temp_board)
                            self.draw_board()
                            self.update_display()
                        else:
                            print("No solution") 
                        return True
                    if action == "compare":
                        print("Compare solver...")
                        dfs_time, heu_time = -1, -1
                        print("Solving using dfs...")
                        if self.solve_binairo(trace = True, measure = True, mode = "dfs"):
                            print("Solution found")
                            currentDFS, peakDFS = self.current, self.peak
                            dfs_time = self.end_time - self.start_time
                        else:
                            print("No solution")
                        print("Solving using heuristic...")
                        if self.solve_binairo(trace = True, measure = True, mode = "heuristic"):
                            print("Solution found")
                            currentHeu, peakHeu = self.current, self.peak
                            heu_time = self.end_time - self.start_time
                        else:
                            print("No solution")
                        if dfs_time != -1 and heu_time != -1:
                            print("-------------------DFS-------------------")
                            print(f"DFS runtime: {dfs_time}")
                            print(f"Memory usage: {currentDFS / 10**6} MB")
                            print(f"Peak memory usage: {peakDFS / 10**6} MB")
                            print("----------------Heuristic----------------")
                            print(f"Heuristic runtime: {heu_time}")
                            print(f"Memory usage: {currentHeu / 10**6} MB")
                            print(f"Peak memory usage: {peakHeu / 10**6} MB")
                    return True
                else:
                    self.board_size = action
                    self.board = self.generate_binairo_board(self.board_size)
                    self.remove_cells(self.board_size * self.board_size * 3 // 4 + 1)
                    self.draw_board()
                    self.circle_board = []
                    self.all_sprites = pygame.sprite.Group()
                    for i in range(self.board_size):
                        temp = []
                        for j in range(self.board_size):
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
                    for row in self.board:
                        print(row)
                    return True

    # Update the handle_click method to include button click handling
    def handle_click(self, pos: tuple[int], button: int) -> None:
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
                    self.circle_board[grid_y][grid_x].set_color(BOARD_COLOR)
                    self.board[grid_y][grid_x] = None
                else:
                    self.circle_board[grid_y][grid_x].set_color(WHITE)
                    self.board[grid_y][grid_x] = 1
            elif button == 3:  # Right click
                if self.circle_board[grid_y][grid_x].color == BLACK:
                    self.circle_board[grid_y][grid_x].set_color(BOARD_COLOR)
                    self.board[grid_y][grid_x] = None
                else:
                    self.circle_board[grid_y][grid_x].set_color(BLACK)
                    self.board[grid_y][grid_x] = 0
            return

        # Handle click on button
        if not self.handle_button_click(pos):
            self.update_board_sprite(self.board)
            self.draw_board()
            self.update_display()

    def validate(self) -> bool:
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
            if None in self.board[i]:
                return True
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
        self.all_sprites.draw(self.screen)

    # Update sprite board according to self.board
    def update_board_sprite(self, board: list[list[int]]) -> None: 
        for i in range(self.board_size):
            for j in range(self.board_size):
                circle = self.circle_board[i][j]
                if circle.canUpdate == False:
                    continue
                if board[i][j] == 1:
                    circle.set_color(WHITE)
                elif board[i][j] == 0:
                    circle.set_color(BLACK)
                else:
                    circle.set_color(BOARD_COLOR)

    def is_valid_move(self, board: list[list[int]], row: int, col: int) -> bool:
        
        # Check row streaks
        for i in range(max(0, col-2), min(self.board_size-3, col)+1):
            if board[row][i] == board[row][i+1] == board[row][i+2] != None:
                return False

        # Check column streaks
        for i in range(max(0, row-2), min(self.board_size-3, row)+1):
            if board[i][col] == board[i+1][col] == board[i+2][col] != None:
                return False
            
        # Check if the row is fully populated before validating
        if None not in board[row]:
            if sum(board[row]) != self.board_size // 2:
                return False
            for otherRow in range(self.board_size):
                if otherRow != row and board[otherRow] == board[row]:
                    return False
        
        # Check if the column is fully populated before validating
        col_values = [board[r][col] for r in range(self.board_size)]
        if None not in col_values:
            if sum(col_values) != self.board_size // 2:
                return False
            for otherCol in range(self.board_size):
                if otherCol != col and [board[r][otherCol] for r in range(self.board_size)] == col_values:
                    return False

        # If all checks passed, return True
        return True

    def solve_binairo(self, trace : bool = False, measure : bool = False, mode : str = "heuristic") -> bool:  
        def dfs(row, col):
            if row == self.board_size:  # If we've reached past the last row, solution found
                if measure:
                    self.current, self.peak = tracemalloc.get_traced_memory()
                    self.end_time = time.time()
                return True
            
            next_row, next_col = (row, col + 1) if col + 1 < self.board_size else (row + 1, 0)
            
            if self.temp_board[row][col] != None:  # Skip pre-filled cells
                return dfs(next_row, next_col)
            
            for num in [0, 1]:
                if trace:
                    print(f"Trying {num} at ({row}, {col})")
                self.temp_board[row][col] = num
                if self.is_valid_move(self.temp_board, row, col) and dfs(next_row, next_col):
                    return True
                self.temp_board[row][col] = None  # Undo move if it didn't lead to a solution
            
            return False
    
        # Helper function to count occurrences of 0s and 1s in a row or column
        def count_occurrences(line):
            return line.count(0), line.count(1)
        
        # Logical move application
        def apply_logical_moves():
            progress = True
            while progress:
                progress = False
                for row in range(self.board_size):
                    for col in range(self.board_size):
                        if self.temp_board[row][col] is None:
                            # Check neighbors to apply logical rules
                            neighbors = []
                            if col > 1:
                                neighbors.append(self.temp_board[row][col-2:col+1])
                            if col > 0 and col < self.board_size - 1:
                                neighbors.append(self.temp_board[row][col-1:col+2])
                            if col < self.board_size - 2:
                                neighbors.append(self.temp_board[row][col:col+3])
                            if row > 1:
                                neighbors.append([self.temp_board[r][col] for r in range(row-2, row+1)])
                            if row > 0 and row < self.board_size - 1:
                                neighbors.append([self.temp_board[r][col] for r in range(row-1, row+2)])
                            if row < self.board_size - 2:
                                neighbors.append([self.temp_board[r][col] for r in range(row, row+3)])
                            
                            for group in neighbors:
                                if group.count(0) == 2:
                                    self.temp_board[row][col] = 1
                                    if trace:
                                        print(f"Filling 1 at ({row}, {col})")
                                    progress = True
                                elif group.count(1) == 2:
                                    if trace:
                                        print(f"Filling 0 at ({row}, {col})")
                                    self.temp_board[row][col] = 0
                                    progress = True
                            
                            # Check row and column balance
                            row_zeros, row_ones = count_occurrences(self.temp_board[row])
                            col_values = [self.temp_board[r][col] for r in range(self.board_size)]
                            col_zeros, col_ones = count_occurrences(col_values)
                            
                            if row_zeros == self.board_size // 2:
                                for c in range(self.board_size):
                                    if self.temp_board[row][c] is None:
                                        if trace:
                                            print(f"Filling 1 at ({row}, {c})")
                                        self.temp_board[row][c] = 1
                                        progress = True

                            if row_ones == self.board_size // 2:
                                for c in range(self.board_size):
                                    if self.temp_board[row][c] is None:
                                        if trace:
                                            print(f"Filling 0 at ({row}, {c})")
                                        self.temp_board[row][c] = 0
                                        progress = True

                            if col_zeros == self.board_size // 2:
                                for r in range(self.board_size):
                                    if self.temp_board[r][col] is None:
                                        if trace:
                                            print(f"Filling 1 at ({r}, {col})")
                                        self.temp_board[r][col] = 1
                                        progress = True

                            if col_ones == self.board_size // 2:
                                for r in range(self.board_size):
                                    if self.temp_board[r][col] is None:
                                        if trace:
                                            print(f"Filling 0 at ({r}, {col})")
                                        self.temp_board[r][col] = 0
                                        progress = True

        # Heuristic DFS with prioritized cells
        def heuristic_dfs():
            temp_board = self.temp_board
            # Apply logical moves before DFS
            apply_logical_moves()
            
            # Find  empty cell
            move = None
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.temp_board[row][col] == None:
                        move = [row, col]
                        break
                if move is not None:
                    break  
            
            # If no empty cells, solution found
            if move is None:
                self.current, self.peak = tracemalloc.get_traced_memory()
                self.end_time = time.time()
                return True
            
            row, col = move
            for num in [0, 1]:
                if trace:
                    print(f"Trying {num} at ({row}, {col})")
                self.temp_board[row][col] = num
                if self.is_valid_move(self.temp_board, row, col) and heuristic_dfs() and self.validate():
                    return True
                self.temp_board[row][col] = None  # Undo move
            
            self.temp_board = temp_board
            return False
        
        # Copy the board to avoid modifying the original board
        self.temp_board = [row[:] for row in self.board]
        if measure:
            self.start_time = time.time()
            tracemalloc.start()
        if mode == "dfs":
            return dfs(0, 0)
        else:    
            return heuristic_dfs()

    def solve_binairo_step_by_step(self, t: int = 500, mode: str = "heuristic") -> bool:
        def dfs(row, col) -> bool:
            if row == self.board_size:
                return True
            
            next_row, next_col = (row, col + 1) if col + 1 < self.board_size else (row + 1, 0)
            
            if self.temp_board[row][col] is not None:
                return dfs(next_row, next_col)
            
            for num in [0, 1]:
                print(f"Trying {num} at ({row}, {col})")
                self.temp_board[row][col] = num
                if self.is_valid_move(self.temp_board, row, col):
                    self.update_board_sprite(self.temp_board)
                    self.update_display()
                    pygame.display.flip()
                    time.sleep(t / 1000.0)
                    if dfs(next_row, next_col):
                        return True
                self.temp_board[row][col] = None
            
            return False

        def heuristic_dfs() -> bool:
            def count_occurrences(line):
                return line.count(0), line.count(1)

            def apply_logical_moves():
                progress = True
                while progress:
                    self.update_board_sprite(self.temp_board)
                    self.update_display()
                    pygame.display.flip()
                    time.sleep(t / 1000.0)
                    progress = False
                    for row in range(self.board_size):
                        for col in range(self.board_size):
                            if self.temp_board[row][col] is None:
                                # Check neighbors to apply logical rules
                                neighbors = []
                                if col > 1:
                                    neighbors.append(self.temp_board[row][col-2:col+1])
                                if col > 0 and col < self.board_size - 1:
                                    neighbors.append(self.temp_board[row][col-1:col+2])
                                if col < self.board_size - 2:
                                    neighbors.append(self.temp_board[row][col:col+3])
                                if row > 1:
                                    neighbors.append([self.temp_board[r][col] for r in range(row-2, row+1)])
                                if row > 0 and row < self.board_size - 1:
                                    neighbors.append([self.temp_board[r][col] for r in range(row-1, row+2)])
                                if row < self.board_size - 2:
                                    neighbors.append([self.temp_board[r][col] for r in range(row, row+3)])
                                
                                for group in neighbors:
                                    if group.count(0) == 2:
                                        self.temp_board[row][col] = 1
                                        print(f"Filling 1 at ({row}, {col})")
                                        progress = True
                                    elif group.count(1) == 2:
                                        print(f"Filling 0 at ({row}, {col})")
                                        self.temp_board[row][col] = 0
                                        progress = True
                                
                                # Check row and column balance
                                row_zeros, row_ones = count_occurrences(self.temp_board[row])
                                col_values = [self.temp_board[r][col] for r in range(self.board_size)]
                                col_zeros, col_ones = count_occurrences(col_values)
                                
                                if row_zeros == self.board_size // 2:
                                    for c in range(self.board_size):
                                        if self.temp_board[row][c] is None:
                                            print(f"Filling 1 at ({row}, {c})")
                                            self.temp_board[row][c] = 1
                                            progress = True

                                if row_ones == self.board_size // 2:
                                    for c in range(self.board_size):
                                        if self.temp_board[row][c] is None:
                                            print(f"Filling 0 at ({row}, {c})")
                                            self.temp_board[row][c] = 0
                                            progress = True

                                if col_zeros == self.board_size // 2:
                                    for r in range(self.board_size):
                                        if self.temp_board[r][col] is None:
                                            print(f"Filling 1 at ({r}, {col})")
                                            self.temp_board[r][col] = 1
                                            progress = True

                                if col_ones == self.board_size // 2:
                                    for r in range(self.board_size):
                                        if self.temp_board[r][col] is None:
                                            print(f"Filling 0 at ({r}, {col})")
                                            self.temp_board[r][col] = 0
                                            progress = True

            temp_board = self.temp_board

            apply_logical_moves()
            
            move = None
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.temp_board[row][col] == None:
                        move = [row, col]
                        break
                if move is not None:
                    break
            
            if move is None:
                return True
            
            row, col = move
            for num in [0, 1]:
                print(f"Trying {num} at ({row}, {col})")
                self.update_board_sprite(self.temp_board)
                self.update_display()
                pygame.display.flip()
                time.sleep(t / 1000.0)
                self.temp_board[row][col] = num
                if self.is_valid_move(self.temp_board, row, col) and heuristic_dfs() and self.validate():
                    return True
                self.temp_board[row][col] = None
            
            self.temp_board = temp_board
            return False

        self.temp_board = [row[:] for row in self.board]
        if mode == "dfs":
            return dfs(0, 0)
        else:
            return heuristic_dfs()

    def remove_cells(self, n: int) -> None:
        """Remove n cells from the board."""
        removed = 0
        attempts = 0
        max_attempts = n * 10  # To prevent infinite loops
        
        while removed < n and attempts < max_attempts:
            row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            if self.board[row][col] is not None:  # Check if the cell is not already empty
                original_value = self.board[row][col]
                self.board[row][col] = None  
                
                # Check if the board is still valid and uniquely solvable
                if self.is_valid_move(self.board, row, col) and self.solve_binairo():
                    removed += 1
                else:
                    # If invalid or no solution, restore the original value
                    self.board[row][col] = original_value
            
            attempts += 1
        
        if attempts >= max_attempts:
            print(f"Warning: Maximum attempts reached. Only {removed} cells were removed.")

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