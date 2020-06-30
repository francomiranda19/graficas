import glfw
from OpenGL.GL import *
import numpy as np
import sys
import json
import scene_graph as sg
import basic_shapes as bs
import easy_shaders as es
import transformations as tr
import lighting_shaders as ls

# Problem setup
FILENAME = 'temperatures.npy'
T_A = 15
T_B = 10
T_C = 25
N_A = 5
N_B = 3
N_C = 7

# A class to store the application control
class Controller:
    def __init__(self):
        self.showAxis = True
        self.a = True
        self.b = False
        self.c = False

controller = Controller()

def on_key(window, key, scancode, action, mods):
    global controller
    if action != glfw.PRESS:
        return
    if key == glfw.KEY_SPACE:
        controller.showAxis = not controller.showAxis
    elif key == glfw.KEY_A:
        controller.a = not controller.a
        controller.b = False
        controller.c = False
    elif key == glfw.KEY_B:
        controller.b = not controller.b
        controller.a = False
        controller.c = False
    elif key == glfw.KEY_C:
        controller.c = not controller.c
        controller.a = False
        controller.b = False
    elif key == glfw.KEY_ESCAPE:
        sys.exit()

class FishA:
    def __init__(self):
        self.t_a = T_A
        
        self.gpu_body = es.toGPUShape(bs.createColorNormalsCube(1.0, 0.0, 0.0))
        self.gpu_tail = es.toGPUShape(bs.createColorNormalsCube(1.0, 1.0, 0.0))

        # Body of the fish
        self.body = sg.SceneGraphNode('body')
        self.body.transform = tr.scale(0.6, 0.3, 0.3)
        self.body.childs += [self.gpu_body]

        # Tail of the fish
        self.tail = sg.SceneGraphNode('tail')
        self.tail.transform = tr.matmul([tr.translate(-0.4, 0, 0), tr.scale(0.2, 0.05, 0.2)])
        self.tail.childs += [self.gpu_tail]

        self.tailRotation = sg.SceneGraphNode('tailRotation')
        self.tailRotation.childs += [self.tail]

        # Creating the fish
        self.fishA = sg.SceneGraphNode('fishA')
        self.fishA.childs += [self.body]
        self.fishA.childs += [self.tailRotation]

    # Get fish
    def get_fish(self):
        return self.fishA


class FishB:
    def __init__(self):
        self.t_b = T_B

        self.gpu_body = es.toGPUShape(bs.createColorNormalsCube(0.0, 1.0, 0.0))
        self.gpu_tail = es.toGPUShape(bs.createColorNormalsCube(1.0, 0.0, 128 / 255))

        # Body of the fish
        self.body = sg.SceneGraphNode('body')
        self.body.transform = tr.scale(0.6, 0.3, 0.3)
        self.body.childs += [self.gpu_body]

        # Tail of the fish
        self.tail = sg.SceneGraphNode('tail')
        self.tail.transform = tr.matmul([tr.translate(-0.4, 0, 0), tr.scale(0.2, 0.05, 0.2)])
        self.tail.childs += [self.gpu_tail]

        self.tailRotation = sg.SceneGraphNode('tailRotation')
        self.tailRotation.childs += [self.tail]

        # Creating the fish
        self.fishB = sg.SceneGraphNode('fishB')
        self.fishB.childs += [self.body]
        self.fishB.childs += [self.tailRotation]

    # Get fish
    def get_fish(self):
        return self.fishB

class FishC:
    def __init__(self):
        self.t_c = T_C

        self.gpu_body = es.toGPUShape(bs.createColorNormalsCube(1.0, 1.0, 0.0))
        self.gpu_tail = es.toGPUShape(bs.createColorNormalsCube(1.0, 128 / 255, 0.0))

        # Body of the fish
        self.body = sg.SceneGraphNode('body')
        self.body.transform = tr.scale(0.6, 0.3, 0.3)
        self.body.childs += [self.gpu_body]

        # Tail of the fish
        self.tail = sg.SceneGraphNode('tail')
        self.tail.transform = tr.matmul([tr.translate(-0.4, 0, 0), tr.scale(0.2, 0.05, 0.2)])
        self.tail.childs += [self.gpu_tail]

        self.tailRotation = sg.SceneGraphNode('tailRotation')
        self.tailRotation.childs += [self.tail]

        # Creating the fish
        self.fishC = sg.SceneGraphNode('fishC')
        self.fishC.childs += [self.body]
        self.fishC.childs += [self.tailRotation]

    # Get fish
    def get_fish(self):
        return self.fishC

if __name__ == '__main__':

    # Initialize GLFW
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, 'Aquarium', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting callback function to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Simple shader program
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Lighting program
    phongPipeline = ls.SimplePhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # As we work in 3D, we need to check which part is in front, and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creating shapes on GPU Memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    fishA = FishA(); fishB = FishB(); fishC = FishC()
    fishANode = fishA.get_fish(); fishBNode = fishB.get_fish(); fishCNode = fishC.get_fish()

    t0 = glfw.get_time()
    camera_theta = np.pi / 4
    rotation = 0
    zoom = 0

    while not glfw.window_should_close(window):
        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            camera_theta -= 2 * dt
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            camera_theta += 2 * dt

        # Projection
        projection = tr.perspective(45, float(width) / float(height), 0.1, 100)

        # View
        camX = 3 * np.sin(camera_theta)
        camY = 3 * np.cos(camera_theta)
        viewPos = np.array([camX, camY, 3 - zoom])
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS and 2 <= viewPos[2]:
            zoom += dt
            if viewPos[2] < 2:
                viewPos[2] = 2
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS and viewPos[2] <= 4.5:
            zoom -= dt
            if viewPos[2] > 4.5:
                viewPos[2] = 4.5

        view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        # Model
        model = tr.identity()

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Getting the nodes that are going to be transformed
        tailRotationA = sg.findNode(fishANode, 'tailRotation')
        tailRotationB = sg.findNode(fishBNode, 'tailRotation')
        tailRotationC = sg.findNode(fishCNode, 'tailRotation')

        # The axis is drawn without lighting effects
        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawShape(gpuAxis, GL_LINES)

        glUseProgram(phongPipeline.shaderProgram)

        # Setting all uniform shader variables
        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        # Object is barely visible at only ambient. Bright white for diffuse and specular components.
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.9, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 0.5, 0.5, 0.5)

        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPosition"), -6, 6, 6)
        glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1],
                    viewPos[2])
        glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 500)

        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, model)

        # Movement of the tails
        tailRotationA.transform = tr.rotationZ(rotation)
        tailRotationB.transform = tr.rotationZ(rotation)
        tailRotationC.transform = tr.rotationZ(rotation)

        # dty determines the movement of the wings
        dty = np.sin(5 * t0)
        if dty > 0:
            rotation += dt
            if dty > 0.99: # This is for preventing errors
                rotation = 0
        else:
            rotation -= dt

        # Drawing the fishes
        if controller.a:
            sg.drawSceneGraphNode(fishANode, phongPipeline, 'model')
        if controller.b:
            sg.drawSceneGraphNode(fishBNode, phongPipeline, 'model')
        if controller.c:
            sg.drawSceneGraphNode(fishCNode, phongPipeline, 'model')

        # Once the render is done, buffers are swapped, showing only the complete scene
        glfw.swap_buffers(window)

    glfw.terminate()