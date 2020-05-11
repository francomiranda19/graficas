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

    # Assembling the shader program
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # As we work in 3D, we need to check which part is in front, and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    # Landscape
    gpuHills = es.toGPUShape(bs.createTextureNormalsCube('hills.png'), GL_REPEAT, GL_LINEAR)
    gpuGrass = es.toGPUShape(bs.createTextureNormalsCube('grass.jpg'), GL_REPEAT, GL_LINEAR)
    gpuSky = es.toGPUShape(bs.createTextureNormalsCube('sky.jpg'), GL_REPEAT, GL_LINEAR)

    bird = Bird()
    birdNode = bird.get_bird()

    t0 = glfw.get_time()

    # This determines how the wings rotate
    rotation = 0

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
        atX = -4 * mousePosX
        atZ = 3 * mousePosY

        atPos = np.array([atX, 0, atZ])

        view = tr.lookAt(
            np.array([0, 5, 2]),
            atPos,
            np.array([0, 0, 1])
        )

        # Setting up the model transform
        model = tr.rotationX(np.pi)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Movement of the wings
        # Right wing
        upperRightRotationNode = sg.findNode(birdNode, "upperRightRotation")
        upperRightRotationNode.transform = tr.rotationX(-0.5 * rotation)
        foreRightRotationNode = sg.findNode(birdNode, "foreRightRotation")
        foreRightRotationNode.transform = tr.matmul(
            [tr.translate(0, -0.58, 0), tr.rotationX(-2 * rotation), tr.translate(0, 0.58, 0)])
        # Left wing
        upperLeftRotationNode = sg.findNode(birdNode, "upperLeftRotation")
        upperLeftRotationNode.transform = tr.rotationX(0.5 * rotation)
        foreLeftRotationNode = sg.findNode(birdNode, "foreLeftRotation")
        foreLeftRotationNode.transform = tr.matmul(
            [tr.translate(0, 0.58, 0), tr.rotationX(2 * rotation), tr.translate(0, -0.58, 0)])
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
        else:
            rotation -= dt

        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        mvpPipeline.drawShape(gpuAxis, GL_LINES)

        # The landscape is drawn with texture lighting
        glUseProgram(phongTexturePipeline.shaderProgram)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.8, 0.8, 0.8)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPosition"), 5, -3, 5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), 0, 5, 2)
        glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 500)

        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Drawing the landscape
        # Hills
        model1 = tr.matmul([tr.translate(25, -25, 0), tr.scale(0.1, 50, 20)])
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model1)
        phongTexturePipeline.drawShape(gpuHills)
        model2 = tr.matmul([tr.translate(0, -50, 0), tr.rotationZ(np.pi / 2), tr.scale(0.1, 50, 20)])
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model2)
        phongTexturePipeline.drawShape(gpuHills)
        model3 = tr.matmul([tr.translate(-25, -25, 0), tr.scale(0.1, 50, 20)])
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model3)
        phongTexturePipeline.drawShape(gpuHills)

        # Grass
        model4 = tr.matmul([tr.translate(0, -30, -10), tr.scale(50, 65, 0.1)])
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model4)
        phongTexturePipeline.drawShape(gpuGrass)

        # Sky
        model5 = tr.matmul([tr.translate(0, -30, 10), tr.scale(50, 65, 0.1)])
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model5)
        phongTexturePipeline.drawShape(gpuSky)

        # The bird is drawn with lighting effects
        glUseProgram(phongPipeline.shaderProgram)

        # Setting all uniform shader variables
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.9, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPosition"), 5, -3, 5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), 0, 5, 2)
        glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 500)

        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        # Drawing the Bird
        sg.drawSceneGraphNode(birdNode, phongPipeline, "model")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
