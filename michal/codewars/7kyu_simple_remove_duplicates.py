# In this Kata, you will remove the left-most duplicates from a list of integers and return the result.
#
# # Remove the 3's at indices 0 and 3
# # followed by removing a 4 at index 1
# solve([3, 4, 4, 3, 6, 3]) # => [4, 6, 3]

def solve(arr):
    to_delete_indeces = []
    for i in range(0, len(arr)):
        if arr[i] in arr[i+1:]:
            to_delete_indeces.append(i)
    print(to_delete_indeces)

    offset = 0
    for index in to_delete_indeces:
        del arr[index-offset]
        offset += 1
    print(arr)

    return arr



solve([3, 4, 4, 3, 6, 3])
