import numpy as np

class Camera:
    def __init__(self, fov, aspect_ratio, startPosition, near, far):
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.position = np.array(startPosition)
        self.near = near
        self.far = far

        self.pitch = 0
        self.yaw = 0
        self.globalUp = np.array([0, 0, 1])


    #In deg!
    def getOrientation(self):
        pitch = np.deg2rad(self.pitch)
        yaw = np.deg2rad(self.yaw)

        dX = np.cos(pitch) * np.cos(yaw)
        dY = np.cos(pitch) * np.sin(yaw)
        dZ = np.sin(pitch)

        return np.array([dX, dY, dZ])

    def addOrientation(self, dPitch, dYaw):
        if(self.pitch + dPitch < 90 and self.pitch + dPitch > -90):
            self.pitch = self.pitch + dPitch
        while((self.yaw + dYaw) >= 360.0):
            dYaw -= 360
        while((self.yaw + dYaw) <= -360.0):
            dYaw += 360
        self.yaw = self.yaw + dYaw
        

    def addPosition(self, dPos, velocity):
        dPos = np.array(dPos, dtype=float)
        norm = np.linalg.norm(dPos)
        if norm > 0:
            dPos = (dPos / norm) * velocity

            f = self.getOrientation()

            f = np.array([f[0], f[1], 0.0])

            f /= np.linalg.norm(f)

            gO = self.globalUp / np.linalg.norm(self.globalUp)
            
            r = np.cross(gO, f)

            if(np.linalg.norm(r) > 0):
                r /= np.linalg.norm(r)
        
            u = np.cross(r, f)
        
            u /= np.linalg.norm(u)

            self.position = self.position + dPos[0] * f + dPos[1] * r + dPos[2] * u

    def setPosition(self, pos):
        pos = np.array(pos)
        self.position = pos

    def getViewMatrix(self):
        f = self.getOrientation() / np.linalg.norm(self.getOrientation())
        gO = self.globalUp / np.linalg.norm(self.globalUp)

        r = np.cross(gO, f)

        r /= np.linalg.norm(r)

        u = np.cross(r, f)

        u /= np.linalg.norm(u)

        pos = self.position

        viewMatrix = np.array([
            [r[0], r[1], r[2], -np.dot(r, pos)],
            [u[0], u[1], u[2], -np.dot(u, pos)],
            [-f[0], -f[1], -f[2], np.dot(f, pos)],
            [0, 0, 0, 1]
        ]
        )

        return viewMatrix


    def getProjectionMatrix(self):
        fov = np.deg2rad(self.fov)

        scale = 1/(np.tan(fov/2))

        far = self.far
        near = self.near

        projectionMatrix = np.array([
            [scale/self.aspect_ratio, 0, 0, 0],
            [0, scale, 0, 0],
            [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
            [0, 0, -1.0, 0]
        ])

        return projectionMatrix

    def getMVP(self):
        return np.dot(self.getProjectionMatrix(), self.getViewMatrix())