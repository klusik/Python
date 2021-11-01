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
    with concurrent.futures.ThreadPoolExecutor(max_workers = 100) as executor:
        executor.map(dummyFunction, range(400, 300, -1))
    pass

if __name__ == "__main__":
    main()