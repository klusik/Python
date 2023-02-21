"""
    Elfové
"""

# RUNTIME #
if __name__ == "__main__":
    # Open file
    with open("d1t1_input.txt", "r") as f_input:
        data = f_input.read()

    # Separate by empty lines
    data_packs = data.split('\n\n')

    # Create list of sums of elven work and select the maximal (for each elf)
    max_elf = sum(
        sorted(
            list(
                map(
                    lambda l: (sum(list(map(int, l.split())))),
                    data_packs
                )
        ), reverse=True)[0:3]
    )
    print(max_elf)











