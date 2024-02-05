"""
    Program multiplies entered number n-times by 2
"""

number = int(input("Enter the number: "))

while True:
    amount_of_rotations = int(input("How many times to multiply by 2 (1--16): "))
    if 1 <= amount_of_rotations <= 16:
        break
    
# The goal is simple; program just takes the number, for example if you enter 67,
# it is 1000011 in binary 
# 
# So if you enter the 'amount of rotations' for example 3, it means
# it will 3 times multiply by 2, to 2 * 2 * 2 -- 2 powered by 3, so 2^3.
#
# So if you enter 67 and for example 5, it would basically compute:
#
# result = 67 * 2 ^ amount_of_rotations

# This is the "basic way", I'd rather add braces for clarity
result_old_way = number * (2 ** amount_of_rotations)

# Rotation method
# This is MUCH faster, because you don't multiplying and powering any number, you just
# bit-shift the original number :-)
result_rotation_way = number << amount_of_rotations


# Output:
print(f"By the old method: {number} x 2^{amount_of_rotations} = {result_old_way}.")
print(f"By the new method: {number} x 2^{amount_of_rotations} = {result_rotation_way}.")




