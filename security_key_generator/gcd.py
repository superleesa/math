def gcd(a, b):
    """
    Euclidean algorithm
    :param a: an integer
    :param b: another integer
    :return: gcd of given integers
    """
    while b != 0:
        a, b = b, a % b
    return a
