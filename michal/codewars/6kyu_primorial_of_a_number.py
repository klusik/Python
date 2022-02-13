# INSTRUCTIONS:
# Definition (Primorial Of a Number) Is similar to factorial of a number, In primorial, not all the
# natural numbers get multiplied, only prime numbers are multiplied to calculate the primorial of a number. It's
# denoted with P#.
#
# Task
# Given a number N , calculate its primorial. !alt !alt
#
# Notes
# Only positive numbers will be passed (N > 0) .
# Input >> Output Examples:
# 1- numPrimorial (3) ==> return (30)
# Explanation:
# Since the passed number is (3) ,Then the primorial should obtained by multiplying 2 * 3 * 5 = 30 .
#
# Mathematically written as , P3# = 30 .
# 2- numPrimorial (5) ==> return (2310)
# Explanation:
# Since the passed number is (5) ,Then the primorial should obtained by multiplying 2 * 3 * 5 * 7 * 11 = 2310 .
#
# Mathematically written as , P5# = 2310 .
# 3- numPrimorial (6) ==> return (30030)
# Explanation:
# Since the passed number is (6) ,Then the primorial should obtained by multiplying 2 * 3 * 5 * 7 * 11 * 13 = 30030 .
#
# Mathematically written as , P6# = 30030 .


# from instructions it is not 100% clear, but task is to count factorinal of n prime numbers
# this means that amount of numbers is unknown

def num_primorial(n):
    # your code here

    # cycle generating prime numbers
    lstOfPrimeNumber = []
    while len(lstOfPrimeNumber) < n:
        for i in range(n+1):
            if i % 2 <= 1:
                lstOfPrimeNumber.append(i)
                print('seznam prvocisel', lstOfPrimeNumber)
    lstOfPrimeNumber.remove(0)
    print('seznam prvocisel', lstOfPrimeNumber)
    # cycle multiplying prime numbers
    result = 0
    for x in lstOfPrimeNumber:
        result = result * x
        print('vysledek', result)

    return result

num_primorial(3)
