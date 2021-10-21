# this is learning program for sort algorithms
# sor the list in ascending order

# unsorted list
to_sort = [2, 5, 7, 6, 8, 3, 0, 4, 9, 1, 3, 1]

# bubble sort
# cycle until sorted


def bubble():

    while True:
        swap = 0
        for i in range(0, len(to_sort)-1):
            andere = i + 1
            if to_sort[i] > to_sort[andere]:
                # make swap
                buffer = to_sort[i]

                to_sort[i] = to_sort[andere]
                to_sort[andere] = buffer

                swap = swap+1

        if swap == 0:
            break
    print(to_sort)

se