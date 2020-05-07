import glfw
from OpenGL.GL import *
import numpy as np
import sys

import scene_graph as sg
import basic_shapes as bs
import easy_shaders as es
import transformations as tr
import lighting_shaders as ls

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

class Bird():
    def __init__(self):
        self.gpu_body = es.toGPUShape(bs.createColorNormalsCube(0.1, 0.1, 0.1))
        self.gpu_upper_wing = es.toGPUShape(bs.createColorNormalsCube(0.1, 0.1, 0.1))
        self.gpu_fore_wing = es.toGPUShape(bs.createColorNormalsCube(0.9, 0.9, 0.9))
        self.gpu_neck = es.toGPUShape(bs.createColorNormalsCube(0.9, 0.9, 0.9))
        self.gpu_head = es.toGPUShape(bs.createColorNormalsCube(0.1, 0.1, 0.1))
        self.gpu_back_wing = es.toGPUShape(bs.createColorNormalsCube(0.9, 0.9, 0.9))
        self.gpu_paw = es.toGPUShape(bs.createColorNormalsCube(0.9, 0, 0))

        # Body of the bird
        self.body = sg.SceneGraphNode("body")
        self.body.transform = tr.scale(1, 0.7, 0.5)
        self.body.childs += [self.gpu_body]

        # Creating a single upper wing
        self.upperWing = sg.SceneGraphNode("upperWing")
        self.upperWing.transform = tr.scale(0.5, 0.5, 0.1)
        self.upperWing.childs += [self.gpu_upper_wing]

        # Creating a single fore wing
        self.foreWing = sg.SceneGraphNode("foreWing")
        self.foreWing.transform = tr.scale(0.5, 0.7, 0.1)
        self.foreWing.childs += [self.gpu_fore_wing]

        # Creating the right wing of the bird
        self.upperRight = sg.SceneGraphNode("upperRight")
        self.upperRight.transform = tr.matmul([tr.translate(0, -0.5, 0), tr.rotationX(5 * np.pi / 6)])
        self.upperRight.childs += [self.upperWing]

        self.foreRight = sg.SceneGraphNode("foreRight")
        self.foreRight.transform = tr.matmul([tr.translate(0, -1, -0.05), tr.rotationX(7 * np.pi / 6)])
        self.foreRight.childs += [self.foreWing]

        self.rightWingRotation = sg.SceneGraphNode("rightWingRotation")
        self.rightWingRotation.childs += [self.upperRight, self.foreRight]

        # Creating the left wing of the bird
        self.upperLeft = sg.SceneGraphNode("upperLeft")
        self.upperLeft.transform = tr.matmul([tr.translate(0, 0.5, 0), tr.rotationX(np.pi / 6)])
        self.upperLeft.childs += [self.upperWing]

        self.foreLeft = sg.SceneGraphNode("foreLeft")
        self.foreLeft.transform = tr.matmul([tr.translate(0, 1, -0.05), tr.rotationX(-np.pi / 6)])
        self.foreLeft.childs += [self.foreWing]

        self.leftWingRotation = sg.SceneGraphNode("leftWingRotation")
        self.leftWingRotation.childs += [self.upperLeft, self.foreLeft]

        # Creating the neck of the bird
        self.neck = sg.SceneGraphNode("neck")
        self.neck.transform = tr.matmul(
            [tr.translate(0.5, 0, 0.2), tr.rotationY(2.5 * np.pi / 3), tr.scale(0.6, 0.3, 0.3)])
        self.neck.childs += [self.gpu_neck]

        # Creating the head of the bird
        self.head = sg.SceneGraphNode("head")
        self.head.transform = tr.matmul([tr.translate(0.8, 0, 0.5), tr.uniformScale(0.5)])
        self.head.childs += [self.gpu_head]

        self.headAndNeckRotation = sg.SceneGraphNode("headAndNeckRotation")
        self.headAndNeckRotation.childs += [self.head, self.neck]

        # Creating the back wing of the bird
        self.backWing = sg.SceneGraphNode("backWing")
        self.backWing.transform = tr.matmul(
            [tr.translate(-0.6, 0, 0.1), tr.rotationY(-2.5 * np.pi / 3), tr.scale(0.6, 0.3, 0.3)])
        self.backWing.childs += [self.gpu_back_wing]

        self.backWingRotation = sg.SceneGraphNode("backWingRotation")
        self.backWingRotation.childs += [self.backWing]

        # Creating a single paw
        self.paw = sg.SceneGraphNode("paw")
        self.paw.transform = tr.scale(0.1, 0.1, 1)
        self.paw.childs += [self.gpu_paw]

        # Creating both paws
        self.rightPaw = sg.SceneGraphNode("rightPaw")
        self.rightPaw.transform = tr.translate(0, -0.2, -0.3)
        self.rightPaw.childs += [self.paw]

        self.leftPaw = sg.SceneGraphNode("leftPaw")
        self.leftPaw.transform = tr.translate(0, 0.2, -0.3)
        self.leftPaw.childs += [self.paw]

        # Creating the bird
        self.bird = sg.SceneGraphNode("bird")
        self.bird.childs += [self.body]
        self.bird.childs += [self.rightWingRotation]
        self.bird.childs += [self.leftWingRotation]
        self.bird.childs += [self.headAndNeckRotation]
        self.bird.childs += [self.backWingRotation]
        self.bird.childs += [self.leftPaw]
        self.bird.childs += [self.rightPaw]

    # Get bird
    def get_bird(self):
        return self.bird


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Bird", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting callback functions to handle keyboard and mouse events
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    # Lighting program
    phongPipeline = ls.SimplePhongShaderProgram()

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # As we work in 3D, we need to check which part is in front, and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    bird = Bird()
    birdNode = bird.get_bird()

    t0 = glfw.get_time()
    camera_theta = np.pi / 4

    while not glfw.window_should_close(window):
        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            camera_theta -= 2 * dt

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            camera_theta += 2 * dt

        projection = tr.perspective(45, float(width) / float(height), 0.1, 100)

        camX = 3 * np.sin(camera_theta)
        camY = 3 * np.cos(camera_theta)

        viewPos = np.array([camX, camY, 2])

        view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        axis = np.array([0, 0, 1])
        axis = axis / np.linalg.norm(axis)
        model = tr.identity()

        # Getting the mouse location in opengl coordinates
        mousePosX = 2 * (controller.mousePos[0] - width / 2) / width
        mousePosY = 2 * (height / 2 - controller.mousePos[1]) / height

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # The axis is drawn without lighting effects
        glUseProgram(mvpPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        mvpPipeline.drawShape(gpuAxis, GL_LINES)

        # Getting the nodes that are going to be transformed
        leftWingRotationNode = sg.findNode(birdNode, "leftWingRotation")
        rightWingRotationNode = sg.findNode(birdNode, "rightWingRotation")
        headAndNeckRotationNode = sg.findNode(birdNode, "headAndNeckRotation")
        backWingRotationNode = sg.findNode(birdNode, "backWingRotation")

        # Nodes transformations
        if mousePosY > -0.4 and mousePosY < 0.4:
            leftWingRotationNode.transform = tr.rotationX(0.5 * mousePosY)
            rightWingRotationNode.transform = tr.rotationX(-0.5 * mousePosY)
            headAndNeckRotationNode.transform = tr.rotationY(0.5 * mousePosY)
            backWingRotationNode.transform = tr.rotationY(-0.5 * mousePosY)

        # The bird is drawn with lighting effects
        glUseProgram(phongPipeline.shaderProgram)

        # Setting all uniform shader variables
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.9, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPosition"), -6, 6, 6)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1],
                    viewPos[2])
        glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 50)

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