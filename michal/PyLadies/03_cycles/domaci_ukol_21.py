'''
Vyber si jeden z předchozích úkolů a uprav jej tak, aby počet řádků a sloupců mohl zadat uživatel.
'''
lines = int(input('Enter number of lines: '))
columns = int(input('Enter number of columns: '))

# outer cycle - column
for line in range(lines):
    print(end="\n")
    # inner cycle - row
    for column in range(columns):
        print('X', end=' ')