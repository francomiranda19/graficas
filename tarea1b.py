import numpy as np
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import transformations as tr
import random

if __name__ == "__main__":

    import glfw
    from OpenGL.GL import *
    import OpenGL.GL.shaders
    import numpy as np
    import transformations as tr
    import sys

    # We will use 32 bits data, so an integer has 4 bytes
    # 1 byte = 8 bits
    INT_BYTES = 4

    # A class to store the application control
    class Controller:
        def __init__(self):
            self.x = 0.0
            self.y = 0.0
            self.theta = 0.0
            self.rotate = False
            self.fillPolygon = True

        def reset(self):
            self.x = 0.0
            self.y = 0.0
            self.theta = 0.0
            self.rotate = False
            self.fillPolygon = True

    controller = Controller()

    def on_key(window, key, scancode, action, mods):
        global controller

        # Keep pressed buttons
        if action == glfw.REPEAT or action == glfw.PRESS:
            if key == glfw.KEY_A:
                controller.x -= 0.1
            elif key == glfw.KEY_D:
                controller.x += 0.1
            elif key == glfw.KEY_W:
                controller.y += 0.1
            elif key == glfw.KEY_S:
                controller.y -= 0.1

        if action != glfw.PRESS:
            return

        if key == glfw.KEY_SPACE:
            controller.rotate = not controller.rotate

        elif key == glfw.KEY_1:
            controller.fillPolygon = not controller.fillPolygon

        elif key == glfw.KEY_ESCAPE:
            sys.exit()

        else:
            print('Unknown key')

    # GPUShape
    class GPUShape:
        def __init__(self):
            self.vao = 0
            self.vbo = 0
            self.ebo = 0
            self.texture = 0
            self.size = 0

    def drawShape(shaderProgram, shape, transform):

        # Binding the proper buffers
        glBindVertexArray(shape.vao)
        glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

        # updating the new transform attribute
        glUniformMatrix4fv(glGetUniformLocation(shaderProgram, "transform"), 1, GL_TRUE, transform)

        # Describing how the data is stored in the VBO
        position = glGetAttribLocation(shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # This line tells the active shader program to render the active element buffer with the given size
        glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)

    def opacidad(cf, alpha):
        return alpha * np.array(cf) + (1 - alpha) * np.array([0, 0, 0])

    def createFigure(R, N, color, alpha = 1):
        color_nuevo = opacidad(color, alpha)
        dphi = (2 * np.pi) / N
        # Here the new shape will be stored
        gpuShape = GPUShape()

        # Defining locations and colors for each vertex of the shape

        vertexData = np.zeros(N * 6, dtype=np.float32)
        l = 0;
        m = 0
        for i in range(len(vertexData)):
            if i % 6 == 0:
                vertexData[i] = R * np.cos(np.pi / N + l * dphi)
                l += 1
            elif i % 6 == 1:
                vertexData[i] = R * np.sin(np.pi / N + m * dphi)
                m += 1
            elif i % 6 == 2:
                vertexData[i] = 0.0
            elif i % 6 == 3:
                vertexData[i] = color_nuevo[0]
            elif i % 6 == 4:
                vertexData[i] = color_nuevo[1]
            elif i % 6 == 5:
                vertexData[i] = color_nuevo[2]

        # Defining connections among vertices
        # We have a triangle every 3 indices specified
        indices = np.zeros((N - 2) * 3, dtype=np.uint32)
        n = 1;
        k = 2
        for i in range(len(indices)):
            if i % 3 == 1:
                indices[i] = n
                n += 1
            elif i % 3 == 2:
                indices[i] = k
                k += 1

        gpuShape.size = len(indices)

        # VAO, VBO and EBO and  for the shape
        gpuShape.vao = glGenVertexArrays(1)
        gpuShape.vbo = glGenBuffers(1)
        gpuShape.ebo = glGenBuffers(1)

        # Vertex data must be attached to a Vertex Buffer Object (VBO)
        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertexData) * 4, vertexData, GL_STATIC_DRAW)

        # Connections among vertices are stored in the Elements Buffer Object (EBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * 4, indices, GL_STATIC_DRAW)

        return gpuShape

    # Definición del main:
    def main():
        # Initialize glfw
        if not glfw.init():
            sys.exit()

        width = 600
        height = 600

        window = glfw.create_window(width, height, "Space Wars", None, None)

        if not window:
            glfw.terminate()
            sys.exit()

        glfw.make_context_current(window)

        # Connecting the callback function 'on_key' to handle keyboard events
        glfw.set_key_callback(window, on_key)

        # Defining shaders for our pipeline
        vertex_shader = """
        #version 130
        in vec3 position;
        in vec3 color;

        out vec3 fragColor;

        uniform mat4 transform;

        void main()
        {
            fragColor = color;
            gl_Position = transform * vec4(position, 1.0f);
        }
        """

        fragment_shader = """
        #version 130

        in vec3 fragColor;
        out vec4 outColor;

        void main()
        {
            outColor = vec4(fragColor, 1.0f);
        }
        """

        # Assembling the shader program (pipeline) with both shaders
        shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        # Telling OpenGL to use our shader program
        glUseProgram(shaderProgram)

        # Setting up the clear screen color
        glClearColor(0, 0, 0, 1.0)

        # Creating shapes on GPU memory
        planetaRojo = createFigure(1/40, 20, [1, 0, 0], 0.4)
        planetaAzul = createFigure(1/40, 20, [0, 0, 1], 0.4)
        planetaVerde = createFigure(1/40, 20, [0, 1, 0], 0.4)
        estrella = createFigure(1/80, 20, [1, 1, 1])

        # Fill mode Polygon
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Get initial time
        t0 = glfw.get_time()

        x0 = random.uniform(-1.0, 1.0); y0 = random.uniform(-1.0, 1.0)

        while not glfw.window_should_close(window):
            # Getting the time difference from the previous iteration
            t1 = glfw.get_time()
            dt = t1 - t0
            t0 = t1

            # Using GLFW to check for input events
            glfw.poll_events()

            # Filling or not the shapes depending on the controller state
            if controller.fillPolygon:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

            # Clearing the screen in both, color and depth
            glClear(GL_COLOR_BUFFER_BIT)

            # theta is modified an amount proportional to the time spent in a loop iteration
            if controller.rotate:
                controller.theta += dt

            # Create transform matrix

            transform_planeta_rojo = tr.matmul([
                tr.translate(0.0, -t0, 0.0),
                tr.translate(0.1, 0.1, 0.0),
                tr.translate(0.5, 0.5, 0.0)
            ])

            transform_planeta_azul = tr.matmul([
                tr.translate(0.0, -t0, 0.0),
                tr.translate(-0.3, 0.2, 0.0),
                tr.translate(-0.5, -0.5, 0.0)
            ])

            transform_planeta_verde = tr.matmul([
                tr.translate(0.0, -t0, 0.0),
                tr.translate(0.6, -0.2, 0.0),
                tr.translate(-0.5, 0.5, 0.0)
            ])

            transform_estrella = tr.matmul([
                tr.translate(0.0, -t0, 0.0),
                tr.translate(0.3, 0.1, 0.0),
                tr.translate(0.5, -0.5, 0.0)
            ])

            listaShapes = [planetaRojo, planetaAzul, planetaVerde, estrella]
            listaTransformaciones = [transform_planeta_rojo, transform_planeta_azul, transform_planeta_verde, transform_estrella]

            drawShape(shaderProgram, planetaRojo, transform_planeta_rojo)
            drawShape(shaderProgram, planetaRojo, tr.matmul([tr.translate(0.3, -0.6, 0.0), transform_planeta_rojo]))
            drawShape(shaderProgram, planetaRojo, tr.matmul([tr.translate(-0.9, -0.8, 0.0), transform_planeta_rojo]))

            drawShape(shaderProgram, planetaAzul, transform_planeta_azul)
            drawShape(shaderProgram, planetaAzul, tr.matmul([tr.translate(0.4, 0.5, 0.0), transform_planeta_azul]))
            drawShape(shaderProgram, planetaAzul, tr.matmul([tr.translate(0.9, -0.2, 0.0), transform_planeta_azul]))

            drawShape(shaderProgram, planetaVerde, transform_planeta_verde)
            drawShape(shaderProgram, planetaVerde, tr.matmul([tr.translate(0.5, -0.7, 0.0), transform_planeta_verde]))
            drawShape(shaderProgram, planetaVerde, tr.matmul([tr.translate(-0.8, 0.6, 0.0), transform_planeta_verde]))

            drawShape(shaderProgram, estrella, transform_estrella)
            drawShape(shaderProgram, estrella, tr.matmul([tr.translate(-0.3, 0.6, 0.0), transform_estrella]))
            drawShape(shaderProgram, estrella, tr.matmul([tr.translate(0.6, -0.2, 0.0), transform_estrella]))
            drawShape(shaderProgram, estrella, tr.matmul([tr.translate(0.5, -0.8, 0.0), transform_estrella]))
            drawShape(shaderProgram, estrella, tr.matmul([tr.translate(0.2, -0.7, 0.0), transform_estrella]))
            drawShape(shaderProgram, estrella, tr.matmul([tr.translate(-0.1, -0.4, 0.0), transform_estrella]))
            drawShape(shaderProgram, estrella, tr.matmul([tr.translate(-0.2, -0.2, 0.0), transform_estrella]))
            drawShape(shaderProgram, estrella, tr.matmul([tr.translate(-0.6, -0.3, 0.0), transform_estrella]))
            drawShape(shaderProgram, estrella, tr.matmul([tr.translate(-0.2, -0.5, 0.0), transform_estrella]))

            if y0 - t0 <= -3.0:
                glfw.set_time(0.0)
                y0 = 3.0

            # Once the render is done, buffers are swapped, showing only the complete scene.
            glfw.swap_buffers(window)

        glfw.terminate()

    controller.reset()
    main()