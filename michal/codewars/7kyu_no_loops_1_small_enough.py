#* No Loops Allowed *
# You will be given an array (a) and a limit value (limit). You must check that all values in the array are below
# or equal to the limit value. If they are, return true. Else, return false.
# You can assume all values in the array are numbers.
# Do not use loops. Do not modify input array.

def small_enough(a, limit):
    # your code here
    if max(a) <= limit:
        return True
    else:
        return False


print(small_enough([1, 2, 3, 4, 5], 5))
