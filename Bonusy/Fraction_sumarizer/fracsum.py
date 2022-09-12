"""
    Sum the fraction.

    Input the fraction in form like:
        '1/2 + 2/3 + 1/7'

    Output will be the fraction in form X/Y
"""

# IMPORTS #

# RUNTIME #
if __name__ == "__main__":

    # Input the fraction from keyboard
    fraction_string = str(input("Enter the fraction sum: "))

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



    print(f"{fraction_string} = ({(nominator)}) / {common_denominator} = {eval(nominator)} / {common_denominator}")

