from math import*
import numpy


def euclid(pairs):
    distance = sqrt(sum([pow(x - y, 2) for x, y in pairs]))
    max_distance = 6.324555320336759
    similarity = 1-(distance/max_distance)
    #return 1 / (1 + distance)
    return round(similarity*100, 2)

 
def square_rooted(x):
 
    return round(sqrt(sum([a*a for a in x])),3)
 
# def cosine_similarity(x,y):
 
#     numerator = sum(a*b for a,b in zip(x,y))
#     denominator = square_rooted(x)*square_rooted(y)
#     return round(numerator/float(denominator),3)
 
def cosine_similarity(x, y):
    similarity = numpy.dot(x, y) /(numpy.sqrt(numpy.dot(x, x)) * numpy.sqrt(numpy.dot(y, y)))
    return similarity 


def corrcoef(x,y):
    numps_similarity = numpy.corrcoef(x,y)
    return numps_similarity
