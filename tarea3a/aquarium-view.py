import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import json
import sys
import matplotlib.pyplot as mpl
from random import *

import transformations as tr
import easy_shaders as es
import basic_shapes as bs
import scene_graph as sg

with open('view-setup.json') as file:
    data = json.load(file)
    for parameter in data['parameters']:
        # Solution
        FILENAME = parameter['filename']
        # Ideal temperatures
        T_A = parameter['t_a']
        T_B = parameter['t_b']
        T_C = parameter['t_c']
        # Number of fishes for each type
        N_A = parameter['n_a']
        N_B = parameter['n_b']
        N_C = parameter['n_c']

# Problem setup
FILENAME = 'temperatures.npy'
T_A = 15
T_B = 10
T_C = 25
N_A = 5
N_B = 3
N_C = 7

def fast_marching_cube(X, Y, Z, temperatures, t_value):
    dims = X.shape[0] - 1, X.shape[1] - 1, X.shape[2] - 1
    voxels = np.zeros(shape = dims, dtype = bool)
    for i in range(1, X.shape[0] - 1):
        for j in range(1, X.shape[1] - 1):
            for k in range(1, X.shape[2] - 1):
                t_min = temperatures[i - 1:i + 1, j - 1:j + 1, k - 1:k + 1].min()
                t_max = temperatures[i - 1:i + 1, j - 1:j + 1, k - 1:k + 1].max()
                if t_min >= t_value - 2 and t_max <= t_value + 2:
                    voxels[i, j, k] = True
                else:
                    voxels[i, j, k] = False
    return voxels

def createColorCube2(i, j, k, X, Y, Z, r, g, b):
    l_x = X[i, j, k]
    r_x = l_x + 1
    b_y = Y[i, j, k]
    f_y = b_y + 1
    b_z = Z[i, j, k]
    t_z = b_z + 1
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y, t_z, r, g, b,
        r_x, b_y, t_z, r, g, b,
        r_x, f_y, t_z, r, g, b,
        l_x, f_y, t_z, r, g, b,
    # Z-: number 6
        l_x, b_y, b_z, r, g, b,
        r_x, b_y, b_z, r, g, b,
        r_x, f_y, b_z, r, g, b,
        l_x, f_y, b_z, r, g, b,
    # X+: number 5
         r_x, b_y, b_z, r, g, b,
         r_x, f_y, b_z, r, g, b,
         r_x, f_y, t_z, r, g, b,
         r_x, b_y, t_z, r, g, b,
    # X-: number 2
        l_x, b_y, b_z, r, g, b,
        l_x, f_y, b_z, r, g, b,
        l_x, f_y, t_z, r, g, b,
        l_x, b_y, t_z, r, g, b,
    # Y+: number 4
        l_x, f_y, b_z, r, g, b,
        r_x, f_y, b_z, r, g, b,
        r_x, f_y, t_z, r, g, b,
        l_x, f_y, t_z, r, g, b,
    # Y-: number 3
        l_x, b_y, b_z, r, g, b,
        r_x, b_y, b_z, r, g, b,
        r_x, b_y, t_z, r, g, b,
        l_x, b_y, t_z, r, g, b,
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return bs.Shape(vertices, indices)

def merge(destinationShape, strideSize, sourceShape):
    # Current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset / strideSize) + index for index in sourceShape.indices]

class Controller:
    def __init__(self):
        self.a = True
        self.b = False
        self.c = False

# We will use the global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):
    global controller
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_A:
        controller.a = True
        controller.b = False
        controller.c = False
    elif key == glfw.KEY_B:
        controller.a = False
        controller.b = True
        controller.c = False
    elif key == glfw.KEY_C:
        controller.a = False
        controller.b = False
        controller.c = True
    elif key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

def createFish(r, g, b):
    gpu_body = es.toGPUShape(bs.createColorCube(r, g, b))
    gpu_tail = es.toGPUShape(bs.createColorCube(r, g, b))

    # Body of the fish
    body = sg.SceneGraphNode('body')
    body.transform = tr.matmul([tr.uniformScale(2), tr.scale(0.6, 0.2, 0.3)])
    body.childs += [gpu_body]

    # Tail of the fish
    tail = sg.SceneGraphNode('tail')
    tail.transform = tr.matmul([tr.uniformScale(2), tr.translate(-0.4, 0, 0), tr.scale(0.2, 0.05, 0.2)])
    tail.childs += [gpu_tail]

    tailRotation = sg.SceneGraphNode('tailRotation')
    tailRotation.childs += [tail]

    # Creating the fish
    fish = sg.SceneGraphNode('fish')
    fish.childs += [body]
    fish.childs += [tailRotation]

    return fish

if __name__ == '__main__':
    # Initialize GLFW
    if not glfw.init():
        sys.exit()
    width = 600
    height = 600
    window = glfw.create_window(width, height, 'Aquarium-view', None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)

    # Connecting the callback function on_key to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # As we work in 3D, we need to check which part is in front, and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))

    # Load temperatures and grid
    load_voxels = np.load(FILENAME)
    X = np.arange(0, load_voxels.shape[0], 1, dtype=int)
    Y = np.arange(0, load_voxels.shape[1], 1, dtype=int)
    Z = np.arange(0, load_voxels.shape[2], 1, dtype=int)
    X, Y, Z = np.meshgrid(Y, X, Z)

    voxelsA = fast_marching_cube(X, Y, Z, load_voxels, T_A)
    voxelsB = fast_marching_cube(X, Y, Z, load_voxels, T_B)
    voxelsC = fast_marching_cube(X, Y, Z, load_voxels, T_C)

    # Creating shapes on GPU memory
    isosurfaceA = bs.Shape([], [])
    pointsA = []
    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            for k in range(X.shape[2] - 1):
                if voxelsA[i, j, k]:
                    pointsA.append((i, j, k))
                    temp_shape = createColorCube2(i, j, k, X, Y, Z, 0.0, 0.5, 0.0)
                    merge(isosurfaceA, 6, temp_shape)
    copyPointsA = pointsA.copy()

    isosurfaceB = bs.Shape([], [])
    pointsB = []
    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            for k in range(X.shape[2] - 1):
                if voxelsB[i, j, k]:
                    pointsB.append((i, j, k))
                    temp_shape = createColorCube2(i, j, k, X, Y, Z, 0.0, 0.0, 0.5)
                    merge(isosurfaceB, 6, temp_shape)
    copyPointsB = pointsB.copy()

    isosurfaceC = bs.Shape([], [])
    pointsC = []
    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            for k in range(X.shape[2] - 1):
                if voxelsC[i, j, k]:
                    pointsC.append((i, j, k))
                    temp_shape = createColorCube2(i, j, k, X, Y, Z, 0.5, 0.0, 0.0)
                    merge(isosurfaceC, 6, temp_shape)
    copyPointsC = pointsC.copy()

    aquariumBorder = bs.Shape([], [])
    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            for k in range(X.shape[2] - 1):
                if ((i == 0 or i == X.shape[0] - 2) and (
                        j == 0 or j == X.shape[1] - 2 or k == 0 or k == X.shape[2] - 2)) or (
                        (j == 0 or j == X.shape[1] - 2) and (
                        i == 0 or i == X.shape[0] - 2 or k == 0 or k == X.shape[2] - 2)) or (
                        (j == 0 or j == X.shape[1] - 2 or i == 0 or i == X.shape[0] - 2) and (
                        k == 0 or k == X.shape[2] - 2)):
                    temp_shape = createColorCube2(i, j, k, X, Y, Z, 1.0, 1.0, 1.0)
                    merge(aquariumBorder, 6, temp_shape)

    gpu_surfaceA = es.toGPUShape(isosurfaceA)
    surfaceA = sg.SceneGraphNode('surfaceA')
    surfaceA.transform = tr.translate(-20, -10, -10)
    surfaceA.childs += [gpu_surfaceA]
    scaledSurfaceA = sg.SceneGraphNode('scaledSurfaceA')
    scaledSurfaceA.transform = tr.uniformScale(0.5)
    scaledSurfaceA.childs += [surfaceA]

    gpu_surfaceB = es.toGPUShape(isosurfaceB)
    surfaceB = sg.SceneGraphNode('surfaceB')
    surfaceB.transform = tr.translate(-20, -10, -10)
    surfaceB.childs += [gpu_surfaceB]
    scaledSurfaceB = sg.SceneGraphNode('scaledSurfaceB')
    scaledSurfaceB.transform = tr.uniformScale(0.5)
    scaledSurfaceB.childs += [surfaceB]

    gpu_surfaceC = es.toGPUShape(isosurfaceC)
    surfaceC = sg.SceneGraphNode('surfaceC')
    surfaceC.transform = tr.translate(-20, -10, -10)
    surfaceC.childs += [gpu_surfaceC]
    scaledSurfaceC = sg.SceneGraphNode('scaledSurfaceC')
    scaledSurfaceC.transform = tr.uniformScale(0.5)
    scaledSurfaceC.childs += [surfaceC]

    border = es.toGPUShape(aquariumBorder)
    borderAquarium = sg.SceneGraphNode('borderAquarium')
    borderAquarium.transform = tr.translate(-19, -9, -9)
    borderAquarium.childs += [border]
    scaledBorder = sg.SceneGraphNode('scaledBorder')
    scaledBorder.transform = tr.uniformScale(0.5)
    scaledBorder.childs += [borderAquarium]

    fishesA = []
    fishesB = []
    fishesC = []

    nas = []
    nbs = []
    ncs = []

    randomRotationA = []
    randomRotationB = []
    randomRotationC = []

    # We create random numbers for each zone
    # Each fish will be in that position
    for i in range(N_A):
        na = randint(0, len(pointsA) - 1)
        ra = uniform(0, np.pi)
        fishesA.append(createFish(1.0, 0.0, 0.0))
        nas.append(na)
        randomRotationA.append(ra)
        pointsA.pop(na)
    pointsA = copyPointsA
    for i in range(N_B):
        nb = randint(0, len(pointsB) - 1)
        rb = uniform(0, np.pi)
        fishesB.append(createFish(0.0, 1.0, 0.0))
        nbs.append(nb)
        randomRotationB.append(rb)
        pointsB.pop(nb)
    pointsB = copyPointsB
    for i in range(N_C):
        nc = randint(0, len(pointsC) - 1)
        rc = uniform(0, np.pi)
        fishesC.append(createFish(0.0, 0.0, 1.0))
        ncs.append(nc)
        randomRotationC.append(rc)
        pointsC.pop(nc)
    pointsC = copyPointsC

    t0 = glfw.get_time()
    camera_theta = np.pi / 4
    rotation = 0
    zoom = 0.5

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            camera_theta -= 2 * dt
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            camera_theta += 2 * dt

        # Setting up the projection transform
        projection = tr.perspective(60, float(width) / float(height), 0.1, 100)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'projection'), 1, GL_TRUE, projection)

        # Setting up the view transform
        camX = 20 * np.sin(camera_theta)
        camY = 20 * np.cos(camera_theta)

        viewPos = np.array([camX, camY, 10])
        view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'view'), 1, GL_TRUE, view)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Zoom
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            if zoom < 1.7:
                zoom += 0.05
        elif glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            if zoom > 0.4:
                zoom -= 0.05

        # Zoom transformations
        scaledSurfaceA.transform = tr.uniformScale(zoom)
        scaledSurfaceB.transform = tr.uniformScale(zoom)
        scaledSurfaceC.transform = tr.uniformScale(zoom)
        scaledBorder.transform = tr.uniformScale(zoom)

        # Fish transformations
        for i in range(len(fishesA)):
            fishesA[i].transform = tr.matmul([tr.uniformScale(zoom),
                                              tr.translate(pointsA[nas[i]][1] - 20, pointsA[nas[i]][0] - 10, pointsA[nas[i]][2] - 10),
                                              tr.rotationZ(randomRotationA[i])])
            tailRotationA = sg.findNode(fishesA[i], 'tailRotation')
            tailRotationA.transform = tr.rotationZ(rotation)

        for i in range(len(fishesB)):
            fishesB[i].transform = tr.matmul([tr.uniformScale(zoom),
                                              tr.translate(pointsB[nbs[i]][1] - 20, pointsB[nbs[i]][0] - 10, pointsB[nbs[i]][2] - 10),
                                              tr.rotationZ(randomRotationB[i])])
            tailRotationB = sg.findNode(fishesB[i], 'tailRotation')
            tailRotationB.transform = tr.rotationZ(rotation)

        for i in range(len(fishesC)):
            fishesC[i].transform = tr.matmul([tr.uniformScale(zoom),
                                              tr.translate(pointsC[ncs[i]][1] - 20, pointsC[ncs[i]][0] - 10, pointsC[ncs[i]][2] - 10),
                                              tr.rotationZ(randomRotationC[i])])
            tailRotationC = sg.findNode(fishesC[i], 'tailRotation')
            tailRotationC.transform = tr.rotationZ(rotation)

        # dty determines the movement of the tails
        dty = np.sin(5 * t0)
        if dty > 0:
            rotation += dt
            if dty > 0.99:  # This is for preventing errors
                rotation = 0
        else:
            rotation -= dt

        # Drawing shapes with different model transformations
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'model'), 1, GL_TRUE, tr.identity())
        pipeline.drawShape(gpuAxis, GL_LINES)

        if controller.a:
            sg.drawSceneGraphNode(scaledSurfaceA, pipeline, 'model')
        elif controller.b:
            sg.drawSceneGraphNode(scaledSurfaceB, pipeline, 'model')
        elif controller.c:
            sg.drawSceneGraphNode(scaledSurfaceC, pipeline, 'model')
        sg.drawSceneGraphNode(scaledBorder, pipeline, 'model')

        for fishA in fishesA:
            sg.drawSceneGraphNode(fishA, pipeline, 'model')
        for fishB in fishesB:
            sg.drawSceneGraphNode(fishB, pipeline, 'model')
        for fishC in fishesC:
            sg.drawSceneGraphNode(fishC, pipeline, 'model')

        # Once the drawing is rendered, buffers are swapped so an uncomplete drawing is never seen
        glfw.swap_buffers(window)

    glfw.terminate()