__author__ = "Satoshi Kashima"
__studentid__ = "32678940"


from random import randint, sample
from modular_exponentation import mod_exp

def miller_rabin_test(n: int, k: int):
    """
    Implementation of Miller Rabin Primality test. It returns False if the given value is definitely composite.
    Returns True if probably prime.
    :param n: the number to test
    :param k: the number of witnesses i.e. number of "a"s
    :return: False if the given value is definitely composite, True if probably prime.
    """
    # special cases
    if n == 2:
        return True

    # check if n is even number
    if n % 2 == 0 or n < 0:
        return False

    # decompose n-1 into 2^s.t
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2

    # generating k "a"s
    bases = set()
    while len(bases) < k:
        a = randint(2, n - 2)
        bases.add(a)

    # actual testing procedure
    for a in bases:
        # Fermat's little theorem
        if mod_exp(a, n-1, n) != 1:
            return False

        # obs2
        current = mod_exp(a, t, n)
        for _ in range(1, s + 1):
            previous = current
            current = previous*previous % n

            if current == 1 and previous != n-1 and previous != 1:
                return False

    return True