'''
Pomocí dvou cyklů for a příkazu if napiš program, který z jednotlivých 'X' a mezer vypíše:

X X X X X X
X         X
X         X
X         X
X         X
X X X X X X
'''

# outer cycle - line
for line in range(6):
    print(end="\n")
    # inner cycle - column
    for column in range(6):
        # first and last line prints X
        if line == 0 or line == 5:
            print('X', end = ' ')
        else:
            # remaining lines prints X    X    
            if column == 0 or column == 5:
                print('X', end = ' ')
            else:
                print(' ', end = ' ')