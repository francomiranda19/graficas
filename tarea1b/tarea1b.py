import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import random

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')

def createShip():
    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1, 1, 1))
    gpuGreyTriangle = es.toGPUShape(bs.createColorTriangle(0.5, 0.5, 0.5))
    gpuOrangeTriangle = es.toGPUShape(bs.createColorTriangle(1, 112 / 255, 40 / 255))
    gpuYellowTriangle = es.toGPUShape(bs.createColorTriangle(1, 1, 0))
    gpuRedTriangle = es.toGPUShape(bs.createColorTriangle(1, 0, 0))


    # Creating a single orange flame
    orangeFlame = sg.SceneGraphNode("orangeFlame")
    orangeFlame.transform = tr.matmul([tr.rotationZ(np.pi), tr.uniformScale(0.1)])
    orangeFlame.childs += [gpuOrangeTriangle]

    # Instanciating 6 orange flames, for the wings and back parts
    backLeftOrangeFlame = sg.SceneGraphNode("backLeftOrangeFlame")
    backLeftOrangeFlame.transform = tr.translate(-0.11,-0.55, 0.0 )
    backLeftOrangeFlame.childs += [orangeFlame]

    backRightOrangeFlame = sg.SceneGraphNode("backRightOrangeFlame")
    backRightOrangeFlame.transform = tr.translate(0.11, -0.55, 0.0)
    backRightOrangeFlame.childs += [orangeFlame]

    leftWingLeftOrangeFlame = sg.SceneGraphNode("leftWingLeftOrangeFlame")
    leftWingLeftOrangeFlame.transform = tr.matmul([tr.translate(-0.45, -0.07, 0.0), tr.uniformScale(0.5)])
    leftWingLeftOrangeFlame.childs += [orangeFlame]

    leftWingRightOrangeFlame = sg.SceneGraphNode("leftWingRightOrangeFlame")
    leftWingRightOrangeFlame.transform = tr.matmul([tr.translate(-0.3, -0.07, 0.0), tr.uniformScale(0.5)])
    leftWingRightOrangeFlame.childs += [orangeFlame]

    rightWingLeftOrangeFlame = sg.SceneGraphNode("rightWingLeftOrangeFlame")
    rightWingLeftOrangeFlame.transform = tr.matmul([tr.translate(0.3, -0.07, 0.0), tr.uniformScale(0.5)])
    rightWingLeftOrangeFlame.childs += [orangeFlame]

    rightWingRightOrangeFlame = sg.SceneGraphNode("rightWingRightOrangeFlame")
    rightWingRightOrangeFlame.transform = tr.matmul([tr.translate(0.45, -0.07, 0.0), tr.uniformScale(0.5)])
    rightWingRightOrangeFlame.childs += [orangeFlame]


    # Creating a single yellow flame
    yellowFlame = sg.SceneGraphNode("yellowFlame")
    yellowFlame.transform = tr.matmul([tr.rotationZ(np.pi), tr.uniformScale(0.2)])
    yellowFlame.childs += [gpuYellowTriangle]

    # Instanciating 6 yellow flames, for the wings and back parts
    backLeftYellowFlame = sg.SceneGraphNode("backLeftYellowFlame")
    backLeftYellowFlame.transform = tr.translate(-0.11, -0.6, 0.0)
    backLeftYellowFlame.childs += [yellowFlame]

    backRightYellowFlame = sg.SceneGraphNode("backRightYellowFlame")
    backRightYellowFlame.transform = tr.translate(0.11, -0.6, 0.0)
    backRightYellowFlame.childs += [yellowFlame]

    leftWingLeftYellowFlame = sg.SceneGraphNode("leftWingLeftYellowFlame")
    leftWingLeftYellowFlame.transform = tr.matmul([tr.translate(-0.45, -0.1, 0.0), tr.uniformScale(0.5)])
    leftWingLeftYellowFlame.childs += [yellowFlame]

    leftWingRightYellowFlame = sg.SceneGraphNode("leftWingRightYellowFlame")
    leftWingRightYellowFlame.transform = tr.matmul([tr.translate(-0.3, -0.1, 0.0), tr.uniformScale(0.5)])
    leftWingRightYellowFlame.childs += [yellowFlame]

    rightWingLeftYellowFlame = sg.SceneGraphNode("rightWingLeftYellowFlame")
    rightWingLeftYellowFlame.transform = tr.matmul([tr.translate(0.3, -0.1, 0.0), tr.uniformScale(0.5)])
    rightWingLeftYellowFlame.childs += [yellowFlame]

    rightWingRightYellowFlame = sg.SceneGraphNode("rightWingRightYellowFlame")
    rightWingRightYellowFlame.transform = tr.matmul([tr.translate(0.45, -0.1, 0.0), tr.uniformScale(0.5)])
    rightWingRightYellowFlame.childs += [yellowFlame]


    # Creating a single wing
    wing = sg.SceneGraphNode("wing")
    wing.transform = tr.matmul([tr.translate(0, 0.3, 0), tr.scale(1.1, 0.7, 1)])
    wing.childs += [gpuGreyTriangle]


    # Creating the upper part
    upper = sg.SceneGraphNode("upper")
    upper.transform = tr.matmul([tr.translate(0, 0.7, 0), tr.uniformScale(0.5)])
    upper.childs += [gpuRedTriangle]


    # Creating the chasis of the ship
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.scale(0.5, 1, 1)
    chasis.childs += [gpuWhiteQuad]


    ship = sg.SceneGraphNode("ship")
    ship.childs += [backLeftYellowFlame]
    ship.childs += [backRightYellowFlame]
    ship.childs += [leftWingLeftYellowFlame]
    ship.childs += [leftWingRightYellowFlame]
    ship.childs += [rightWingLeftYellowFlame]
    ship.childs += [rightWingRightYellowFlame]
    ship.childs += [backLeftOrangeFlame]
    ship.childs += [backRightOrangeFlame]
    ship.childs += [leftWingLeftOrangeFlame]
    ship.childs += [leftWingRightOrangeFlame]
    ship.childs += [rightWingLeftOrangeFlame]
    ship.childs += [rightWingRightOrangeFlame]
    ship.childs += [wing]
    ship.childs += [upper]
    ship.childs += [chasis]

    traslatedShip = sg.SceneGraphNode("traslatedShip")
    traslatedShip.transform = tr.translate(0, -0.2, 0)
    traslatedShip.childs += [ship]

    return traslatedShip


def createEnemyShip():
    gpuGreenQuad = es.toGPUShape(bs.createColorQuad(0, 1, 0))
    gpuGreyQuad = es.toGPUShape(bs.createColorQuad(0.5, 0.5, 0.5))
    gpuBlueTriangle = es.toGPUShape(bs.createColorTriangle(0, 0, 1))
    gpuGreyTriangle = es.toGPUShape(bs.createColorTriangle(0.5, 0.5, 0.5))
    gpuOrangeTriangle = es.toGPUShape(bs.createColorTriangle(1, 112 / 255, 40 / 255))
    gpuYellowTriangle = es.toGPUShape(bs.createColorTriangle(1, 1, 0))
    gpuRedTriangle = es.toGPUShape(bs.createColorTriangle(1, 0, 0))


    # Creating a single orange flame
    orangeFlame = sg.SceneGraphNode("orangeFlame")
    orangeFlame.transform = tr.matmul([tr.rotationZ(np.pi), tr.uniformScale(0.1)])
    orangeFlame.childs += [gpuOrangeTriangle]

    # Instanciating 2 orange flames, for the back part
    backLeftOrangeFlame = sg.SceneGraphNode("backLeftOrangeFlame")
    backLeftOrangeFlame.transform = tr.translate(-0.11, -0.35, 0.0)
    backLeftOrangeFlame.childs += [orangeFlame]

    backRightOrangeFlame = sg.SceneGraphNode("backRightOrangeFlame")
    backRightOrangeFlame.transform = tr.translate(0.11, -0.35, 0.0)
    backRightOrangeFlame.childs += [orangeFlame]


    # Creating a single yellow flame
    yellowFlame = sg.SceneGraphNode("yellowFlame")
    yellowFlame.transform = tr.matmul([tr.rotationZ(np.pi), tr.uniformScale(0.2)])
    yellowFlame.childs += [gpuYellowTriangle]

    # Instanciating 2 yellow flames, for the back part
    backLeftYellowFlame = sg.SceneGraphNode("backLeftYellowFlame")
    backLeftYellowFlame.transform = tr.translate(-0.11, -0.4, 0.0)
    backLeftYellowFlame.childs += [yellowFlame]

    backRightYellowFlame = sg.SceneGraphNode("backRightYellowFlame")
    backRightYellowFlame.transform = tr.translate(0.11, -0.4, 0.0)
    backRightYellowFlame.childs += [yellowFlame]


    # Creating the back part
    back = sg.SceneGraphNode("wing")
    back.transform = tr.uniformScale(0.7)
    back.childs += [gpuGreyTriangle]


    # Creating the upper part
    upper = sg.SceneGraphNode("upper")
    upper.transform = tr.matmul([tr.translate(0, 0.5, 0), tr.uniformScale(0.5)])
    upper.childs += [gpuBlueTriangle]


    # Creating the chasis of the ship
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.uniformScale(0.5)
    chasis.childs += [gpuGreenQuad]


    enemyShip = sg.SceneGraphNode("enemyShip")
    enemyShip.childs += [backLeftYellowFlame]
    enemyShip.childs += [backRightYellowFlame]
    enemyShip.childs += [backLeftOrangeFlame]
    enemyShip.childs += [backRightOrangeFlame]
    enemyShip.childs += [back]
    enemyShip.childs += [upper]
    enemyShip.childs += [chasis]

    traslatedEnemyShip = sg.SceneGraphNode("traslatedEnemyShip")
    traslatedEnemyShip.transform = tr.translate(0, -0.2, 0)
    traslatedEnemyShip.childs += [enemyShip]

    return traslatedEnemyShip

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Enemy Ship", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Creating shapes on GPU memory
    ship = createShip()
    enemyShip = createEnemyShip()

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the Ship
        sg.drawSceneGraphNode(enemyShip, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
