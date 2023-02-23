"""
    Boxes
"""


# RUNTIME #
def get_boxes():
    with open('aoc_day_03.txt', 'r') as f_ruksaks:
        ruksaks = f_ruksaks.read()

    return str(ruksaks).split('\n')


def get_compartments(ruksak: str) -> (str, str):
    """ Divide ruksak to two compartments and return those halves """
    ruksak_separator = int(len(ruksak) / 2)

    return ruksak[0:ruksak_separator], ruksak[ruksak_separator:]


def get_priority(item: str):
    if 'a' <= item <= 'z':
        return ord(item) - ord('a') + 1
    elif 'A' <= item <= 'Z':
        return ord(item) - ord('A') + 27
    else:
        raise ValueError('Input must be a letter')


def main():
    ruksaks = get_boxes()

    # PART 1 #
    total_score = 0
    for ruksak in ruksaks:
        comp1, comp2 = get_compartments(ruksak)

        # get common letters
        common_items = list(set(comp2).intersection(set(comp1)))[0]

        total_score += get_priority(common_items)

    print(f"Total: {total_score}")

    # PART 2 #
    batch_ruksaks = []
    total_score = 0
    for ruksak in ruksaks:
        batch_ruksaks.append(ruksak)
        if len(batch_ruksaks) == 3:
            three_ruksaks = set.intersection(*list(map(set, batch_ruksaks)))
            batch_ruksaks.clear()
            total_score += sum(map(get_priority, three_ruksaks))
            print(three_ruksaks, total_score)

    print(f"Three ruksaks: {total_score}")


if __name__ == "__main__":
    main()
