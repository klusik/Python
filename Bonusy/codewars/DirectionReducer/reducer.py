"""
    CW: https://www.codewars.com/kata/550f22f4d758534c1100025a/train/python
"""

def dirReduc(input_array):
    wests = input_array.count("WEST")
    easts = input_array.count("EAST")
    norths = input_array.count("NORTH")
    souths = input_array.count("SOUTH")

    output = list()

    for index, way in enumerate(input_array):
        if index+1 < len(input_array):
            if way == "NORTH":
                pass

    return output

if __name__ == "__main__":
    array = ["WEST", "SOUTH", "EAST"]
    dirReduct(array)