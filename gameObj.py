import numpy as np


class GameObject:

    def __init__(self, vertices, faces, startPosition):
        self.vertices = np.array(vertices)
        self.faces = np.array(faces)
        self.startPosition = np.array(startPosition)

    @staticmethod
    def importObj(filename, startPosition):
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

        return GameObject(vertices, faces, startPosition)

    def getGlobalVertices(self):
        transformed_vertices = []
        for vertex in self.vertices:
            transformed_vertices.append(np.add(vertex, self.startPosition))
        return transformed_vertices