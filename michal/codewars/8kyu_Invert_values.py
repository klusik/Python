# Given a set of numbers, return the additive inverse of each.
# Each positive becomes negatives, and the negatives become positives.

def invert(lst):
    inv = []
    for i in lst:
        if i >= 0:
            inv.append(-i)

        else:
            inv.append(abs(i))
    return inv


print(invert([1, 2, -3, 4, 5]))
