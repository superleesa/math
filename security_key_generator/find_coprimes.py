__author__ = "Satoshi Kashima"
__studentid__ = "32678940"


from gcd import gcd

from random import randint

def find_random_coprime_value(start: int, end: int, other: int):
    """
    Find a random coprime value. It randomely selects which index to start searching for a coprime and returns the first
    of such occurrences. It uses GCD function to decide if two values are coprimes or not.

    :param start: inclusive
    :param end: exclusive
    :param other: the other value
    :return: a random coprime
    """

    start_traversal_num = randint(start, end-1)
    for n in range(start_traversal_num, end):
        if gcd(n, other) == 1:
            return n

    for n in range(start, start_traversal_num):
        if gcd(n, other) == 1:
            return n

    raise ValueError("No coprimes found")