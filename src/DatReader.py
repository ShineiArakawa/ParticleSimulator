from src.ParticleModel import ParticleModel

import numpy as np
import os


def readDatFile(pathFile):
    with open(file=pathFile) as file:
        lines = file.readlines()

        nParticles = int(lines[0].split()[0])
        radius = np.empty(shape=nParticles, dtype=np.float64)
        particleCoords = np.empty(shape=(nParticles, 3), dtype=np.float64)

        for iLine in range(1, len(lines)):
            iLineList = lines[iLine].split()
            particleID = iLine - 1
            iParticleRadius = float(iLineList[3])
            iParticleCoordX = float(iLineList[4])
            iParticleCoordY = float(iLineList[5])
            iParticleCoordZ = float(iLineList[6])

            radius[particleID] = iParticleRadius
            particleCoords[particleID][0] = iParticleCoordX
            particleCoords[particleID][1] = iParticleCoordY
            particleCoords[particleID][2] = iParticleCoordZ

    return nParticles, particleCoords, radius


def writeDauFile(iter: int, particleModel: ParticleModel):
    saveDir = './output'
    if os.path.exists(saveDir) is False:
        os.makedirs(saveDir)

    nParticles = particleModel.nParticles
    savePath = saveDir + f'/iter_{iter}.dat'
    with open(file=savePath, mode='w') as file:
        file.write(f'{addBlank(nParticles, 10)}\n')
        for iParticle in range(nParticles):
            coord = particleModel.getParticleCoord(index=iParticle)
            velocity = particleModel.getParticleVelocity(index=iParticle)
            radius = particleModel.getParticleRadius(index=iParticle)
            string = f'{addBlank(iParticle, 10)}{addBlank(radius, 15)}{addBlank(coord[0], 15)}{addBlank(coord[1], 15)}{addBlank(coord[2], 15)}{addBlank(velocity[0], 15)}{addBlank(velocity[1], 15)}{addBlank(velocity[2], 15)}\n'
            file.write(string)


def addBlank(value, length: int):
    string = str(value)
    if type(value) == np.float64:
        string = '{:.5f}'.format(value)

    string = string.rjust(length)

    if len(string) > length:
        string = string[0:length]
    return string
