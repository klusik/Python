# In order to prove it's success and gain funding, the wilderness zoo needs to prove to environmentalists that it has
# x number of mating pairs of bears.
#
# You must check within string (s) to find all of the mating pairs, and return a string containing only them.
# Line them up for inspection.
#
# Rules:
# Bears are either 'B' (male) or '8' (female),
# Bears must be together in male/female pairs 'B8' or '8B',
# Mating pairs must involve two distinct bears each ('B8B' may look fun, but does not count as two pairs).
#
# Return an array containing a string of only the mating pairs available. e.g:
# 'EvHB8KN8ik8BiyxfeyKBmiCMj' ---> 'B88B' (empty string if there are no pairs)
# and true if the number is more than or equal to x,
# false if not:
# (6, 'EvHB8KN8ik8BiyxfeyKBmiCMj') ---> ['B88B', false];
# x will always be a positive integer, and s will never be empty

def bears(x,s):
    # your code here
    slicedList = []
    maleFemale = 'B8'
    femaleMale = '8B'
    listOfPairs = []
    index = 0
    for i in s:

        # slice string s
        string = s[index:index + 2]
        # add it to list
        slicedList.append(string)
        index = index + 1

    lstIndex = 0
    # loop through strings in 'sliced list'
    for i in slicedList:
        # if i value in 'sliced list' equals to maleFemale string
        if i == maleFemale:
            # add the i value to 'list of pairs'
            listOfPairs.append(i)
            # delete found pair from 'sliced list'
            slicedList.pop(lstIndex)

        # if i value in 'sliced list' equals to femaleMale string
        if i == femaleMale:
            # add i to list of pairs
            listOfPairs.append(i)
            # delete found pair from 'sliced list'
            slicedList.pop(lstIndex)
        lstIndex = lstIndex + 1



    numberOfPairs = len(listOfPairs)

    truefalse = 0
    if numberOfPairs >= int(x):
        truefalse = True
    else:
        truefalse = False

    # convert 'list of pairs' to string
    outputString = ''.join(listOfPairs)

    # prepare correct output format
    solution = [outputString, truefalse]
    return(solution)

bears('0', 'j8BmB88B88gkBBlf8hg8888lbe88')