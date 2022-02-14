# In this kata, you will do addition and subtraction on a given string. The return value must be also a string.
# Note: the input will not be empty.
# Examples
# "1plus2plus3plus4"  --> "10"
# "1plus2plus3minus4" -->  "2"

import re

def calculate(numbersAndOperators):
    # your code here
    # idea is to convert given string to list of elements (numbers and operators) in order
    # then take first number, operator and second number
    # after previous operation update list, first three items will be replaced by operation result
    # iterate until last two characters remain (operator and number)

    # convert given string into list

    # V3
    print ("V3")
    numbers = []

    # "1plus2minus3minus4plus5minus5" -> ["1", "2minus3minus4", "5minus6"]
    for minusGroup in numbersAndOperators.split("plus"):
        # "2minus3minus4" -> ["2", "3", "4"]
        splitMinuses = minusGroup.split("minus")

        # "2"
        plus = splitMinuses[0]
        # ["3", "4"]
        minuses = splitMinuses[1:]

        # +2
        numbers.append(int(plus))
        # -3, -4
        numbers.extend(-int(minus) for minus in minuses)


    print (numbers)

    sumaSumarum =  sum(numbers)

    print (sumaSumarum)


    # V2
    print ("V2")
    numbers = []

    operatorRegexp = re.compile("^(plus|minus)(.*)")
    numberRegexp = re.compile("^(\d+)(.*)")

    sign = +1

    while True:

        # try to match a number in the beginning e.g. "1234"
        numberMatch = numberRegexp.match(numbersAndOperators)

        assert (numberMatch)

        numbers.append(sign * int(numberMatch.group(1)))

        numbersAndOperators = numberMatch.group(2)

        if (not numbersAndOperators):
            break

        # try to match the operator in the beginning e.g. "plus"
        operatorMatch = operatorRegexp.match(numbersAndOperators)

        assert (operatorMatch)

        operator = operatorMatch.group(1)

        if (operator == "plus"):
            sign = +1
        else:
            sign = -1

        numbersAndOperators = operatorMatch.group(2)

    print (numbers)

    sumaSumarum =  sum(numbers)

    print (sumaSumarum)


    # V1
    print ("V1")

    currentNumber = 0
    sign = +1
    expectedOperatorChars = ''

    lst = []
    numbers = []
    operators = []


    for znak in numbersAndOperators:
        # if znak == 1:
        #     lst.append(znak)
        #     numbers.append(znak)

        if (expectedOperatorChars):
            assert (znak == expectedOperatorChars[0])
            expectedOperatorChars = expectedOperatorChars[1:]

        elif (znak in '0123456789'):
            currentNumber = (10 * currentNumber) + (sign * int(znak))

        elif znak == 'p':
            expectedOperatorChars = 'lus'
            numbers.append(currentNumber)
            sign = +1
            currentNumber = 0

        elif znak == 'm':
            expectedOperatorChars = 'inus'
            numbers.append(currentNumber)
            sign = -1
            currentNumber = 0

        else:
            assert (False), znak

    if (currentNumber):
        numbers.append(currentNumber)

    print (numbers)

    sumaSumarum =  sum(numbers)

    print (sumaSumarum)

    return str(sumaSumarum)

    print('vstup: ', numbersAndOperators)
    print('list vytvoreny ze vstupu: ', lst)

    # calculation
    print(len(numbers))

    # while len(numbers) > 0:
    for i in operators:
        if i == '+':
            soucet = numbers[0] + numbers[1]
            print('soucet: ', soucet)
            numbers = numbers[2:]
            print('numbers pred pridanim souctu: ', numbers)
            numbers.insert(0, soucet)
            print('numbers po pridani souctu na prvni misto: ', numbers)

        if i == '-':
            rozdil = numbers[0] - numbers[2]
            print('rozdil: ', rozdil)
            numbers = numbers[2:]
            print('numbers pred vlozenim souctu: ')
            numbers.insert(0, rozdil)
            print('numbers po vlozeni souctu na prvni misto: ', numbers)

    print('cisla: ', numbers)
    print('operatory: ', operators)

    return


calculate('10000plus2minus1881plus134minus1')
