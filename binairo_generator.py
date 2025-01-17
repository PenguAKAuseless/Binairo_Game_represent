import random

def generate_binairo_board(n: int) -> list[list[int]]:
    # Binairo board size must be an even number
    if n % 2 != 0:
        raise ValueError("n must be an even number.")

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
