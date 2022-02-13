# Create a function named divisors/Divisors that takes an integer n > 1 and returns an array with all of the integer's
# divisors(except for 1 and the number itself), from smallest to largest. https://www.youtube.com/watch?v=2TN0bUw7u7Y
# If the number is prime return the string '(integer) is prime'

# chteji vypsat vsechny delitele daneho cisla, ktere nemaji zbytek
# prvocisla chteji oznacit textem

def divisors(integer):
    # check, ze zadane cislo je cele cislo
    integer = int(integer)

    # promenna, ktera bude obsahovat vsechny spolecne delitele
    divs = []
