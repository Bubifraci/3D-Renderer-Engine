import sys
import pygame
import numpy as np

from camera import Camera
from gameObj import GameObject
from lightsource import LightSource


def renderObjects(objects, cam, width, height, screen, lightsources):
    globalBrightness = []
    globalTriangles = []
    mvp = cam.getMVP()
    for gObject in objects:
        vertices = gObject.getGlobalVertices()
        faces = np.array(gObject.faces)

        vertexMatrix = np.array(vertices)

        #Calculate brightness
        triangles_3d = vertexMatrix[faces]
        v0 = triangles_3d[:, 0, :]
        v1 = triangles_3d[:, 1, :]
        v2 = triangles_3d[:, 2, :]

        A = v1 - v0
        B = v2 - v0

        normals = np.cross(A, B)
        norm_lengths = np.linalg.norm(normals, axis=1, keepdims=True)
        norm_lengths[norm_lengths == 0] = 1.0 
        normals /= norm_lengths

        brightness = np.zeros(len(faces))

        for light in lightsources:
            dir = np.array(light.position, dtype=float)
            light_norm = np.linalg.norm(dir)
            if light_norm > 0:
                dir /= light_norm
            brightness += np.maximum(0.2, np.dot(normals, dir))
            


        ones = np.ones(len(vertexMatrix))

        vertexMatrix = np.column_stack((vertexMatrix, ones)).T

        transformedMatrix = (mvp @ vertexMatrix).T
        clip_polygons = transformedMatrix[faces]

        w_clip = clip_polygons[:, :, 3]
        valid_mask = (w_clip > cam.near).all(axis=1)

        valid_clip_polygons = clip_polygons[valid_mask]
        valid_brightness = brightness[valid_mask]

        w_valid = valid_clip_polygons[:, :, 3]
        x_vals = width * (valid_clip_polygons[:, :, 0] / w_valid + 1) / 2.0
        y_vals = height * (1 - valid_clip_polygons[:, :, 1] / w_valid) / 2.0

        renderCoordinates = np.stack([x_vals, y_vals, w_valid], axis=2)

        # Faces
        p0 = renderCoordinates[:, 0, :2]
        p1 = renderCoordinates[:, 1, :2]
        p2 = renderCoordinates[:, 2, :2]

        cross_2d = (p1[:, 0] - p0[:, 0]) * (p2[:, 1] - p0[:, 1]) - (p1[:, 1] - p0[:, 1]) * (p2[:, 0] - p0[:, 0])

        front_mask = cross_2d < 0

        front_polygons = renderCoordinates[front_mask]
        front_brightness = valid_brightness[front_mask]

        if len(front_polygons) > 0:
            globalTriangles.append(front_polygons)
            globalBrightness.append(front_brightness)

    if not globalTriangles:
            return
    all_triangles = np.concatenate(globalTriangles, axis=0)
    all_brightness = np.concatenate(globalBrightness, axis=0)

    mean_w = all_triangles[:, :, 2].mean(axis=1)
    sort_indices = np.argsort(mean_w)[::-1]

    sorted_triangles = all_triangles[sort_indices]
    sorted_brightness = all_brightness[sort_indices]

    i = 0
    for pol, bright in zip(sorted_triangles, sorted_brightness):
        pts = pol[:, :2]
        color_val = int(np.clip(255 * bright, 0, 255))
        pygame.draw.polygon(screen, (color_val, color_val, color_val), pts)
        i += 1

    

def main():
    pygame.init()

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 920
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("3D Renderer")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True) 

    velocity = 1
    sensitivity = 0.1

    clock = pygame.time.Clock()
    FPS = 60

    BG_COLOR = (30, 30, 30)

    running = True

    current_cam = Camera(60, SCREEN_WIDTH/SCREEN_HEIGHT, [0, 0, 0], 0.1, 50.0)

    present_objects = generateRandomObjects(200, 1.0, 100, filename="cube")

    present_lights = [LightSource(0.9, [0, 15, 10]), LightSource(0.9, [0, -15, -10]), LightSource(0.9, [23, -14, -30])]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        dx, dy = pygame.mouse.get_rel()

        current_cam.addOrientation(dy * sensitivity, dx * sensitivity)

        if keys[pygame.K_w]:
            current_cam.addPosition([1, 0, 0], velocity)
        if keys[pygame.K_s]:
            current_cam.addPosition([-1, 0, 0], velocity)
        if keys[pygame.K_a]:
            current_cam.addPosition([0, -1, 0], velocity)
        if keys[pygame.K_d]:
            current_cam.addPosition([0, 1, 0], velocity)

        
        screen.fill(BG_COLOR)

        renderObjects(present_objects, current_cam, SCREEN_WIDTH, SCREEN_HEIGHT, screen, present_lights)

        pygame.display.flip() 

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def generateRandomObjects(amount, scale=1.0, max_dist=100.0, filename="cube"):
    objects = []
    positions = []
    
    for _ in range(amount):
        max_attempts = 1000
        for _ in range(max_attempts):
            x = np.random.uniform(-max_dist / 2, max_dist / 2)
            y = np.random.uniform(-max_dist / 2, max_dist / 2)
            z = np.random.uniform(-max_dist / 2, max_dist / 2)
            coordinate = np.array([x, y, z])
            if all(np.linalg.norm(coordinate - oldCoord) > scale * 2 for oldCoord in positions):
                positions.append(coordinate)
                objects.append(
                    GameObject.importObj(
                        "objects/"+filename+".obj", [x, y, z], [0, 0, 0], [scale, scale, scale]
                    )
                )
                break

    return objects

            


if __name__ == "__main__":
    main()