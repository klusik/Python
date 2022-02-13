s = ("ahoj hello world hello")
w = ('hello')
counter = 0

# to keep previous value of string 's', further we work only with string 'sx'
sx = s

# infinite cycle to search through string line 'sx'
while True:
    # index find position of first character of 'w' (searched word) in string 's'
    index = sx.find(w)

    # index cycles through 'sx' and if 'w' is not present it returns -1. If -1 is returned while cycle ends here
    if index == -1:
        break

    # if condition is not met the count value raises by 1 to represent found word
    counter += 1

    # here string sx is shortened. everything from index (first letter of 'w') + count of letters of 'w' is cut off
    # making sx shorthened new sx
    sx = sx[index + len(w):]

print(s)

print(index)
if index > 0:
    print(counter)
new = s.lstrip(5)
print(new)
# vyhledat index
# zkratit radku na index + delka hledaneho slova
