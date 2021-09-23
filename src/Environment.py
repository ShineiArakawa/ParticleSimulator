from src.CommonFunctions import calcSymmetricVector
from src.ParticleModel import ParticleModel

from abc import abstractmethod
from typing import overload
import numpy as np


class Environment:
    def __init__(self):
        pass

    @abstractmethod
    def calcHitWall(self, coord: np.ndarray, radius: np.float64):
        pass


class Cube(Environment):
    LABEL_FACE_INVALID = -1
    LABEL_FACE_XY_MIN = 0
    LABEL_FACE_XY_MAX = 1
    LABEL_FACE_YZ_MIN = 2
    LABEL_FACE_YZ_MAX = 3
    LABEL_FACE_ZX_MIN = 4
    LABEL_FACE_ZX_MAX = 5
    LIST_LABEL_FACE = [LABEL_FACE_XY_MIN,
                       LABEL_FACE_XY_MAX,
                       LABEL_FACE_YZ_MIN,
                       LABEL_FACE_YZ_MAX,
                       LABEL_FACE_ZX_MIN,
                       LABEL_FACE_ZX_MAX]
    UNIT_PERPENDICULAR_VECTOR_XY_MIN = np.array([0, 0, 1])
    UNIT_PERPENDICULAR_VECTOR_XY_MAX = np.array([0, 0, -1])
    UNIT_PERPENDICULAR_VECTOR_YZ_MIN = np.array([1, 0, 0])
    UNIT_PERPENDICULAR_VECTOR_YZ_MAX = np.array([-1, 0, 0])
    UNIT_PERPENDICULAR_VECTOR_ZX_MIN = np.array([0, 1, 0])
    UNIT_PERPENDICULAR_VECTOR_ZX_MAX = np.array([0, -1, 0])

    LIST_UNIT_PERPENDICULAR_VECTOR = [UNIT_PERPENDICULAR_VECTOR_XY_MIN,
                                      UNIT_PERPENDICULAR_VECTOR_XY_MAX,
                                      UNIT_PERPENDICULAR_VECTOR_YZ_MIN,
                                      UNIT_PERPENDICULAR_VECTOR_YZ_MAX,
                                      UNIT_PERPENDICULAR_VECTOR_ZX_MIN,
                                      UNIT_PERPENDICULAR_VECTOR_ZX_MAX]

    def __init__(self, width: float) -> None:
        super(Cube, self).__init__()
        self.__boundX = np.array([-width/2, width/2])
        self.__boundY = np.array([-width/2, width/2])
        self.__boundZ = np.array([-width/2, width/2])

    def calcHitWall(self, particleModel: ParticleModel):
        nParticles = particleModel.nParticles
        for iParticle in range(nParticles):
            coord = particleModel.getParticleCoord(index=iParticle)
            radius = particleModel.getParticleRadius(index=iParticle)
            faceID = []
            minCoord = coord - radius
            maxCoord = coord + radius

            if minCoord[0] < self.__boundX[0]:
                faceID.append(self.LABEL_FACE_YZ_MIN)
            if minCoord[1] < self.__boundY[0]:
                faceID.append(self.LABEL_FACE_ZX_MIN)
            if minCoord[2] < self.__boundZ[0]:
                faceID.append(self.LABEL_FACE_XY_MIN)
            if maxCoord[0] > self.__boundX[1]:
                faceID.append(self.LABEL_FACE_YZ_MAX)
            if maxCoord[1] > self.__boundY[1]:
                faceID.append(self.LABEL_FACE_ZX_MAX)
            if minCoord[2] > self.__boundZ[1]:
                faceID.append(self.LABEL_FACE_XY_MAX)

            if len(faceID) == 0:
                continue
            else:
                tmp = np.array([self.__boundZ[0] - minCoord[2],
                                maxCoord[2] - self.__boundZ[1],
                                self.__boundX[0] - minCoord[0],
                                maxCoord[0] - self.__boundX[1],
                                self.__boundY[0] - minCoord[1],
                                maxCoord[1] - self.__boundY[1]])
                mostDeepHit = self.LIST_LABEL_FACE[np.argmax(tmp)]
                perpendicularVector = self.LIST_UNIT_PERPENDICULAR_VECTOR[mostDeepHit]
                preVelocity = particleModel.getParticleVelocity(
                    index=iParticle)
                afterVelocity = - calcSymmetricVector(
                    vector=preVelocity, pole=perpendicularVector)
                particleModel.setParticleVelocity(
                    index=iParticle, velocity=afterVelocity)
