"""
Implement the function unique_in_order which takes as argument
a sequence and returns a list of items without any elements
with the same value next to each other and preserving
the original order of elements.

For example:

unique_in_order('AAAABBBCCDAABBB') == ['A', 'B', 'C', 'D', 'A', 'B']
unique_in_order('ABBCcAD')         == ['A', 'B', 'C', 'c', 'A', 'D']
unique_in_order([1,2,2,3,3])       == [1,2,3]
"""

def unique_in_order(input_list):
    """ Main function """

    # Define output list
    output = list()

    # Go through all the items and add them to list
    for item_from_list in input_list:
        # If not first
        if len(output):
            # If not same as previous
            if item_from_list != output[-1]:
                output.append(item_from_list)
        else:
            # First
            output.append(item_from_list)

    return output


if __name__ == "__main__":
    input_value = "TEsssT"
    input_list = [1, 2, 3, 'test', input_value]

    print(unique_in_order(input_value))
    print(unique_in_order(input_list))