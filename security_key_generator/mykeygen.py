__author__ = "Satoshi Kashima"
__studentid__ = "32678940"

from gcd import gcd
from find_coprimes import find_random_coprime_value
from sieve_of_eratosthenes import generate_first_n_primes
from miller_rabin_test import miller_rabin_test

import sys

def generate_primes(d: int) -> tuple[int, int]:
    """
    Generate two primes p and q for private key.

    we have that, if x is a composite number then so is 2^x − 1. Hence, we ignore any 2^x-1 where x is not prime itself.
     to check if a number within 2 < d <= 2000 is a prime, we simply precompute all primes up to 2000 using
      sieve of eratosthenes. This is faster than using miller_rabin_test for each x.

    Raises a ValueError if there is no two primes in the specified range.
    :param d: the smallest x
    :return: (most likely) the two smallest primes in form of 2^x-1
    """
    primes = generate_first_n_primes(2000)  # this list should never be empty since there is 1 and 2
    p_and_q = []

    # finds the first index of a prime that is greater than or equal to d
    pointer = 0
    for i in range(len(primes)):
        prime = primes[i]
        if prime >= d:
            pointer = i
            break

    # traverse through the primes and see if 2^p-1 is also prime
    while pointer < len(primes) and len(p_and_q) < 2:
        x = primes[pointer]
        p_temp = (1 << x) - 1  # 2^x-1 (shifting to avoid overflow)
        if miller_rabin_test(p_temp, 10):
            p_and_q.append(p_temp)

        pointer += 1

    if len(p_and_q) < 2:
        raise ValueError("no two primes within d to 2000")

    return p_and_q[0], p_and_q[1]



def generate(d: int) -> tuple[int, int, int, int]:
    """
    Generates both the shared and private keys.

    :param d: the smallest x
    :return: p, q, mod, and e
    """
    p, q = generate_primes(d)
    mod = p*q
    lambda_ = (p-1)*(q-1) // gcd(p-1, q-1) - 1
    e = find_random_coprime_value(3, lambda_, lambda_)


    return p, q, mod, e

def output_public_key(mod: int, e: int):
    return "# modulus (n)\n" + str(mod) + "\n" + "# exponent (e)\n" + str(e)

def output_secret_primes(p: int, q: int):
    return "# p\n" + str(p) + "\n" + "# q\n" + str(q)


if __name__ == "__main__":
    # print(generate(500))
    _, d = sys.argv

    p, q, mod, e = generate(int(d))

    public_key_output_file_name = "publickeyinfo.txt"
    secret_primes_file_name = "secretprimes.txt"
    with open(public_key_output_file_name, "w") as file:
        file.write(output_public_key(mod, e))

    with open(secret_primes_file_name, "w") as file:
        file.write(output_secret_primes(p, q))
