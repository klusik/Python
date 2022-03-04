'''
Pomocí dvou cyklů for a parametru end pro print napiš program, který vypíše následující tvar:

X X X X X
X X X X X
X X X X X
X X X X X
X X X X X
'''

# outer cycle - column
for column in range(5):
    print(end="\n")
    # inner cycle - row
    for line in range(5):
        print('X', end=' ')