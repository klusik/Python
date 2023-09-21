"""
    There is a queue for the self-checkout tills at the supermarket.
    Your task is write a function to calculate the total time required for all the customers to check out!

    input
    customers: an array of positive integers representing the queue.
    Each integer represents a customer, and its value is the amount of time they require to check out.
    n: a positive integer, the number of checkout tills.
    output
    The function should return an integer, the total time required.

    Important
    Please look at the examples and clarifications below, to ensure you understand the task correctly :)

    Examples
    queue_time([5,3,4], 1)
    # should return 12
    # because when n=1, the total time is just the sum of the times

    queue_time([10,2,3,3], 2)
    # should return 10
    # because here n=2 and the 2nd, 3rd, and 4th people in the
    # queue finish before the 1st person has finished.

    queue_time([2,3,10], 2)
    # should return 12
    Clarifications
    There is only ONE queue serving many tills, and
    The order of the queue NEVER changes, and
    The front person in the queue (i.e. the first element in the array/list)
    proceeds to a till as soon as it becomes free.
    N.B. You should assume that all the test input will be valid, as specified above.
"""
# IMPORTS #
import threading
import queue
import time


# RUNTIME #
def checkout_customer(customers_queue: queue.Queue,
                      till_number: int,
                      time_queue:queue.Queue,
                      ):
    """ Checks out a customer (going from queue) """

    # Time counter reset for given till
    till_total_time = 0

    # Sleep ratio (lower means fastest simulation)
    sleep_ratio = 0.01

    # Work with a queue
    while not customers_queue.empty():
        # Get a next customer from a queue
        customer = customers_queue.get()

        # Sleep for a while so threading could solve it
        time.sleep(customer * sleep_ratio)

        # Adding a current customer time to till time counter
        till_total_time += customer

    time_queue.put(till_total_time)
    return till_total_time


def queue_time(customers, tiles):
    """ Returns maximal value for time """

    # Going through all customers and using queue

    # Create a customer queue
    customers_queue = queue.Queue()

    # Create a time queue
    time_queue = queue.Queue()

    # Populate queue
    for customer in customers:
        customers_queue.put(customer)

    # List of threads
    till_threads = []

    # Go through all tilles and create single thread for each
    for till in range(tiles):
        till_thread = threading.Thread(target=checkout_customer, args=(customers_queue, till, time_queue))
        till_threads.append(till_thread)
        till_thread.start()

    for till_thread in till_threads:
        till_thread.join()

    # Total time from queues
    total_time = 0
    while not time_queue.empty():
        total_time += time_queue.get()

    # print(f"Done. Total time used was {total_time}")
    return total_time


if __name__ == "__main__":
    customers = [3, 2, 7, 3]
    tiles = 2

    print(queue_time(customers, tiles))
