"""
    Numbers that are a power of their sum of digits

    The number 81 has a special property, a certain power of the sum of its digits
    is equal to 81 (nine squared). Eighty one (81), is the first number in having
    this property (not considering numbers of one digit). The next one, is 512.
    Let's see both cases with the details

    8 + 1 = 9 and 9^2 = 81

    512 = 5 + 1 + 2 = 8 and 8^3 = 512

    We need to make a function that receives a number as an argument n
    and returns the n-th term of this sequence of numbers.

    Examples (input --> output)
    1 --> 81

    2 --> 512
    Happy coding!

    CW: https://www.codewars.com/kata/55f4e56315a375c1ed000159/train/python
"""
# IMPORTS #
import math


def sum_of_digits(input_number: int) -> int:
    """ Returns sum of digits """
    return 0 if input_number == 0 else input_number % 10 + sum_of_digits(input_number // 10)


def number_of_digits(input_number: int) -> int:
    """ Returns number of digits """
    return len(str(input_number))


def power_sumDigTerm(input_number: int) -> int:
    """ Function which does what it needs to be done """

    # Output would be placed here
    list_of_cool_numbers: list[int] = []

    # Iterate number
    test_number = 80

    while True:
        """ Do this iteration until the right number count is not found """

        # caching
        sum_od_digits_cache = sum_of_digits(test_number)
        number_of_digits_cache = number_of_digits(test_number)

        for power in range(number_of_digits_cache+1, 1, -1):
            if (sum_od_digits_cache ** power) == test_number:
                list_of_cool_numbers.append(test_number)
                print(list_of_cool_numbers)

        if len(list_of_cool_numbers) >= input_number:
            return list_of_cool_numbers[-1]

        # print(test_number, list_of_cool_numbers)

        test_number += 1



if __name__ == "__main__":
    user_input = int(input("Enter the order number: "))
    print(f"The {user_input}. solution is {power_sumDigTerm(user_input)}.")
