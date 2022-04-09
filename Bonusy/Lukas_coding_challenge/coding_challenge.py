"""
coding challenge

máš zadané kladné celé n

najdi všechna taková a, b, c, že a+b+c = n (s tím, že např. trojice 1, 3, 8 je jiná než 3, 1, 8)

Udělej to v O(n^2)
"""

# IMPORTS #
import pprint
import time


# RUNTIME #
def find_numbers_o2(input_number):
    """ Same as find_numbers, but hopefully faster :-D """
    numbers = set()

    for number_1 in range(1, input_number+1):
        for number_2 in range(number_1, input_number+1-number_1):
            for number_3 in range(number_2, input_number+1-number_1-number_2):
                if (number_1 + number_2 + number_3) == input_number:
                    # Basic combination
                    numbers.add((number_1, number_2, number_3))
                    # Run permutations (yeah, bruteforce)
                    numbers.add((number_1, number_3, number_2))
                    numbers.add((number_2, number_1, number_3))
                    numbers.add((number_2, number_3, number_1))
                    numbers.add((number_3, number_2, number_1))
                    numbers.add((number_3, number_1, number_2))


    return numbers

def find_numbers(input_number):
    """ Find numbers according to the assignment """
    # O(n^3) solution

    numbers = set()

    for number in range(1, input_number + 1):
        # Find other 2 numbers
        remaining_number = input_number - number
        for number_2 in range(1, remaining_number + 1):
            remaining_number_2 = remaining_number - number_2
            for number_3 in range(1, remaining_number_2 + 1):
                remaining_number_3 = remaining_number_2 - number_3

                if (number + number_2 + number_3) == input_number:
                    numbers.add((number, number_2, number_3))

    return numbers


def main():
    try:
        input_number = int(input("Enter the whole positive number, 3 or higher: "))
        if input_number < 3:
            raise (ValueError)
    except ValueError:
        print("Bad format of number or the value doesn't make sense.")

    initial_time = time.time()
    # found_numbers = find_numbers(input_number)
    final_time = time.time()

    print("Numbers found (1st method): ")
    # pprint.pprint(found_numbers)
    print(f"It ran for {final_time - initial_time} s.")

    initial_time = time.time()
    found_numbers = find_numbers_o2(input_number)
    final_time = time.time()

    print("Numbers found (2nd method): ")
    # pprint.pprint(found_numbers)
    print(f"It is {len(found_numbers)} numbers.")
    print(f"It ran for {final_time - initial_time} s.")


if __name__ == "__main__":
    main()
