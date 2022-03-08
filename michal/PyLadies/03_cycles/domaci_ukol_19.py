'''
Pomocí dvou cyklů for a parametru end pro print napiš program, který vypíše „tabulku“ s násobilkou.

0 0 0 0 0
0 1 2 3 4
0 2 4 6 8
0 3 6 9 12
0 4 8 12 16
'''
# outer cycle - column
for column in range(5):
    print(end="\n")
    # inner cycle - row
    for line in range(5):
        print(line * column, end=' ')