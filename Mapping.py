from numpy.core.numeric import outer
from src.DatReader import readDatFile
from src.Environment import Cube, EnvComb
from src.Physics import Physics
from src.ParticleModel import ParticleModel

import numpy as np
import sys


def main(args):
    seed = 0
    ro = 1
    boxSize = 100
    maxTime = 1
    userRandom = np.random
    userRandom.seed(seed=seed)
    if len(args) < 2:
        nParticles = 1000
        initPosition = np.random.rand(nParticles, 3) * boxSize - boxSize / 2
        initVelocity = np.empty(shape=(nParticles, 3))
        amp = 1000
        theta = np.random.rand(int(np.sqrt(nParticles))) * 90 + 90
        theta = np.deg2rad(theta)
        phi = np.random.rand(int(np.sqrt(nParticles))) * 360
        phi = np.deg2rad(phi)
        for i in range(theta.shape[0]):
            for j in range(phi.shape[0]):
                index = i * phi.shape[0] + j
                initVelocity[index][0] = amp * np.sin(theta[i]) * np.cos(phi[j])
                initVelocity[index][1] = amp * np.sin(theta[i]) * np.sin(phi[j])
                initVelocity[index][2] = amp * np.cos(theta[i])

        #radius = np.empty(shape=(nParticles,))
        #mass = np.empty(shape=(nParticles,))
        #initPosition[0][0] = -5.0
        #initPosition[0][1] = 0.0
        #initPosition[0][2] = 0.0
        #initPosition[1][0] = 5.0
        #initPosition[1][1] = 0.0
        #initPosition[1][2] = 0.0
        #initVelocity[0][0] = 20.0
        #initVelocity[0][1] = 0.0
        #initVelocity[0][2] = 0.0
        #initVelocity[1][0] = -20.0
        #initVelocity[1][1] = 0.0
        #initVelocity[1][2] = 0.0
        #radius[0] = 2.0
        #radius[1] = 3.0
        #mass[0] = 1.0
        #mass[1] = 1.0
                
        radius = np.random.rand(nParticles)
        mass = 4 / 3 * np.pi * np.power(radius.copy(), 3) * ro 
    else:
        pathDatFile = args[1]
        nParticles, initPosition, radius = readDatFile(pathFile=pathDatFile)
        initVelocity = (userRandom.rand(nParticles, 3) - 0.5) * 500
        mass = radius.copy()

    particleModel = ParticleModel(nParticles=nParticles, initialPositions=initPosition,
                                  initialVelocity=initVelocity, radius=radius, mass=mass)
    
    outerCube = Cube(width=boxSize)
    environment = EnvComb(environments=[outerCube])
    
    physics = Physics(particleModel=particleModel, environment=environment)
    physics.simulate(maxTime=maxTime, boxSize=boxSize)


if __name__ == '__main__':
    args = sys.argv
    main(args)
