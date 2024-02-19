to_checks = [
    (0,1,2),
    (3,4,5),
    (6,7,8),
    (0,3,6),
    (1,4,7),
    (2,5,8),
    (0,4,8),
    (2,4,6),
]
def check_win(grid, player):
    return any(all(grid[i] == player for i in to_check) for to_check in to_checks)
# def check_win(grid, player):
#     for to_check in to_checks:
#         win = True
#         for i in to_check:
#             if grid[i] != player:
#                 win = False
#         if win:
#             return True
#     return False
def check_draw(grid):
    return all(field != " " for field in grid)
def moves(grid, player):
    for i in range(9):
        if grid[i] == " ":
            new_grid = grid[:]
            new_grid[i] = player
            yield new_grid
def print_grid(grid):
    for i in range(3):
        print(grid[3 * i : 3 * i + 3])
    print()

def value(grid, player):
    if check_win(grid, "X"):
        return 1
    if check_win(grid, "O"):
        return -1
    if check_draw(grid):
        return 0
    if player == "X":
        return max(
            value(new_grid, "O")
            for new_grid in moves(grid, player)
        )
    else:
        return min(
            value(new_grid, "X")
            for new_grid in moves(grid, player)
        )

# grid = [" "] * 9
grid = list("   OX    ")
print_grid(grid)
val = value(grid, "X")
print(val)
print()
for new_grid in moves(grid, "X"):
    if value(new_grid, "O") == val:
        print_grid(new_grid)