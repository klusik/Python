# Collatz
#
# If a number is odd, do 3x + 1.
# If a number is even, do x / 2.
#
# Repeat until the result is 1.
# Track all progress.
# Enter the biggest number to test.


def user_input():
    while True:
        number = int(input("Input a number n>1: "))
        if number > 1:
            return number


def collatz_sequences(max_number):
    # Cache complete suffixes for starting values within the requested range.
    # This avoids recomputing shared tails while keeping cache growth bounded.
    cache = {1: (1,)}

    for start in range(1, max_number + 1):
        if start == 1:
            yield start, (1, 4, 2, 1)
            continue

        current = start
        path = []
        cached_tail = None

        while cached_tail is None:
            cached_tail = cache.get(current)
            if cached_tail is not None:
                break

            path.append(current)
            if current & 1:
                current = (current * 3) + 1
            else:
                current >>= 1

        sequence = tuple(path) + cached_tail

        # Populate cache only for values inside the requested range.
        for index, value in enumerate(path):
            if value <= max_number and value not in cache:
                cache[value] = sequence[index:]

        yield start, sequence


def write_output(max_number, output_path="output.txt"):
    with open(output_path, "w", encoding="utf-8") as file_link:
        for start, sequence in collatz_sequences(max_number):
            file_link.write(
                f"{start} (length = {len(sequence)}): {list(sequence)}\n"
            )


def main():
    max_number = user_input()
    print(f"maxNumber = {max_number}")
    write_output(max_number)


if __name__ == "__main__":
    main()
