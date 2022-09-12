"""
    Sum the fraction.

    Input the fraction in form like:
        '1/2 + 2/3 + 1/7'

    Output will be the fraction in form X/Y
"""

# IMPORTS #
import sympy

# RUNTIME #
if __name__ == "__main__":

    # Input the range
    prime_max_input = int(input("Please enter the maximum prime: "))

    prime_list = sympy.primerange(2, prime_max_input)

    # Input the fraction from keyboard
    # fraction_string = str(input("Enter the fraction sum: "))

    # Generating fraction_string
    fraction_string = str()
    for prime_index, prime in enumerate(prime_list):
        if prime_index > 0:
            fraction_string += ' + '
        fraction_string += f"1/{prime}"

    # Create parts between plusses
    fraction_parts = fraction_string.split('+')

    for fraction_part in fraction_parts:
        print(f"Part {fraction_part.strip()} found.")

    # Find common denominator
    common_denominator = 1
    for frac_part in fraction_parts:
        common_denominator *= int(frac_part.strip().split('/')[-1]) # Last one

    print(f"Common denominator: {common_denominator}")

    # Find nominator
    nominator = str()
    for frac_index, frac_part in enumerate(fraction_parts):
        frac_nominator = int(frac_part.strip().split('/')[0]) # First one
        frac_denominator = int(frac_part.strip().split('/')[-1]) # Last one

        if frac_index > 0:
            nominator += " + "

        nominator += str(int(common_denominator / frac_denominator * frac_nominator))



    print(f"{fraction_string} =\n= ({(nominator)}) / {common_denominator} =\n= {eval(nominator)} / {common_denominator}")

