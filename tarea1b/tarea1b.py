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

class Controller:
    x = 0.0
    y = 0.0

# we will use the global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):
    global controller

    # Keep pressed buttons
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_A:
            if controller.x <= -1.0:
                return
            controller.x -= 0.05

        elif key == glfw.KEY_D:
            if controller.x >= 1.0:
                return
            controller.x += 0.05

        elif key == glfw.KEY_W:
            if controller.y >= 0.5:
                return
            controller.y += 0.05

        elif key == glfw.KEY_S:
            if controller.y <= 0.0:
                return
            controller.y -= 0.05

    if action != glfw.PRESS:
        return

    elif key == glfw.KEY_ESCAPE:
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

    translatedShip = sg.SceneGraphNode("translatedShip")
    translatedShip.childs += [ship]
    translatedShip.pos_x = controller.x
    translatedShip.pos_y = controller.y

    return translatedShip


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

    translatedEnemyShip = sg.SceneGraphNode("translatedEnemyShip")
    translatedEnemyShip.transform = tr.translate(0, -0.2, 0)
    translatedEnemyShip.childs += [enemyShip]
    translatedEnemyShip.pos_x = controller.x
    translatedEnemyShip.pos_y = controller.y

    return translatedEnemyShip

def createRedPlanet():
    x0 = random.uniform(-1, 1); y0 = random.uniform(-1, 2)
    gpuRedPlanet = es.toGPUShape(bs.createColorCircle(60, [1, 0, 0], 0.4))

    redPlanet = sg.SceneGraphNode("redPlanet")
    redPlanet.transform = tr.uniformScale(0.05)
    redPlanet.childs += [gpuRedPlanet]

    redPlanet1 = sg.SceneGraphNode("redPlanet1")
    redPlanet1.transform = tr.translate(x0, y0, 0)
    redPlanet1.childs += [redPlanet]

    redPlanets = sg.SceneGraphNode("redPlanets")
    redPlanets.childs += [redPlanet1]
    redPlanets.pos_x = x0
    redPlanets.pos_y = y0

    return redPlanets

def createGreenPlanet():
    x0 = random.uniform(-1, 1); y0 = random.uniform(-1, 2)
    gpuGreenPlanet = es.toGPUShape(bs.createColorCircle(60, [0, 1, 0], 0.4))

    greenPlanet = sg.SceneGraphNode("greenPlanet")
    greenPlanet.transform = tr.uniformScale(0.05)
    greenPlanet.childs += [gpuGreenPlanet]

    greenPlanet1 = sg.SceneGraphNode("greenPlanet1")
    greenPlanet1.transform = tr.translate(x0, y0, 0)
    greenPlanet1.childs += [greenPlanet]

    greenPlanets = sg.SceneGraphNode("greenPlanets")
    greenPlanets.childs += [greenPlanet1]
    greenPlanets.pos_x = x0
    greenPlanets.pos_y = y0

    return greenPlanets

def createBluePlanet():
    x0 = random.uniform(-1, 1); y0 = random.uniform(-1, 2)
    gpuBluePlanet = es.toGPUShape(bs.createColorCircle(60, [0, 0, 1], 0.4))

    bluePlanet = sg.SceneGraphNode("bluePlanet")
    bluePlanet.transform = tr.uniformScale(0.05)
    bluePlanet.childs += [gpuBluePlanet]

    bluePlanet1 = sg.SceneGraphNode("bluePlanet1")
    bluePlanet1.transform = tr.translate(x0, y0, 0)
    bluePlanet1.childs += [bluePlanet]

    bluePlanets = sg.SceneGraphNode("bluePlanets")
    bluePlanets.childs += [bluePlanet1]
    bluePlanets.pos_x = x0
    bluePlanets.pos_y = y0

    return bluePlanets

def createStar():
    x0 = random.uniform(-1, 1); y0 = random.uniform(-1, 2)
    gpuStar = es.toGPUShape(bs.createColorCircle(60, [1, 1, 1]))

    star = sg.SceneGraphNode("star")
    star.transform = tr.uniformScale(0.01)
    star.childs += [gpuStar]

    star1 = sg.SceneGraphNode("star1")
    star1.transform = tr.translate(x0, y0, 0)
    star1.childs += [star]

    stars = sg.SceneGraphNode("stars")
    stars.childs += [star1]
    stars.pos_x = x0
    stars.pos_y = y0

    return stars

def createShot():
    gpuWhiteQuad = es.toGPUShape(bs.createColorQuad(1, 1, 1))

    # Creating a single shot
    shot = sg.SceneGraphNode("shot")
    shot.transform = tr.scale(0.1, 0.3, 1)
    shot.childs += [gpuWhiteQuad]

    shots = sg.SceneGraphNode("shots")
    shots.childs += [shot]
    shots.pos_x = controller.x
    shots.pos_y = 2

    return shots


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Space War", None, None)

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
    shot = createShot()

    redPlanet1 = createRedPlanet(); greenPlanet1 = createGreenPlanet(); bluePlanet1 = createBluePlanet()
    redPlanet2 = createRedPlanet(); greenPlanet2 = createGreenPlanet(); bluePlanet2 = createBluePlanet()
    redPlanet3 = createRedPlanet(); greenPlanet3 = createGreenPlanet(); bluePlanet3 = createBluePlanet()
    redPlanet4 = createRedPlanet(); greenPlanet4 = createGreenPlanet(); bluePlanet4 = createBluePlanet()
    redPlanet5 = createRedPlanet(); greenPlanet5 = createGreenPlanet(); bluePlanet5 = createBluePlanet()
    redPlanet6 = createRedPlanet(); greenPlanet6 = createGreenPlanet(); bluePlanet6 = createBluePlanet()

    star1 = createStar(); star11 = createStar()
    star2 = createStar(); star12 = createStar()
    star3 = createStar(); star13 = createStar()
    star4 = createStar(); star14 = createStar()
    star5 = createStar(); star15 = createStar()
    star6 = createStar(); star16 = createStar()
    star7 = createStar(); star17 = createStar()
    star8 = createStar(); star18 = createStar()
    star9 = createStar(); star19 = createStar()
    star10 = createStar(); star20 = createStar()

    redPlanets = [redPlanet1, redPlanet2, redPlanet3, redPlanet4, redPlanet5, redPlanet6]
    greenPlanets = [greenPlanet1, greenPlanet2, greenPlanet3, greenPlanet4, greenPlanet5, greenPlanet6]
    bluePlanets = [bluePlanet1, bluePlanet2, bluePlanet3, bluePlanet4, bluePlanet5, bluePlanet6]
    stars = [star1, star2, star3, star4, star5, star6, star7, star8, star9, star10,
             star11, star12, star13, star14, star15, star16, star17, star18, star19, star20]

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS or glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            ship.pos_x = controller.x
            shot.pos_x = ship.pos_x
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS or glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            ship.pos_y = controller.y

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the scene
        for redPlanet in redPlanets:
            redPlanet.transform = tr.translate(0, redPlanet.pos_y, 0)
            if redPlanet.pos_y - dt > -3:
                redPlanet.pos_y -= dt
            else:
                redPlanet.pos_y = 2
                redPlanet.pos_y -= dt

        for greenPlanet in greenPlanets:
            greenPlanet.transform = tr.translate(0, greenPlanet.pos_y, 0)
            if greenPlanet.pos_y - dt > -3:
                greenPlanet.pos_y -= dt
            else:
                greenPlanet.pos_y = 2
                greenPlanet.pos_y -= dt

        for bluePlanet in bluePlanets:
            bluePlanet.transform = tr.translate(0, bluePlanet.pos_y, 0)
            if bluePlanet.pos_y - dt > -3:
                bluePlanet.pos_y -= dt
            else:
                bluePlanet.pos_y = 2
                bluePlanet.pos_y -= dt

        for star in stars:
            star.transform = tr.translate(0, star.pos_y, 0)
            if star.pos_y - dt > -3:
                star.pos_y -= dt
            else:
                star.pos_y = 2
                star.pos_y -= dt


        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            if shot.pos_y <= 2:
                shot.transform = tr.matmul(
                    [tr.translate(ship.pos_x, shot.pos_y, 0), tr.translate(0, -0.8, 0), tr.uniformScale(0.2)])
                shot.pos_y += 5*dt
            else:
                shot.pos_y = ship.pos_y
        else:
            if shot.pos_y > 2:
                shot.transform = tr.translate(0, 2, 0)
            else:
                shot.transform = tr.matmul(
                    [tr.translate(ship.pos_x, shot.pos_y, 0), tr.translate(0, -0.8, 0), tr.uniformScale(0.2)])
                shot.pos_y += 5*dt


        ship.transform = tr.matmul([tr.translate(controller.x, controller.y, 0),
                                    tr.translate(0, -0.8, 0),
                                    tr.uniformScale(0.2)])


        for redPlanet in redPlanets:
            sg.drawSceneGraphNode(redPlanet, pipeline, "transform")
        for greenPlanet in greenPlanets:
            sg.drawSceneGraphNode(greenPlanet, pipeline, "transform")
        for bluePlanet in bluePlanets:
            sg.drawSceneGraphNode(bluePlanet, pipeline, "transform")
        for star in stars:
            sg.drawSceneGraphNode(star, pipeline, "transform")

        sg.drawSceneGraphNode(shot, pipeline, "transform")
        sg.drawSceneGraphNode(ship, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
