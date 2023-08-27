__author__ = "Satoshi Kashima"
__studentid__ = "32678940"


def generate_first_n_primes(n: int):
    """
    Generate all prime numbers until n using Sieve of Eratosthenes.
    :param n: the end value
    :return: all prime numbers untill n in sorted order.
    """
    #todo add start if possible
    primes_indices = [True]*n

    for factor in range(2, n):
        for i in range(2*factor, n+1, factor):
            primes_indices[i-2] = False

    primes_indices[0] = True

    primes = []
    for i in range(n):
        if primes_indices[i]:
            primes.append(i+2)

    return primes