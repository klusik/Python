"""
    How often is there repeating denominator
"""

# IMPORTS #
import fractions


# FUNCTIONS #
def create_list_denominator(denominator_count: int) -> list:
    sum_list = [fractions.Fraction(1, 1)]

    for item_idx, item in enumerate(range(denominator_count)):
        if item_idx:
            sum_list.append(sum_list[item_idx - 1] + fractions.Fraction(1, item) ** 2)

    return list(map(lambda frac: frac.denominator, sum_list))


def create_list_full(count_of_items: int) -> list:
    list_full = []

    list_denominators: list[int] = create_list_denominator(count_of_items)

    print(list_denominators)

    for denominator_idx, denominator in enumerate(list_denominators):
        if denominator_idx:
            denominator_diff = denominator - list_denominators[denominator_idx - 1]
            if denominator_diff:
                list_full.extend([denominator] * 1)
            else:
                list_full.append(denominator)

    return list_full


# RUNTIME #
if __name__ == "__main__":
    print(create_list_full(20))
