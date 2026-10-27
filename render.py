import sys
import pygame
import numpy as np

from camera import Camera
from gameObj import GameObject


def renderObjects(objects, cam, width, height, screen):
    mvp = cam.getMVP()
    for gObject in objects:
        vertices = gObject.getGlobalVertices()

        vertexMatrix = np.array(vertices)

        ones = np.ones(len(vertexMatrix))

        vertexMatrix = np.column_stack((vertexMatrix, ones)).T

        transformedMatrix = mvp @ vertexMatrix

        w_vals = transformedMatrix[3]

        transformedMatrix /= w_vals

        x_vals = width * (transformedMatrix[0] + 1) / 2.0
        y_vals = height * (1 - transformedMatrix[1]) / 2.0

        renderCoordinates = np.array([x_vals, y_vals, w_vals]).T

        # Faces
        faces = np.array(gObject.faces)

        polygons = renderCoordinates[faces]

        w_polygons = polygons[:, :, 2]

        valid_mask = (w_polygons > 0).all(axis=1)

        w_polyongs = polygons[valid_mask]

        mean_w = w_polyongs[:, :, 2].mean(axis=1)

        sort_indices = np.argsort(mean_w)[::-1]

        sorted_triangles = w_polyongs[sort_indices]

        for pol in sorted_triangles:
            pts = pol[:, :2]
            w = pol[:, 2].mean()
            t = min(1.0, 1.0 - max(0, (w - cam.near)/(cam.far - cam.near)))
            r_g = int(t * t * 255)
            b = min(255, int(255 / (max(0.01, t) * 2)))
            pygame.draw.polygon(screen, (r_g, r_g, b), pts)

    

def main():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
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

    present_objects = [GameObject.importObj("objects/tea.obj", [20, 0, 0])]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        dx, dy = pygame.mouse.get_rel()

        current_cam.addOrientation(dy * sensitivity, dx * sensitivity)

        if keys[pygame.K_w]:
            current_cam.addPosition([-1, 0, 0], velocity)
        if keys[pygame.K_s]:
            current_cam.addPosition([1, 0, 0], velocity)
        if keys[pygame.K_a]:
            current_cam.addPosition([0, 1, 0], velocity)
        if keys[pygame.K_d]:
            current_cam.addPosition([0, -1, 0], velocity)

        
        screen.fill(BG_COLOR)

        renderObjects(present_objects, current_cam, SCREEN_WIDTH, SCREEN_HEIGHT, screen)

        pygame.display.flip() 

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()