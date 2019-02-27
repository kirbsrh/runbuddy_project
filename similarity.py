from math import sqrt


def euclid(pairs):
    distance = sqrt(sum([pow(x - y, 2) for x, y in pairs]))
    return 1 / (1 + distance)

    