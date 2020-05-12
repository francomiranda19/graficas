import glfw
from OpenGL.GL import *
import numpy as np
import csv
import sys

import scene_graph as sg
import basic_shapes as bs
import easy_shaders as es
import transformations as tr
import lighting_shaders as ls
from curves import *
from bird import *

# A class to store the application control
class Controller:
    def __init__(self):
        self.mousePos = (0.0, 0.0)

controller = Controller()

def on_key(window, key, scancode, action, mods):
    global controller
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            sys.exit()

def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x, y)

def createCurve(filename, N):
    listaPuntos = []
    listaCurvas = []
    with open(filename) as file:
        reader = csv.reader(file)
        for line in reader:
            line = np.array([[float(x) for x in line]]).T
            listaPuntos.append(line)
    for i in range(len(listaPuntos) - 3):
        GMcr = catmullRomMatrix(listaPuntos[i], listaPuntos[i + 1], listaPuntos[i + 2], listaPuntos[i + 3])
        catmullRomCurve = evalCurve(GMcr, N)
        listaCurvas.append(catmullRomCurve)
    curva = []
    for i in range(len(listaCurvas)):
        for j in range(len(listaCurvas[i])):
            curva.append(listaCurvas[i][j])
    return curva

def curvesQuantity(filename):
    with open(filename) as file:
        reader = csv.reader(file)
        i = 0
        for line in reader:
            i += 1
    return i - 3

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Bird Herd", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting callback functions to handle keyboard and mouse events
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    # Lighting program without textures
    phongPipeline = ls.SimplePhongShaderProgram()

    # Lighting program with textures
    phongTexturePipeline = ls.SimpleTexturePhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # As we work in 3D, we need to check which part is in front, and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creating shapes on GPU memory
    # Landscape
    gpuHills = es.toGPUShape(bs.createTextureNormalsCube('hills.png'), GL_REPEAT, GL_LINEAR)
    gpuGrass = es.toGPUShape(bs.createTextureNormalsCube('grass.jpg'), GL_REPEAT, GL_LINEAR)
    gpuSky = es.toGPUShape(bs.createTextureNormalsCube('sky.jpg'), GL_REPEAT, GL_LINEAR)

    # Transformations of the landscape
    leftHills = tr.matmul([tr.translate(25, -25, 0), tr.scale(0.1, 100, 20)])
    frontHills = tr.matmul([tr.translate(0, -50, 0), tr.rotationZ(np.pi / 2), tr.scale(0.1, 100, 20)])
    rightHills = tr.matmul([tr.translate(-25, -25, 0), tr.scale(0.1, 100, 20)])
    grass = tr.matmul([tr.translate(0, -30, -10), tr.scale(50, 100, 0.1)])
    sky = tr.matmul([tr.translate(0, -30, 10), tr.scale(50, 100, 0.1)])

    # Birds
    bird = Bird()
    birdNode1 = bird.get_bird()
    birdNode2 = bird.get_bird()
    birdNode3 = bird.get_bird()
    birdNode4 = bird.get_bird()
    birdNode5 = bird.get_bird()
    birdNodes = [birdNode1, birdNode2, birdNode3, birdNode4, birdNode5]

    # The user determines which path the birds will follow
    path = sys.argv[1]; N = 100
    C = createCurve(path, N)
    c = curvesQuantity(path)

    # This determines how the wings rotate
    rotation = 0

    # This is going to be used for the movement of the birds
    i = 0; j = 0; k = 0; l = 0; m = 0

    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Getting the mouse location in openGL coordinates
        mousePosX = 2 * (controller.mousePos[0] - width / 2) / width
        mousePosY = 2 * (height / 2 - controller.mousePos[1]) / height

        # Setting up the projection transform
        projection = tr.perspective(45, float(width) / float(height), 0.1, 100)

        # Setting up the view transform
        atX = -6 * mousePosX
        atZ = 5 * mousePosY

        atPos = np.array([atX, 0, atZ])

        view = tr.lookAt(
            np.array([0, 5, 2]),
            atPos,
            np.array([0, 0, 1])
        )

        # Setting up the model transform
        model = tr.identity()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # The landscape is drawn with texture lighting
        glUseProgram(phongTexturePipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "Ka"), 0.8, 0.8, 0.8)
        glUniform3f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        glUniform3f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "lightPosition"), 5, -3, 5)
        glUniform3f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "viewPosition"), 0, 5, 2)
        glUniform1ui(glGetUniformLocation(phongTexturePipeline.shaderProgram, "shininess"), 1000)

        glUniform1f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongTexturePipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(phongTexturePipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongTexturePipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Drawing the landscape
        # Hills
        glUniformMatrix4fv(glGetUniformLocation(phongTexturePipeline.shaderProgram, "model"), 1, GL_TRUE, leftHills)
        phongTexturePipeline.drawShape(gpuHills)
        glUniformMatrix4fv(glGetUniformLocation(phongTexturePipeline.shaderProgram, "model"), 1, GL_TRUE, frontHills)
        phongTexturePipeline.drawShape(gpuHills)
        glUniformMatrix4fv(glGetUniformLocation(phongTexturePipeline.shaderProgram, "model"), 1, GL_TRUE, rightHills)
        phongTexturePipeline.drawShape(gpuHills)
        # Grass
        glUniformMatrix4fv(glGetUniformLocation(phongTexturePipeline.shaderProgram, "model"), 1, GL_TRUE, grass)
        phongTexturePipeline.drawShape(gpuGrass)
        # Sky
        glUniformMatrix4fv(glGetUniformLocation(phongTexturePipeline.shaderProgram, "model"), 1, GL_TRUE, sky)
        phongTexturePipeline.drawShape(gpuSky)

        # The birds are drawn with lighting effects
        glUseProgram(phongPipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPosition"), 5, -3, 5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), 0, 5, 2)
        glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 1000)

        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        # Movement of the wings
        for birdNode in birdNodes:
            # Right wing
            upperRightRotationNode = sg.findNode(birdNode, "upperRightRotation")
            upperRightRotationNode.transform = tr.rotationX(-rotation)
            foreRightRotationNode = sg.findNode(birdNode, "foreRightRotation")
            foreRightRotationNode.transform = tr.matmul(
                [tr.translate(0, -0.58, 0), tr.rotationX(-4 * rotation), tr.translate(0, 0.58, 0)])
            # Left wing
            upperLeftRotationNode = sg.findNode(birdNode, "upperLeftRotation")
            upperLeftRotationNode.transform = tr.rotationX(rotation)
            foreLeftRotationNode = sg.findNode(birdNode, "foreLeftRotation")
            foreLeftRotationNode.transform = tr.matmul(
                [tr.translate(0, 0.58, 0), tr.rotationX(4 * rotation), tr.translate(0, -0.58, 0)])
            # Head and Neck
            headAndNeckRotationNode = sg.findNode(birdNode, "headAndNeckRotation")
            headAndNeckRotationNode.transform = tr.rotationY(0.5 * rotation)
            # Back wing
            backWingRotationNode = sg.findNode(birdNode, "backWingRotation")
            backWingRotationNode.transform = tr.rotationY(-0.2 * rotation)

        # dty determines the movement of the wings
        dty = np.sin(5 * t0)
        if dty > 0:
            rotation += dt
            if dty > 0.99:  # This is for preventing errors
                rotation = 0
        else:
            rotation -= dt

        # Drawing the birds
        if t0 > 3:
            if i < N * c - 2:
                # Calculating the derivative for the rotation of the bird
                x1 = C[i][0]; y1 = C[i][1]; z1 = C[i][2]
                derivative1 = (C[i + 2][1] - y1) / (C[i + 2][0] - x1)
                angle1 = np.arctan(derivative1)
                # Transformation of the bird
                birdNode1.transform = tr.matmul([tr.translate(x1, y1, z1), tr.rotationZ(angle1), tr.uniformScale(0.2)])
                sg.drawSceneGraphNode(birdNode1, phongPipeline, "model")
                i += 1
            elif i == N * c - 2:
                i = 0

        if t0 > 4:
            if j < N * c - 2:
                # Calculating the derivative for the rotation of the bird
                x2 = C[j][0]; y2 = C[j][1]; z2 = C[j][2]
                derivative2 = (C[j + 2][1] - y2) / (C[j + 2][0] - x2)
                angle2 = np.arctan(derivative2)
                # Transformation of the bird
                birdNode2.transform = tr.matmul([tr.translate(x2, y2, z2), tr.rotationZ(angle2), tr.uniformScale(0.2)])
                sg.drawSceneGraphNode(birdNode2, phongPipeline, "model")
                j += 1
            elif j == N * c - 2:
                j = 0

        if t0 > 5:
            if k < N * c - 2:
                # Calculating the derivative for the rotation of the bird
                x3 = C[k][0]; y3 = C[k][1]; z3 = C[k][2]
                derivative3 = (C[k + 2][1] - y3) / (C[k + 2][0] - x3)
                angle3 = np.arctan(derivative3)
                # Transformation of the bird
                birdNode3.transform = tr.matmul([tr.translate(x3, y3, z3), tr.rotationZ(angle3), tr.uniformScale(0.2)])
                sg.drawSceneGraphNode(birdNode3, phongPipeline, "model")
                k += 1
            elif k == N * c - 2:
                k = 0

        if t0 > 6:
            if l < N * c - 2:
                # Calculating the derivative for the rotation of the bird
                x4 = C[l][0]; y4 = C[l][1]; z4 = C[l][2]
                derivative4 = (C[l + 2][1] - y4) / (C[l + 2][0] - x4)
                angle4 = np.arctan(derivative4)
                # Transformation of the bird
                birdNode4.transform = tr.matmul([tr.translate(x4, y4, z4), tr.rotationZ(angle4), tr.uniformScale(0.2)])
                sg.drawSceneGraphNode(birdNode4, phongPipeline, "model")
                l += 1
            elif l == N * c - 2:
                l = 0

        if t0 > 7:
            if m < N * c - 2:
                # Calculating the derivative for the rotation of the bird
                x5 = C[m][0]; y5 = C[m][1]; z5 = C[m][2]
                derivative5 = (C[m + 2][1] - y5) / (C[m + 2][0] - x5)
                angle5 = np.arctan(derivative5)
                # Transformation of the bird
                birdNode5.transform = tr.matmul([tr.translate(x5, y5, z5), tr.rotationZ(angle5), tr.uniformScale(0.2)])
                sg.drawSceneGraphNode(birdNode5, phongPipeline, "model")
                m += 1
            elif m == N * c - 2:
                m = 0

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()