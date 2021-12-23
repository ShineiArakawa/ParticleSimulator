import os
from src.ParticleModel import ParticleModel

import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def saveCurrentParticle(particleModel: ParticleModel, boxSize: float, pathSave: str):
    plt.clf()
    PPI = 72
    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')

    nParticles = particleModel.nParticles
    # lsColors = list(colors.cnames.keys())
    # lsColors = ['blue', 'orange', 'black', 'red', 'yellow', 'green', 'magenta', 'aqua']
    lsLabels = [f'particle{i}' for i in range(nParticles)]

    ax_length = axes.bbox.get_points()[1][0]-axes.bbox.get_points()[0][0]
    ax_point = ax_length*PPI/fig.dpi
    fact = ax_point/boxSize
    for iParticle in range(nParticles):
        particleCoords = particleModel.getParticleCoord(index=iParticle)
        particleRadius = particleModel.getParticleRadius(index=iParticle)
        size = particleRadius * fact
        # axes.scatter(particleCoords[0], particleCoords[1], particleCoords[2], s=size**2,
        # c=lsColors[iParticle], edgecolor=lsColors[iParticle], label=lsLabels[iParticle])
        axes.scatter(particleCoords[0], particleCoords[1],
                     particleCoords[2], s=size**2, label=lsLabels[iParticle])

    axes.set_xlim3d(-boxSize/2 - boxSize/32, boxSize/2 + boxSize/32)
    axes.set_ylim3d(-boxSize/2 - boxSize/32, boxSize/2 + boxSize/32)
    axes.set_zlim3d(-boxSize/2 - boxSize/32, boxSize/2 + boxSize/32)
    axes.set_xlabel("X")
    axes.set_ylabel("Y")
    axes.set_zlabel("Z")
    #if nParticles < 5:
    #    axes.legend()
    plt.savefig(pathSave, dpi=500)
    plt.close()
    plt.clf()


def saveFigFromFile(pathProject: str):
    paths = []
    nParticles = -1
    boxSize = -1.0
    
    pathDirOutput = os.path.join(pathProject, 'results')
    if os.path.exists(pathDirOutput) is False:
        os.makedirs(pathDirOutput)
    
    with open(pathProject) as file:
        lines = file.readlines()

        nParticles = int(lines[0].replace('\n', ''))
        boxSize = float(lines[0].replace('\n', ''))
        for iter in range(2, len(lines)):
            line = lines[iter].replace('\n', '').split()
            paths.append(line)

    for iter in range(len(paths)):
        particleCoords = np.empty(shape=(nParticles, 3))
        particleVelocity = np.empty(shape=(nParticles, 3))
        particleMass = np.empty(shape=(nParticles,))
        particleRadius = np.empty(shape=(nParticles,))

        with open(paths[iter]) as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                line = line.replace('\n', '').split()
                particleRadius[i] = float(line[0])
                particleMass[i] = float(line[1])
                particleCoords[i][0] = float(line[2])
                particleCoords[i][1] = float(line[3])
                particleCoords[i][2] = float(line[4])
                particleVelocity[i][0] = float(line[5])
                particleVelocity[i][1] = float(line[6])
                particleVelocity[i][2] = float(line[7])

        particleModel = ParticleModel(nParticles=nParticles, initialPositions=particleCoords,
                                      initialVelocity=particleVelocity, radius=particleRadius, mass=particleMass)
        pathOurput = os.path.join(pathDirOutput, f'Iter_{iter}.jpg')
        saveCurrentParticle(particleModel=particleModel, boxSize=boxSize, pathSave=pathOurput)