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

    # Assembling the shader program
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Telling openGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # As we work in 3D, we need to check which part is in front, and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))

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
        atX = 3 * np.sin(np.pi * mousePosX)
        atY = 3 * np.cos(np.pi * mousePosX)

        atPos = np.array([atX, atY, 3 * mousePosY])

        view = tr.lookAt(
            np.array([1, 1, 1]),
            atPos,
            np.array([0, 0, 1])
        )

        # Setting up the model transform
        model = tr.identity()

        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # The bird is drawn with lighting effects
        mvpPipeline.drawShape(gpuAxis, GL_LINES)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()