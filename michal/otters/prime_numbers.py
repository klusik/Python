#  purpose of this script is to return all prime numbers until user given number

# imports:
# standard modules
import math
import time
# third party modules

# my modules

def prime_numbers(n):
    ''':return 'True' if 'n' is a prime number. False otherwise'''

    # 1 is not prime number by definition
    if n == 1:
        return False

    # if n is even, it is not prime
    if n == 2:
        return True
    if n > 2 and n % 2 == 0:
        return False

    max_divisor = math.floor(math.sqrt(n))

    for d in range (3, 1 + max_divisor, 2):
        if n % d == 0:
            return False
    return True

t0 = time.time()
for n in range(1,21):
    print(n, prime_numbers(n))
t1 = time.time()
print('time required: ', t1-t0)