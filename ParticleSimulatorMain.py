from src.DatReader import readDatFile
from src.Environment import Cube
from src.Physics import Physics
from src.ParticleModel import ParticleModel

import numpy as np
import sys


def main(args):
    seed = 0
    boxSize = 100
    maxTime = 1
    userRandom = np.random
    userRandom.seed(seed=seed)
    if len(args) < 2:
        nParticles = 8
        initialPosition = np.array([[40, 40, 40],
                                    [40, 40, -40],
                                    [40, -40, 40],
                                    [-40, 40, 40],
                                    [40, -40, -40],
                                    [-40, 40, -40],
                                    [-40, -40, 40],
                                    [-40, -40, -40]])
        initialVelocity = (userRandom.rand(nParticles, 3) - 0.5) * 500
        radius = np.array([5, 5, 5, 5, 5, 5, 5, 5])
        mass = np.array([1, 1, 1, 1, 1, 1, 1, 1])
    else:
        pathDatFile = args[1]
        nParticles, initialPosition, radius = readDatFile(pathFile=pathDatFile)
        initialVelocity = (userRandom.rand(nParticles, 3) - 0.5) * 500
        mass = radius.copy()

    particleModel = ParticleModel(nParticles=nParticles, initialPositions=initialPosition,
                                  initialVelocity=initialVelocity, radius=radius, mass=mass)
    environment = Cube(width=boxSize)
    physics = Physics(particleModel=particleModel, environment=environment)
    physics.simulate(maxTime=maxTime, boxSize=boxSize)


if __name__ == '__main__':
    args = sys.argv
    main(args)
