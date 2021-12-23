from typing import List
import numpy as np
from numpy.lib.twodim_base import mask_indices


class ParticleModel:
    def __init__(self, nParticles: int, initialPositions: np.ndarray, initialVelocity: np.ndarray, radius: np.ndarray, mass: np.ndarray) -> None:
        self.__particles: List[Particle] = list()
        self.nParticles = nParticles
        for iParticle in range(nParticles):
            particle = Particle(
                initialPosition=initialPositions[iParticle], initialVelocity=initialVelocity[iParticle], radius=radius[iParticle], mass=mass[iParticle])
            self.__particles.append(particle)
        self.__nHitEnvironment = np.zeros(shape=nParticles)

    def isHit(self, i: int, j: int):
        isHit = False
        iParticleCoord = self.__particles[i].position
        jParticleCoord = self.__particles[j].position
        iParticleRadius = self.__particles[i].radius
        jParticleRadius = self.__particles[j].radius
        distance = np.sqrt(np.sum(np.power(iParticleCoord-jParticleCoord, 2)))
        if distance <= iParticleRadius + jParticleRadius:
            isHit = True
        return isHit

    def getParticleCoord(self, index: int) -> np.ndarray:
        particle: Particle = self.__particles[index]
        coord = particle.position
        return coord

    def setParticleCoord(self, index: int, coord: np.ndarray):
        particle: Particle = self.__particles[index]
        particle.position = coord

    def getParticleVelocity(self, index: int) -> np.ndarray:
        particle: Particle = self.__particles[index]
        velocity = particle.velocity
        return velocity

    def setParticleVelocity(self, index: int, velocity: np.ndarray):
        particle: Particle = self.__particles[index]
        particle.velocity = velocity

    def getParticleRadius(self, index: int) -> np.float64:
        particle: Particle = self.__particles[index]
        radius = particle.radius
        return radius

    def getParticleMass(self, index: int) -> np.float64:
        particle: Particle = self.__particles[index]
        mass = particle.mass
        return mass
    
    def getNumHitWall(self, index: int) -> int:
        return self.__nHitEnvironment[index]

    def setNumHitWall(self, index: int, nHit: int) -> int:
        self.__nHitEnvironment[index] = nHit
        
    def step(self, timeSpan: float):
        for i in range(self.nParticles):
            self.__particles[i].position = self.__particles[i].position + self.__particles[i].velocity * timeSpan


class Particle:
    def __init__(self, initialPosition: np.ndarray, initialVelocity: np.ndarray, radius: np.float64, mass: np.float64) -> None:
        self.__position: np.ndarray = initialPosition
        self.__velocity: np.ndarray = initialVelocity
        self.__radius: np.float64 = radius
        self.__mass: np.float64 = mass

    @property
    def position(self):
        pass

    @position.getter
    def position(self):
        return self.__position

    @position.setter
    def position(self, position: np.ndarray):
        self.__position = position

    @property
    def velocity(self):
        pass

    @velocity.getter
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity: np.ndarray):
        self.__velocity = velocity

    @property
    def radius(self):
        pass

    @radius.getter
    def radius(self):
        return self.__radius

    @property
    def mass(self):
        pass

    @mass.getter
    def mass(self):
        return self.__mass
