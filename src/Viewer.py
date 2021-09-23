import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from src.ParticleModel import ParticleModel


def saveCurrentParticle(particleModel: ParticleModel, boxSize: float, pathSave: str):
    plt.clf()
    PPI = 72
    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')

    nParticles = particleModel.nParticles
    #lsColors = list(colors.cnames.keys())
    #lsColors = ['blue', 'orange', 'black', 'red', 'yellow', 'green', 'magenta', 'aqua']
    lsLabels = [f'particle{i}' for i in range(nParticles)]

    ax_length = axes.bbox.get_points()[1][0]-axes.bbox.get_points()[0][0]
    ax_point = ax_length*PPI/fig.dpi
    fact = ax_point/boxSize
    for iParticle in range(nParticles):
        particleCoords = particleModel.getParticleCoord(index=iParticle)
        particleRadius = particleModel.getParticleRadius(index=iParticle)
        size = particleRadius * fact
        #axes.scatter(particleCoords[0], particleCoords[1], particleCoords[2], s=size**2,
        #c=lsColors[iParticle], edgecolor=lsColors[iParticle], label=lsLabels[iParticle])
        axes.scatter(particleCoords[0], particleCoords[1], particleCoords[2], s=size**2, label=lsLabels[iParticle])

    axes.set_xlim3d(-boxSize/2, boxSize/2)
    axes.set_ylim3d(-boxSize/2, boxSize/2)
    axes.set_zlim3d(-boxSize/2, boxSize/2)
    axes.set_xlabel("X")
    axes.set_ylabel("Y")
    axes.set_zlabel("Z")
    if nParticles < 5:
        axes.legend()
    plt.savefig(pathSave)
    plt.close()
