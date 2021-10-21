lListOfElements = [1, 1, 7, -7, -4, 1]


def swap(iIndex1, iIndex2):
    """
    swap function help:
    function takes two input parameters and switches it's values
    function returns two files

    index1 = first input parameter
    index2 = second input parameter
    """

    iSkladka = iIndex1
    iIndex1 = iIndex2
    iIndex2 = iSkladka

    return iIndex1, iIndex2


def smallest(lVstupniList, iIndex):
    """
    smallest function help:
    function takes two input parameters, a list and a index
    function finds smallest value in the given list limited by given index
    function returns index of the smallest item in the reshaped list
    """

# kurva, neslicuje to, opravit
    # slice the given list
    lReshaped_list = lVstupniList[iIndex:]

    iNejmensi_value = lReshaped_list[0]
    iNejmensi_index = 0
    # cycle through elements of given list
    for i in lReshaped_list:

        if iNejmensi_value > i:
            iNejmensi_value = i
        iNejmensi_index = iNejmensi_index + 1

    return iIndex


def select_sort(lList_to_be_sorted):
    """
    select sort function help:
    function sorts the given list using select sort algorithm
    input is list of numbers
    return is sorted list of numbers
    """
    # define index pointer
    iPointer = 0
    lSorted_list = []

    # kurva, neupravuje to lSorted_list
    for i in lList_to_be_sorted:

        # find the smallest number in the list
        iSmallestIndex = smallest(lList_to_be_sorted, iPointer)

        if iSmallestIndex != 0:
            lSorted_list = swap(0, iSmallestIndex)

    return lSorted_list

lListListu = [
    [1, 1, 7, -7, -4, 1],
    [-1, 1, -1, 1, -2, 2, 9],
    [3, 1, 4, 1, 5, 9, 2, 5],
]

for i in lListListu:
    print(select_sort(i))