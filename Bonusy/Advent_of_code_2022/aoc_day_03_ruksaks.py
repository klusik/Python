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
    ruksak_separator = int(len(ruksak)/2)

    return ruksak[0:ruksak_separator], ruksak[ruksak_separator:]

def get_priority(item:str):
    if 'a' <= item <= 'z':
        return ord(item) - ord('a') + 1
    elif 'A' <= item <= 'Z':
        return ord(item) - ord('A') + 27
    else:
        raise ValueError('Input must be a letter')

def main():
    ruksaks = get_boxes()

    total_score = 0
    for ruksak in ruksaks:
        comp1, comp2 = get_compartments(ruksak)

        # get common letters
        common_items = list(set(comp2).intersection(set(comp1)))[0]

        total_score += get_priority(common_items)

    print(f"Total: {total_score}")



if __name__ == "__main__":
    main()
