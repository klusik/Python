"""
7 kyu
Descending Order
Your task is to make a function that can take any non-negative integer
as an argument and return it with its digits in descending order.

Essentially, rearrange the digits to create the highest possible number.
"""

def make_the_biggest_number_in_the_universe(number):
    str_number = str(number)

    list_biggest = []

    for character in str_number:
        list_biggest.append(character)

    list_biggest.sort(reverse=True)

    return int("".join(list_biggest))

if __name__ == "__main__":
    try:
        number = int(input("Enter the number: "))

        if number < 0:
            number = -number

    except ValueError:
        print("No way")

    print(make_the_biggest_number_in_the_universe(number))