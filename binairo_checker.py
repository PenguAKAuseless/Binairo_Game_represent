def validate(n, board):
    # Check consecutive streaks of 1s or 0s
    for i in range(n - 2):
        for j in range(n - 2):
            if board[i][j] == board[i + 1][j] and board[i + 1][j] == board[i + 2][j]:
                return False
            if board[i][j] == board[i][j + 1] and board[i][j + 1] == board[i][j + 2]:
                return False
    
    # Check row and col validity
    row_set = set()
    col_set = set()
    for i in range(n):
            if sum(board[i]) != n // 2:
                return False
            row_num = int(''.join(map(str, board[i])), 2)
            if row_num in row_set:
                print(row_num)
                return False
            else:
                row_set.add(row_num)

    for j in range(n):
            if sum(board[row][j] for row in range(n)) != n // 2:
                return False
            col_num = int(''.join(map(str, [board[row][j] for row in range(n)])), 2)
            if col_num in col_set:
                print("Col ", i)
                return False
            else:
                col_set.add(col_num)
    
    return True
