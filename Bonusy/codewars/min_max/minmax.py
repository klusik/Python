def high_and_low(numbers):
    # Initial
    max_number = numbers[0]
    min_number = numbers[0]

    for number in numbers:
        if number < min_number:
            min_number = number
            print(min_number)
        if number > max_number:
            max_number = number

    return f"{max_number} {min_number}"


numbers = [1, 2, 3, 4, 5]
print(high_and_low(numbers))