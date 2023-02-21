""" Some stuff with heaps """

import heapq
import random
import time

if __name__ == "__main__":
    hp = []
    hp2 = []

    rng = 1_000_000

    t_hp1 = time.time()
    for _ in range(rng):
        heapq.heappush(hp, random.randint(1, 10000))

    print("heap insertion: ", time.time() - t_hp1)

    hp = []
    t_hp2 = time.time()
    for _ in range(rng):
        hp2.append(random.randint(1, 10000))

    print("normal list insertion: ", time.time() - t_hp2)

    hp_new = []
    for number in hp:
        heapq.heappush(hp_new, number)
