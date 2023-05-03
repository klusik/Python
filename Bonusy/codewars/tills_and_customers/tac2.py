"""
    Same as tac, but simplier without threading
"""

def queue_time(customers, tiles):
    if tiles == 1:
        return sum(customers)
    elif tiles > len(customers):
        return max(customers)
    else:
        tills = [0] * tiles
        while customers:
            tills[tills.index(min(tills))] += customers.pop(0)

        return max(tills)


