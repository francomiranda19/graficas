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
    showAxis = True

controller = Controller()

def on_key(window, key, scancode, action, mods):
    global controller  # Declares that we are going to use the global object controller inside this function.

    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
            sys.exit()

class CreateBird():
    def __init__(self):
        self.gpu_body = es.toGPUShape(bs.createColorCube(0.1, 0.1, 0.1))
        self.gpu_upper_wing = es.toGPUShape(bs.createColorCube(0.1, 0.1, 0.1))
        self.gpu_fore_wing = es.toGPUShape(bs.createColorCube(0.9, 0.9, 0.9))
        self.gpu_neck = es.toGPUShape(bs.createColorCube(0.9, 0.9, 0.9))
        self.gpu_head = es.toGPUShape(bs.createColorCube(0.1, 0.1, 0.1))
        self.gpu_back_wing = es.toGPUShape(bs.createColorCube(0.9, 0.9, 0.9))
        self.gpu_paw = es.toGPUShape(bs.createColorCube(0.9, 0, 0))

        # Body of the bird
        self.body = sg.SceneGraphNode("body")
        self.body.transform = tr.scale(1, 0.7, 0.5)
        self.body.childs += [self.gpu_body]

        # Creating a single upper wing
        self.upperWing = sg.SceneGraphNode("upperWing")
        self.upperWing.transform = tr.scale(0.5, 0.5, 0.1)
        self.upperWing.childs += [self.gpu_upper_wing]

        # Creating the upper parts of both wings
        self.upperLeft = sg.SceneGraphNode("upperLeft")
        self.upperLeft.transform = tr.matmul([tr.translate(0, -0.5, 0), tr.rotationX(5 * np.pi / 6)])
        self.upperLeft.childs += [self.upperWing]

        self.upperRight = sg.SceneGraphNode("upperRight")
        self.upperRight.transform = tr.matmul([tr.translate(0, 0.5, 0), tr.rotationX(np.pi / 6)])
        self.upperRight.childs += [self.upperWing]

        # Creating a single fore wing
        self.foreWing = sg.SceneGraphNode("foreWing")
        self.foreWing.transform = tr.scale(0.5, 0.7, 0.1)
        self.foreWing.childs += [self.gpu_fore_wing]

        # Creating the fore parts of both wings
        self.foreLeft = sg.SceneGraphNode("foreLeft")
        self.foreLeft.transform = tr.matmul([tr.translate(0, -1, -0.05), tr.rotationX(7 * np.pi / 6)])
        self.foreLeft.childs += [self.foreWing]

        self.foreRight = sg.SceneGraphNode("foreRight")
        self.foreRight.transform = tr.matmul([tr.translate(0, 1, -0.05), tr.rotationX(-np.pi / 6)])
        self.foreRight.childs += [self.foreWing]

        # Creating the neck of the bird
        self.neck = sg.SceneGraphNode("neck")
        self.neck.transform = tr.matmul(
            [tr.translate(-0.5, 0, 0.2), tr.rotationY(-2 * np.pi / 3), tr.scale(0.6, 0.3, 0.3)])
        self.neck.childs += [self.gpu_neck]

        # Creating the head of the bird
        self.head = sg.SceneGraphNode("head")
        self.head.transform = tr.matmul([tr.translate(-0.8, 0, 0.5), tr.uniformScale(0.5)])
        self.head.childs += [self.gpu_head]

        # Creating the back wing of the bird
        self.backWing = sg.SceneGraphNode("backWing")
        self.backWing.transform = tr.matmul(
            [tr.translate(0.6, 0, 0.2), tr.rotationY(2.5 * np.pi / 3), tr.scale(0.6, 0.3, 0.3)])
        self.backWing.childs += [self.gpu_back_wing]

        # Creating a single paw
        self.paw = sg.SceneGraphNode("paw")
        self.paw.transform = tr.scale(0.1, 0.1, 1)
        self.paw.childs += [self.gpu_paw]

        # Creating both paws
        self.leftPaw = sg.SceneGraphNode("leftPaw")
        self.leftPaw.transform = tr.translate(0, -0.2, -0.3)
        self.leftPaw.childs += [self.paw]

        self.rightPaw = sg.SceneGraphNode("rightPaw")
        self.rightPaw.transform = tr.translate(0, 0.2, -0.3)
        self.rightPaw.childs += [self.paw]

        # Creating the bird
        self.bird = sg.SceneGraphNode("bird")
        self.bird.childs += [self.body]
        self.bird.childs += [self.upperLeft]
        self.bird.childs += [self.upperRight]
        self.bird.childs += [self.foreLeft]
        self.bird.childs += [self.foreRight]
        self.bird.childs += [self.neck]
        self.bird.childs += [self.head]
        self.bird.childs += [self.backWing]
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

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleModelViewProjectionShaderProgram()  # Indicamos el shader que utilizaremos

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)  # INDICAMOS PIPELINE.SHADERPROGRAM

    # Setting up the clear screen color
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    gpuAxis = es.toGPUShape(bs.createAxis(7))
    bird = CreateBird()  ## OJO, LA GPUSHAPE VA ACÁ PORQUE SE TRANSFORMA CONSTANTEMENTE
    birdNode = bird.get_bird()

    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(width) / float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    view = tr.lookAt(
        np.array([5, 5, 5]),
        np.array([0, 0, 0]),
        np.array([0, 0, 1])
    )
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if controller.showAxis:
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            pipeline.drawShape(gpuAxis, GL_LINES)

        # Drawing the Arm
        sg.drawSceneGraphNode(birdNode, pipeline, "model")  # FIJARSE QUE LO PONEMOS AQUÍ PARA QUE SE ACTUALICE

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()