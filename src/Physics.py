from src.DatReader import writeDauFile
from src.Environment import Cube, Environment
from src.Viewer import saveCurrentParticle
from src.ParticleModel import ParticleModel
from src.CommonFunctions import calcUnitVector

import os
from PIL import Image
import glob
import sys
import re
from tqdm import tqdm
import itertools
import numpy as np
from multiprocessing import Process

class Physics(Process):
    FPS = 1000
    DURATION = 1000 / FPS
    COEFFICIENT_OF_RESTITUTION = 1.0

    def __init__(self, particleModel: ParticleModel, environment: Environment):
        super(Physics, self).__init__()
        self.__particleModel = particleModel
        self.__environment = environment

    def __update(self):
        timeSpan = 1 / self.FPS
        nParticles = self.__particleModel.nParticles
        self.__particleModel.step(timeSpan=timeSpan)

        lsConbi = list(itertools.combinations(range(nParticles), 2))
        for conbi in lsConbi:
            i = conbi[0]
            j = conbi[1]
            isHit = self.__particleModel.isHit(i, j)
            if isHit:
                self.__reboundWithOtherParticle(i, j)
        self.__environment.calcHitWall(particleModel=self.__particleModel)

    def simulate(self, maxTime: float, boxSize: float, pathSave: str = './data'):
        if os.path.exists(pathSave) is False:
            os.makedirs(pathSave)
        maxIter = maxTime * self.FPS
        for iter in tqdm(range(maxIter)):
            self.__update()
            for i in range(self.__particleModel.nParticles):
                if self.__particleModel.getParticleVelocity(i)[0] > 10e8:
                    print("iter= ", iter)
                    quit()
            #saveCurrentParticle(particleModel=self.__particleModel, boxSize=boxSize,
            #                   pathSave=pathSave+f'/iter_{iter}.png')
            writeDauFile(iter=iter, particleModel=self.__particleModel)

    def __reboundWithOtherParticle(self, i: int, j: int) -> tuple:
        iCoord = self.__particleModel.getParticleCoord(i)
        jCoord = self.__particleModel.getParticleCoord(j)
        iVelocity = self.__particleModel.getParticleVelocity(i)
        jVelocity = self.__particleModel.getParticleVelocity(j)
        iRadius = self.__particleModel.getParticleRadius(i)
        jRadius = self.__particleModel.getParticleRadius(j)
        iMass = self.__particleModel.getParticleMass(i)
        jMass = self.__particleModel.getParticleMass(j)

        actionLineVector = jCoord - iCoord
        unitActionLineVector = calcUnitVector(actionLineVector)
        v1PreParallel = np.dot(unitActionLineVector, iVelocity)
        v2PreParallel = np.dot(-unitActionLineVector, jVelocity)
        v1AfterParallel = (v1PreParallel + jMass * (1 + self.COEFFICIENT_OF_RESTITUTION) * (
            v2PreParallel - v1PreParallel) / (iMass + jMass)) * unitActionLineVector
        v2AfterParallel = (v2PreParallel - iMass * (1 + self.COEFFICIENT_OF_RESTITUTION)
                           * (v2PreParallel - v1PreParallel) / (iMass + jMass)) * unitActionLineVector
        v1AfterPerpendicular = iVelocity - unitActionLineVector * v1PreParallel
        v2AfterPerpendicular = jVelocity + unitActionLineVector * v2PreParallel
        iVelocityAfter = v1AfterParallel + v1AfterPerpendicular
        jVelocityAfter = v2AfterParallel + v2AfterPerpendicular

        self.__particleModel.setParticleVelocity(
            index=i, velocity=iVelocityAfter)
        self.__particleModel.setParticleVelocity(
            index=j, velocity=jVelocityAfter)
        
        energyPre = 0.5 * iMass * np.sqrt(np.sum(np.power(iVelocity, 2))) + 0.5 * jMass * np.sqrt(np.sum(np.power(jVelocity, 2)))
        energyAfter = 0.5 * iMass * np.sqrt(np.sum(np.power(iVelocityAfter, 2))) + 0.5 * jMass * np.sqrt(np.sum(np.power(jVelocityAfter, 2)))
        if np.abs(energyPre - energyAfter) > 0.5:
            print(f"Error particle: pre= {energyPre}, after= {energyAfter}")