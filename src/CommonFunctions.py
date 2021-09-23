import numpy as np


def calcLength(vector: np.ndarray):
    vector = np.power(vector, 2)
    vectorSum = np.sum(vector)
    length = np.sqrt(vectorSum)
    return length

def calcUnitVector(vector: np.ndarray):
    length = calcLength(vector=vector)
    return vector / length

def calcSymmetricVector(vector: np.ndarray, pole: np.ndarray):
    unitPole = calcUnitVector(pole)
    len1 = np.dot(vector, unitPole)
    tempVec1 = len1 * unitPole
    tempVec2 = tempVec1 - vector
    symmetricVector = vector + 2 * tempVec2 
    return symmetricVector