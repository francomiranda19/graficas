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
    shoot = False

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

        if key == glfw.KEY_D:
            if controller.x >= 1.0:
                return
            controller.x += 0.05

        if key == glfw.KEY_W:
            if controller.y >= 0.5:
                return
            controller.y += 0.05

        if key == glfw.KEY_S:
            if controller.y <= 0.0:
                return
            controller.y -= 0.05

        if key == glfw.KEY_SPACE:
            controller.shoot = True

    if action != glfw.PRESS:
        return

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

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
    ship.transform = tr.matmul([tr.translate(0, -0.8, 0), tr.uniformScale(0.2)])
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
    gpuBlueTriangle = es.toGPUShape(bs.createColorTriangle(0, 0, 1))
    gpuGreyTriangle = es.toGPUShape(bs.createColorTriangle(0.5, 0.5, 0.5))
    gpuOrangeTriangle = es.toGPUShape(bs.createColorTriangle(1, 112 / 255, 40 / 255))
    gpuYellowTriangle = es.toGPUShape(bs.createColorTriangle(1, 1, 0))

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
    enemyShip.transform = tr.matmul([tr.translate(0, 2, 0), tr.rotationZ(np.pi), tr.uniformScale(0.2)])
    enemyShip.childs += [backLeftYellowFlame]
    enemyShip.childs += [backRightYellowFlame]
    enemyShip.childs += [backLeftOrangeFlame]
    enemyShip.childs += [backRightOrangeFlame]
    enemyShip.childs += [back]
    enemyShip.childs += [upper]
    enemyShip.childs += [chasis]

    translatedEnemyShip = sg.SceneGraphNode("translatedEnemyShip")
    translatedEnemyShip.childs += [enemyShip]
    translatedEnemyShip.pos_x = 1
    translatedEnemyShip.pos_y = 2

    return translatedEnemyShip

def createRedPlanet():
    x0 = random.uniform(-1, 1); y0 = random.uniform(-1, 2)
    gpuRedPlanet = es.toGPUShape(bs.createColorCircle(60, [1, 0, 0], 0.4))

    # Creating a single red planet
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

    # Creating a single green planet
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

    # Creating a single blue planet
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

    # Creating a single star
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
    shot.transform = tr.matmul([tr.translate(ship.pos_x, ship.pos_y, 0), tr.scale(0.1, 0.3, 0), tr.uniformScale(0.2)])
    shot.childs += [gpuWhiteQuad]

    shots = sg.SceneGraphNode("shots")
    shots.childs += [shot]
    shots.pos_x = ship.pos_x
    shots.pos_y = ship.pos_y

    return shots

def createEnemyShot():
    gpuRedQuad = es.toGPUShape(bs.createColorQuad(1, 0, 0))

    # Creating a single enemy shot
    enemyShot = sg.SceneGraphNode("enemyShot")
    enemyShot.transform = tr.matmul([tr.translate(enemyShip.pos_x, enemyShip.pos_y, 0), tr.scale(0.1, 0.3, 0), tr.uniformScale(0.2)])
    enemyShot.childs += [gpuRedQuad]

    enemyShots = sg.SceneGraphNode("enemyShots")
    enemyShots.childs += [enemyShot]
    enemyShots.pos_x = enemyShip.pos_x
    enemyShots.pos_y = enemyShip.pos_y

    return enemyShots


# Number of enemy ships
N = int(sys.argv[1])

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
    pipelineGameOver = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Creating shapes on GPU memory
    ship = createShip()
    enemyShip = createEnemyShip()
    shot = createShot()
    enemyShot = createEnemyShot()

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

    gpuGameOver = es.toGPUShape(bs.createTextureQuad("gameover.png"), GL_REPEAT, GL_NEAREST)
    gpuGameOverTransform = tr.matmul([tr.uniformScale(1.9)])

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()

    # Number of times the user ship is hit by the enemy shots
    tirosAlUsuario = 0
    # Number of times the enemy ship is hit by the shots of the user ship
    tirosAlEnemigo = 0

    while not glfw.window_should_close(window):
        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # If the buttons for the movement of the ship are pressed, the position of the ship updates
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS or glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            ship.pos_x = controller.x
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS or glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            ship.pos_y = controller.y

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the scene for the planets and the stars
        for redPlanet in redPlanets:
            redPlanet.transform = tr.translate(0, redPlanet.pos_y, 0)
            if redPlanet.pos_y > -3:
                redPlanet.pos_y -= dt
            else:
                redPlanet.pos_y = 2
                redPlanet.pos_y -= dt
            sg.drawSceneGraphNode(redPlanet, pipeline, "transform")

        for greenPlanet in greenPlanets:
            greenPlanet.transform = tr.translate(0, greenPlanet.pos_y, 0)
            if greenPlanet.pos_y > -3:
                greenPlanet.pos_y -= dt
            else:
                greenPlanet.pos_y = 2
                greenPlanet.pos_y -= dt
            sg.drawSceneGraphNode(greenPlanet, pipeline, "transform")

        for bluePlanet in bluePlanets:
            bluePlanet.transform = tr.translate(0, bluePlanet.pos_y, 0)
            if bluePlanet.pos_y > -3:
                bluePlanet.pos_y -= dt
            else:
                bluePlanet.pos_y = 2
                bluePlanet.pos_y -= dt
            sg.drawSceneGraphNode(bluePlanet, pipeline, "transform")

        for star in stars:
            star.transform = tr.translate(0, star.pos_y, 0)
            if star.pos_y > -3:
                star.pos_y -= dt
            else:
                star.pos_y = 2
                star.pos_y -= dt
            sg.drawSceneGraphNode(star, pipeline, "transform")

        # If space is pressed, the ship shoots
        if tirosAlUsuario <= 4:
            if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS or controller.shoot:
                if shot.pos_y <= 1:
                    shot.transform = tr.translate(shot.pos_x, shot.pos_y, 0)
                    shot.pos_y += 3 * dt
                    sg.drawSceneGraphNode(shot, pipeline, "transform")
                else:
                    shot.pos_x = ship.pos_x
                    shot.pos_y = ship.pos_y - 0.8
                    controller.shoot = not controller.shoot
            else:
                shot.pos_x = ship.pos_x
                shot.pos_y = ship.pos_y - 0.8
        else:
            # Game Over animation
            glUseProgram(pipelineGameOver.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipelineGameOver.shaderProgram, "transform"), 1, GL_TRUE, gpuGameOverTransform)
            pipelineGameOver.drawShape(gpuGameOver)

        # When the enemy ship appears, it stars shooting
        if enemyShot.pos_y > -3 and enemyShot.pos_y < -1.2:
            enemyShot.transform = tr.translate(enemyShot.pos_x, enemyShot.pos_y, 0)
            enemyShot.pos_y -= 4 * dt
            sg.drawSceneGraphNode(enemyShot, pipeline, "transform")
        elif enemyShot.pos_y <= -2 or enemyShot.pos_y >= -1.2:
            enemyShot.pos_x = enemyShip.pos_x - 1
            enemyShot.pos_y = enemyShip.pos_y

        # The ship is always moving as the controller
        ship.transform = tr.translate(controller.x, controller.y, 0)

        # Counter for the shoots that hit in the enemy ships, if it is equal to N, there are no more respawns
        if tirosAlEnemigo < N:
            if abs(shot.pos_x - sg.findPosition(enemyShip, "enemyShip")[0][0]) < 0.08 \
                    and abs(shot.pos_y - sg.findPosition(enemyShip, "enemyShip")[1][0]) < 0.08:
                enemyShip.transform = tr.translate(0, 1, 0)
                enemyShip.pos_y = 1
                tirosAlEnemigo += 1
            else:
                if enemyShip.pos_y > -1.2:
                    enemyShip.transform = tr.translate(enemyShip.pos_x, enemyShip.pos_y, 0)
                    enemyShip.pos_x = np.cos(t0)
                    enemyShip.pos_y -= dt
                else:
                    enemyShip.transform = tr.translate(enemyShip.pos_x, -1.2, 0)
                    enemyShip.pos_x = np.cos(t0)
                sg.drawSceneGraphNode(enemyShip, pipeline, "transform")


        # If the user ship is hit 3 times, it disappears
        # (The limit is 4 because due to the velocity of the enemy shot, sometimes the hit counts by two when it is
        # supposed to count by one)
        if tirosAlUsuario <= 4:
            if abs(sg.findPosition(enemyShot, "enemyShot")[0][0] - sg.findPosition(ship, "ship")[0][0]) < 0.08 \
                    and abs(sg.findPosition(enemyShot, "enemyShot")[1][0] - sg.findPosition(ship, "ship")[1][0]) < 0.08:
                ship.transform = tr.translate(0, -1, 0)
                tirosAlUsuario += 1
            sg.drawSceneGraphNode(ship, pipeline, "transform")

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
