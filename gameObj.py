import numpy as np


class GameObject:

    def __init__(self, vertices, faces, startPosition, startRotation, startScale):
        self.vertices = np.array(vertices)
        self.faces = np.array(faces)
        self.position = np.array(startPosition)
        self.rotation = np.array(startRotation)
        self.scale = np.array(startScale)

    @staticmethod
    def importObj(filename, startPosition, startRotation, startScale):
        vertices = []
        faces = []

        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split()
                prefix = parts[0]

                if prefix == "v":
                    x, y, z = (
                        float(parts[1]),
                        float(parts[2]),
                        float(parts[3]),
                    )
                    vertices.append([x, y, z])

                elif prefix == "f":
                    face_indices = []
                    for p in parts[1:]:
                        idx = int(p.split("/")[0]) - 1
                        face_indices.append(idx)
                    faces.append(face_indices)

        return GameObject(vertices, faces, startPosition, startRotation, startScale)

    def getGlobalVertices(self):
            rad = np.deg2rad(self.rotation)
            rotMatrix = GameObject.getRotationMatrix(rad[0], rad[1], rad[2], scale=self.scale)
            return (self.vertices @ rotMatrix.T) + self.position

    @staticmethod
    def getRotationMatrix(r, p, y, scale=[1.0, 1.0, 1.0]):
        alpha = y
        beta = p
        gamma = r
        return np.array([
            [scale[0]*(np.cos(alpha) * np.cos(beta)), scale[0]*(np.cos(alpha) * np.sin(beta) * np.sin(gamma) - np.sin(alpha) * np.cos(gamma)), scale[0]*(np.cos(alpha) * np.sin(beta) * np.cos(gamma) + np.sin(alpha) * np.sin(gamma))],
            [scale[1]*(np.sin(alpha) * np.cos(beta)), scale[1]*(np.sin(alpha) * np.sin(beta) * np.sin(gamma) + np.cos(alpha) * np.cos(gamma)), scale[1]*(np.sin(alpha) * np.sin(beta) * np.cos(gamma) - np.cos(alpha) * np.sin(gamma))],
            [scale[2]*(-np.sin(beta)), scale[2]*(np.cos(beta) * np.sin(gamma)), scale[2]*(np.cos(beta) * np.cos(gamma))]
        ])