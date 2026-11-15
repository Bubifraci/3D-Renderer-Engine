# 3D-Renderer-Engine

A CPU-based 3D software renderer and basic rigid-body physics engine written in Python using NumPy and Pygame. Built from scratch to explore 3D graphics fundamentals (transformation matrices, perspective projection, rasterization) without relying on OpenGL or other graphics APIs.

## Features

- **Software Rendering Pipeline:** Model-View-Projection (MVP) transformations, near-plane clipping, and perspective division vectorized with NumPy.
- **Backface Culling & Depth Sorting:** 2D cross-product backface culling and painter's algorithm depth sorting for polygon occlusion.
- **Flat Shading:** Per-face surface normal calculation and diffuse lighting from multiple light sources.
- **`.obj` Mesh Loader:** Basic Wavefront `.obj` parser supporting custom scaling, Euler rotations, and world positioning.
- **Rigid-Body Physics:** Simple Newtonian physics integration supporting gravity, forces, and impulses (`rigidBody.py`).
- **First-Person Camera:** Free-look camera with mouse yaw/pitch rotation and `WASD` movement.

## Project Structure

- `render.py` – Main loop, scene initialization, and rendering pipeline
- `camera.py` – View/projection matrices and camera movement
- `gameObj.py` – Mesh representation, rotation matrices, and `.obj` file loader
- `rigidBody.py` – Velocity and position integration for rigid bodies
- `lightsource.py` – Light source data structure
- `objects/` – `.obj` mesh files (e.g., `cube.obj`)

## Controls

- `W` / `A` / `S` / `D` – Move camera
- `Mouse` – Look around (Yaw / Pitch)
- `Alt + F4` – Quit

## Setup & Usage

Requires Python 3.8+, `numpy`, and `pygame`.

```bash
git clone https://github.com/Bubifraci/3D-Renderer-Engine.git
cd 3D-Renderer-Engine
pip install numpy pygame
python render.py
