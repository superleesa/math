__author__ = "Satoshi Kashima"
__studentid__ = "32678940"


def decimal_to_binary(decimal: int):
    """
    Convert a decimal integer into binary.
    :param decimal: an integer
    :return: a list containing bits, representing the original integer in binary
    """
    oup = []

    while decimal > 0:
        rem = decimal % 2
        oup.append(rem)
        decimal //= 2

    oup.reverse()
    return oup


def mod_exp(base: int, exponent: int, mod: int):
    """
    Solves Modular Exponentation with repeated squaring.
    :param base: the base value of an expression. e.g. if b^e % m then b is the base
    :param exponent: the exponent part
    :param mod: the modular part
    :return: the result of the modular exponentation
    """
    result = 1
    base = base % mod

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod

        base = (base * base) % mod
        exponent //= 2

    return result
