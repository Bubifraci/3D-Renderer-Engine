import numpy as np

class LightSource:
    def __init__(self, strength, position):
        self.strength = strength
        self.position = np.array(position)