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


class Physics:
    FPS = 1000
    DURATION = 1000 / FPS
    COEFFICIENT_OF_RESTITUTION = 1.0

    def __init__(self, particleModel: ParticleModel, environment: Environment):
        self.__particleModel = particleModel
        self.__environment = environment

    def __update(self):
        timeSpan = 1 / self.FPS
        nParticles = self.__particleModel.nParticles
        for iParticle in range(nParticles):
            coord = self.__particleModel.getParticleCoord(index=iParticle)
            velocity = self.__particleModel.getParticleVelocity(
                index=iParticle)
            coord = coord + velocity * timeSpan
            self.__particleModel.setParticleCoord(index=iParticle, coord=coord)

        lsConbi = list(itertools.combinations(range(nParticles), 2))
        for conbi in lsConbi:
            i = conbi[0]
            j = conbi[1]
            isHit = self.__particleModel.isHit(i, j)
            if isHit:
                iVelocity = self.__particleModel.getParticleVelocity(i)
                jVelocity = self.__particleModel.getParticleVelocity(j)
                self.__reboundWithOtherParticle(i, j)
        self.__environment.calcHitWall(particleModel=self.__particleModel)

    def simulate(self, maxTime: float, boxSize: float, pathSave: str = './data'):
        if os.path.exists(pathSave) is False:
            os.makedirs(pathSave)
        maxIter = maxTime * self.FPS
        for iter in tqdm(range(maxIter)):
            self.__update()
            saveCurrentParticle(particleModel=self.__particleModel, boxSize=boxSize,
                               pathSave=pathSave+f'/iter_{iter}.png')
            #writeDauFile(iter=iter, particleModel=self.__particleModel)

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

    @staticmethod
    def atoi(text):
        return int(text) if text.isdigit() else text

    @staticmethod
    def natural_keys(text):
        return [Physics.atoi(c) for c in re.split(r'(\d+)', text)]

    def createGif(self, dirPath: str = './data', pathGif: str = './data/summary.gif'):
        path_list = sorted(
            glob.glob(os.path.join(*[dirPath, '*.png'])), key=Physics.natural_keys)
        imgs = []

        for i in range(len(path_list)):
            img = Image.open(path_list[i])
            imgs.append(img)

        imgs[0].save(pathGif,
                     save_all=True, append_images=imgs[1:], optimize=False, duration=self.DURATION, loop=0)
