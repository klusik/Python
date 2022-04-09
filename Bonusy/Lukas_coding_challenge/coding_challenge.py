"""
coding challenge

máš zadané kladné celé n

najdi všechna taková a, b, c, že a+b+c = n (s tím, že např. trojice 1, 3, 8 je jiná než 3, 1, 8)

Udělej to v O(n^2)
"""

# IMPORTS #
import pprint


# RUNTIME #
def find_numbers(input_number):
    """ Find numbers according to the assignment """

    numbers = list()

    for number in range(3, input_number + 1):
        # Find other 2 numbers
        remaining_number = input_number - number
        for number_2 in range(2, remaining_number + 1):
            remaining_number_2 = remaining_number - number_2
            for number_3 in range(1, remaining_number_2 + 1):
                remaining_number_3 = remaining_number_2 - number_3

                if (number + number_2 + number_3) == input_number:
                    numbers.append((number, number_2, number_3))

    return numbers


def main():
    try:
        input_number = int(input("Enter the whole positive number, 3 or higher: "))
        if input_number < 3:
            raise (ValueError)
    except ValueError:
        print("Bad format of number or the value doesn't make sense.")

    found_numbers = find_numbers(input_number)

    print("Numbers found: ")
    pprint.pprint(found_numbers)


if __name__ == "__main__":
    main()
