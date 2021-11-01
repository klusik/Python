"""

Exploring Threads

Author: klusik@klusik.cz

"""

import threading
import concurrent.futures

def dummyFunction(numberOfRepetitons):
    sum = 0
    for _ in range(numberOfRepetitons):
        sum += 2 ** numberOfRepetitons
    print(f"For {numberOfRepetitons} repeptions is sum = {sum} ")
    return sum

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers = 500) as executor:
        executor.map(dummyFunction, range(11110, 11000, -1))
    pass

if __name__ == "__main__":
    main()