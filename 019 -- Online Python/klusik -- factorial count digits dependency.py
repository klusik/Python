# Create a list of tuplets in format
# [(n, length(n!), ratio), ...]
#
# This could be exported to excel or gnuplot

# IMPORTS
import numpy

# FUNCTIONS
def factorialLength(inputN):
    """Returns a tuple (input, length(input!))"""
    length = len(str(numpy.math.factorial(inputN)))
    return (inputN, length, float(length/inputN))

def main():
    # Create a list for tuples
    factorialLenghts = list()

    # user input: maximum value
    try:
        maxN = abs(int(input("Enter the max n for n!: ")))
    except ValueError:
        print("Incorrect value.")
        return False

    # Filling up the list
    for n in range(1, maxN+1):
        try:
            if n%100 == 0:
                print(f"Processing for n = {n}.")

            factorialLenghts.append(factorialLength(n))

        except Exception as exception:
            raise(exception)

    # Output
    print(factorialLenghts)



if __name__ == "__main__":
    main()
