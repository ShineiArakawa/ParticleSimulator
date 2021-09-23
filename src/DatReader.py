import numpy as np


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