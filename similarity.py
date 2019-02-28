from math import*
import numpy


def euclid(pairs):
    distance = sqrt(sum([pow(x - y, 2) for x, y in pairs]))
    return 1 / (1 + distance)

 
def square_rooted(x):
 
    return round(sqrt(sum([a*a for a in x])),3)
 
# def cosine_similarity(x,y):
 
#     numerator = sum(a*b for a,b in zip(x,y))
#     denominator = square_rooted(x)*square_rooted(y)
#     return round(numerator/float(denominator),3)
 
def cosine_similarity(x, y):
    similarity = numpy.dot(x, y) /(numpy.sqrt(numpy.dot(x, x)) * numpy.sqrt(numpy.dot(y, y)))
    return numpy.around(similarity,3) 