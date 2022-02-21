"""

    Just dots and commas

"""

if __name__ == "__main__":
    some_numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    for index, number in enumerate(some_numbers):
        if index > 0:
            print(f", {number}", end="")
        else:
            print(f"{number}", end="")
    print(".")