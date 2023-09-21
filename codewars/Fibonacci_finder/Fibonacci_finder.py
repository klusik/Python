"""
    Codewars: https://www.codewars.com/kata/5541f58a944b85ce6d00006a/train/python
"""

import functools
import sys


@functools.lru_cache(maxsize=None)
def fibonacci(number):
    if number <= 1:
        return number
    else:
        return fibonacci(number - 2) + fibonacci(number - 1)


def productFib(number: int):
    print(number)
    if (number == 0):
        return [0, 1, True]
    elif number == 1:
        return [1, 1, True]
    elif number == 2:
        return [1, 2, True]
    elif number == 3:
        return [2, 3, False]

    for test_num in range(number):
        fib_1 = fibonacci(test_num)
        fib_2 = fibonacci(test_num + 1)
        if (fib_1 * fib_2) == number:
            return [fib_1, fib_2, True]

        if (fib_1 * fib_2) > number:
            return [fib_1, fib_2, False]


def main():
    print(sys.getrecursionlimit())
    print(productFib(714))


if __name__ == "__main__":
    main()
