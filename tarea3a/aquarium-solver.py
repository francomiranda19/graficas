import numpy as np
import matplotlib.pyplot as mpl
import json
import sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import scipy
import scipy.sparse.linalg

setup = sys.argv[1]

with open(setup) as file:
    data = json.load(file)
    for parameter in data['parameters']:
        # Problem setup
        H = parameter['height']
        W = parameter['width']
        L = parameter['length']
        # Boundary conditions
        WINDOW_LOSS = parameter['window_loss']
        HEATER_A = parameter['heater_a']
        HEATER_B = parameter['heater_b']
        AMBIENT_TEMPERATURE = parameter['ambient_temperature']
        # Solution
        FILENAME = parameter['filename']

# Discretization step
h = 0.15

# Number of unknowns
nh = int(H // h) - 1
nw = int(W // h) - 1
nl = int(L // h) - 1

# In this case, the domain is a parallelepiped
N = nh * nw * nl

# We define a function to convert the indices from i, j to k and viceversa
# i, j, k indexes the discrete domain in 3D
# m parametrize those i, j, k, this way we can tidy the unknowns
# in a column vector and use the standard algebra

def getM(i, j, k):
    return i + j * nw + nw * nl * k

def getIJK(m):
    i = m % (nw * nl) % nw
    j = m % (nw * nl) // nw
    k = m // (nw * nl)
    return (i, j, k)

# In this matrix we will write all the coefficients of the unknowns
A = scipy.sparse.lil_matrix((N, N))
# In this vector we will write all the right side of the equations
b = np.zeros((N, ))
# Note: to write an equation is equivalent to write a row in the matrix system

# We iterate over each point inside the domain
# Each point has an equation associated
# The equation is different depending on the point location inside the domain
for i in range(nw):
    for j in range(nl):
        for k in range(nh):
            # We will write the equation associated with row m
            m = getM(i, j, k)
            # We obtain indices of the other coefficients
            m_up = getM(i, j + 1, k)
            m_down = getM(i, j - 1, k)
            m_left = getM(i - 1, j, k)
            m_right = getM(i + 1, j, k)
            m_near = getM(i, j, k + 1)
            m_far = getM(i, j, k - 1)

            # Depending on the location of the point, the equation is different
            # Interior
            if 1 <= i and i <= nw - 2 and 1 <= j and j <= nl - 2 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = 0

            # Near face
            elif 1 <= i and i <= nw - 2 and 1 <= j and j <= nl - 2 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE

            # Heater A
            elif nw // 3 <= i and i <= (2 * nw) // 3 and (3 * nl) // 5 <= j and j <= (4 * nl) // 5 and k == 0:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -HEATER_A

            # Heater B
            elif nw // 3 <= i and i <= (2 * nw) // 3 and nl // 5 <= j and j <= (2 * nl) // 5 and k == 0:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -HEATER_B

            # Far face (without heaters)
            elif 1 <= i and i <= nw - 2 and 1 <= j and j <= nl - 2 and k == 0:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = 0

            # Down face
            elif 1 <= i and i <= nw - 2 and j == 0 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 2
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = 2 * h * WINDOW_LOSS

            # Up face
            elif 1 <= i and i <= nw - 2 and j == nl - 1 and 1 <= k and k <= nh - 2:
                A[m, m_down] = 2
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -2 * h * WINDOW_LOSS

            # Left face
            elif i == 0 and 1 <= j and j <= nl - 2 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_right] = 2
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = 2 * h * WINDOW_LOSS

            # Right face
            elif i == nw - 1 and 1 <= j and j <= nl - 2 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 2
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -2 * h * WINDOW_LOSS

            # Down near edge
            elif 1 <= i and i <= nw - 2 and j == 0 and k == nh - 1:
                A[m, m_up] = 2
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE + 2 * h * WINDOW_LOSS

            # Up near edge
            elif 1 <= i and i <= nw - 2 and j == nl - 1 and k == nh - 1:
                A[m, m_down] = 2
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - 2 * h * WINDOW_LOSS

            # Left near edge
            elif i == 0 and 1 <= j and j <= nl - 2 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_right] = 2
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE + 2 * h * WINDOW_LOSS

            # Right near edge
            elif i == nw - 1 and 1 <= j and j <= nl - 2 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 2
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - 2 * h * WINDOW_LOSS

            # Down far edge
            elif 1 <= i and i <= nw - 2 and j == 0 and k == 0:
                A[m, m_up] = 2
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = 2 * h * WINDOW_LOSS

            # Up far edge
            elif 1 <= i and i <= nw - 2 and j == nl - 1 and k == 0:
                A[m, m_down] = 2
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = -2 * h * WINDOW_LOSS

            # Left far edge
            elif i == 0 and 1 <= j and j <= nl - 2 and k == 0:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_right] = 2
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = 2 * h * WINDOW_LOSS

            # Right far edge
            elif i == nw - 1 and 1 <= j and j <= nl - 2 and k == 0:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 2
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = -2 * h * WINDOW_LOSS

            # Down left corner edge
            elif i == 0 and j == 0 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 2
                A[m, m_right] = 2
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = 4 * h * WINDOW_LOSS

            # Down right corner edge
            elif i == nw - 1 and j == 0 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 2
                A[m, m_left] = 2
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = 0

            # Up left corner edge
            elif i == 0 and j == nl - 1 and 1 <= k and k <= nh - 2:
                A[m, m_down] = 2
                A[m, m_right] = 2
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = 0

            # Up right corner edge
            elif i == nw - 1 and j == nl - 1 and 1 <= k and k <= nh - 2:
                A[m, m_down] = 2
                A[m, m_left] = 2
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -4 * h * WINDOW_LOSS

            # Down left near corner
            elif i == 0 and j == 0 and k == nh - 1:
                A[m, m_up] = 2
                A[m, m_right] = 2
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE + 4 * h * WINDOW_LOSS

            # Down right near corner
            elif i == nw - 1 and j == 0 and k == nh - 1:
                A[m, m_up] = 2
                A[m, m_left] = 2
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE

            # Up left near corner
            elif i == 0 and j == nl - 1 and k == nh - 1:
                A[m, m_down] = 2
                A[m, m_right] = 2
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE

            # Up right near corner
            elif i == nw - 1 and j == nl - 1 and k == nh - 1:
                A[m, m_down] = 2
                A[m, m_left] = 2
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - 4 * h * WINDOW_LOSS

            # Down left far corner
            elif i == 0 and j == 0 and k == 0:
                A[m, m_up] = 2
                A[m, m_right] = 2
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = 4 * h * WINDOW_LOSS

            # Down right far corner
            elif i == nw - 1 and j == 0 and k == 0:
                A[m, m_up] = 2
                A[m, m_left] = 2
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = 0

            # Up left far corner
            elif i == 0 and j == nl - 1 and k == 0:
                A[m, m_down] = 2
                A[m, m_right] = 2
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = 0

            # Up right far corner
            elif i == nw - 1 and j == nl - 1 and k == 0:
                A[m, m_down] = 2
                A[m, m_left] = 2
                A[m, m_near] = 2
                A[m, m] = -6
                b[m] = -4 * h * WINDOW_LOSS

            else:
                print("Point (" + str(i) + ', ' + str(j) + ', ' + str(k) + ") missed!")
                print("Associated point index is " + str(m))
                raise Exception()

# Solving our system
x = scipy.sparse.linalg.spsolve(A, b)

# Now we return our solution to the 3D discrete domain
# In this matrix we will store the solution in the 3D domain
u = np.zeros((nw, nl, nh))

for m in range(N):
    i, j, k = getIJK(m)
    u[i, j, k] = x[m]

# Adding the borders, as they have known values
ub = np.zeros((nw + 2, nl + 2, nh + 2))
ub[1:nw + 1, 1:nl + 1, 1:nh + 1] = u[:, :, :]

# Dirichlet boundary condition
# Top
ub[0:nw + 2, 0:nl + 2, nh + 1] = AMBIENT_TEMPERATURE

# Storing our results

np.save(FILENAME, ub)

X = np.arange(0, ub.shape[0] - 2, 1, dtype = int)
Y = np.arange(0, ub.shape[1] - 2, 1, dtype = int)
Z = np.arange(0, ub.shape[2] - 2, 1, dtype = int)
X, Y, Z = np.meshgrid(X, Y, Z)

fig = mpl.figure()
ax = fig.add_subplot(111, projection = '3d')
scat = ax.scatter(Z, X, Y, c = x, marker = 'o')
fig.colorbar(scat, shrink = 0.5, aspect = 5)
ax.set_title('Aquarium temperatures')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
mpl.show()