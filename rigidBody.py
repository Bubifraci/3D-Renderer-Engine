import numpy as np

class RigidBody:
    def __init__(self, mass, startPos):
        self.mass = mass
        self.position = np.asarray(startPos, dtype=float)
        self.forces = [np.array([0, 0, 9.81]) * mass]
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.impulses = []

    def computeNewPosition(self, dT):

        acceleration = np.zeros(3)
        dVelocity = np.zeros(3)

        if self.impulses:
            dVelocity = np.sum(self.impulses, axis=0) / self.mass
            self.impulses.clear()

        if self.forces:
            acceleration = np.sum(self.forces, axis=0) / self.mass

        self.velocity += dVelocity + acceleration * dT
        self.position += self.velocity * dT

        return self.position
