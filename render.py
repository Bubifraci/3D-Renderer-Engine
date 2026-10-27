import sys
import pygame
import numpy as np

from camera import Camera
from gameObj import GameObject


def renderObjects(objects, cam, width, height, screen):
    mvp = cam.getMVP()
    for gObject in objects:
        transformed_coordinates = []
        vertices = gObject.getGlobalVertices()

        for vertex in vertices:
            homVertex = np.array([vertex[0], vertex[1], vertex[2], 1.0])
            newVertex = mvp @ homVertex

            w = newVertex[3]
            if w > 0:
                normalizedVertex = np.array(
                    [newVertex[0] / w, newVertex[1] / w, newVertex[2] / w]
                )
                x_pix = width * (normalizedVertex[0] + 1) / 2.0
                y_pix = height * (1 - normalizedVertex[1]) / 2.0
                transformed_coordinates.append(np.array([x_pix, y_pix, w]))
            else:
                transformed_coordinates.append(np.array([0, 0, w]))

        faces_to_render = []

        for face in gObject.faces:
            if(len(face) == 3):
                w = 0
                vertices = [transformed_coordinates[face[0]], transformed_coordinates[face[1]], transformed_coordinates[face[2]]]
                newVertices = []

                isValid = True

                for vertex in vertices:
                    w += vertex[2]
                    if vertex[2] <= 0:
                        isValid = False
                        break
                    else:
                        newVertices.append(np.array([vertex[0], vertex[1]]))

                w /= 3

                if(isValid):
                    faces_to_render.append((w, newVertices))

        faces_to_render.sort(key=lambda x: x[0], reverse=True)

        for w, draw_vertices in faces_to_render:
            t = min(1.0, 1.0 - max(0, (w - cam.near)/(cam.far - cam.near)))
            pygame.draw.polygon(screen, (int(t * t * 255), int(t * t * 255), int(255 / (t * 2))), draw_vertices)

    

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
            current_cam.addPosition([1, 0, 0], velocity)
        if keys[pygame.K_s]:
            current_cam.addPosition([-1, 0, 0], velocity)
        if keys[pygame.K_a]:
            current_cam.addPosition([0, -1, 0], velocity)
        if keys[pygame.K_d]:
            current_cam.addPosition([0, 1, 0], velocity)

        
        screen.fill(BG_COLOR)

        renderObjects(present_objects, current_cam, SCREEN_WIDTH, SCREEN_HEIGHT, screen)

        pygame.display.flip() 

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()