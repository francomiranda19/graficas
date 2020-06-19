import numpy as np

# Problem setup
H = 4
W = 3
L = 6
h = 0.1

# Boundary Dirichlet conditions
AMBIENT_TEMPERATURE = 25
WINDOW_LOSS = 0.01
HEATER_A = 5
HEATER_B = 30

# Number of unknowns
nh = int(H / h) - 1
nw = int(W / h) - 1
nl = int(L / h) - 1

# In this case, the domain is a parallelepiped
N = nh * nw * nl

# We define a function to convert the indices from i, j to k and viceversa
# i, j, k indexes the discrete domain in 3D
# m parametrize those i, j, k, this way we can tidy the unknowns
# in a column vector and use the standard algebra

def getM(i, j, k):
    return i + j * nw + nw * nl * k

def getIJK(m):
    i = m % nw
    k = m % (nw * nl)
    j = m // nw - nl * k
    return (i, j, k)

# In this matrix we will write all the coefficients of the unknowns
A = np.zeros((N, N))
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
            m_near = getM(i, j, k - 1)
            m_far = getM(i, j, k + 1)

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
            elif 1 <= i and i <= nw - 2 and 1 <= j and j <= nl - 2 and k == 0:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE

            # Far face FALTA
            elif 1 <= i and i <= nw - 2 and 1 <= j and j <= nl - 2 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = 0

            # Down face
            elif 1 <= i and i <= nw - 2 and j == 0 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -WINDOW_LOSS

            # Up face
            elif 1 <= i and i <= nw - 2 and j == nl - 1 and 1 <= k and k <= nh - 2:
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -WINDOW_LOSS

            # Left face
            elif i == 0 and 1 <= j and j <= nl - 2 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -WINDOW_LOSS

            # Right face
            elif i == nw - 1 and 1 <= j and j <= nl - 2 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -WINDOW_LOSS

            # Down near edge
            elif 1 <= i and i <= nw - 2 and j == 0 and k == 0:
                A[m, m_up] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - WINDOW_LOSS

            # Up near edge
            elif 1 <= i and i <= nw - 2 and j == nl - 1 and k == 0:
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - WINDOW_LOSS

            # Left near edge
            elif i == 0 and 1 <= j and j <= nl - 2 and k == 0:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - WINDOW_LOSS

            # Right near edge
            elif i == nw - 1 and 1 <= j and j <= nl - 2 and k == 0:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - WINDOW_LOSS

            # Down far edge
            elif 1 <= i and i <= nw - 2 and j == 0 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -WINDOW_LOSS

            # Up far edge
            elif 1 <= i and i <= nw - 2 and j == nl - 1 and k == nh - 1:
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -WINDOW_LOSS

            # Left far edge
            elif i == 0 and 1 <= j and j <= nl - 2 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -WINDOW_LOSS

            # Right far edge
            elif i == nw - 1 and 1 <= j and j <= nl - 2 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -WINDOW_LOSS

            # Down left corner edge
            elif i == 0 and j == 0 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -2 * WINDOW_LOSS

            # Down right corner edge
            elif i == nw - 1 and j == 0 and 1 <= k and k <= nh - 2:
                A[m, m_up] = 1
                A[m, m_left] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -2 * WINDOW_LOSS

            # Up left corner edge
            elif i == 0 and j == nl - 1 and 1 <= k and k <= nh - 2:
                A[m, m_down] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -2 * WINDOW_LOSS

            # Up right corner edge
            elif i == nw - 1 and j == nl - 1 and 1 <= k and k <= nh - 2:
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_near] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -2 * WINDOW_LOSS

            # Down left near corner
            elif i == 0 and j == 0 and k == 0:
                A[m, m_up] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - 2 * WINDOW_LOSS

            # Down right near corner
            elif i == nw - 1 and j == 0 and k == 0:
                A[m, m_up] = 1
                A[m, m_left] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - 2 * WINDOW_LOSS

            # Up left near corner
            elif i == 0 and j == nl - 1 and k == 0:
                A[m, m_down] = 1
                A[m, m_right] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - 2 * WINDOW_LOSS

            # Up right near corner
            elif i == nw - 1 and j == nl - 1 and k == 0:
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_far] = 1
                A[m, m] = -6
                b[m] = -AMBIENT_TEMPERATURE - 2 * WINDOW_LOSS

            # Down left far corner
            elif i == 0 and j == 0 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -2 * WINDOW_LOSS

            # Down right far corner
            elif i == nw - 1 and j == 0 and k == nh - 1:
                A[m, m_up] = 1
                A[m, m_left] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -2 * WINDOW_LOSS

            # Up left far corner
            elif i == 0 and j == nl - 1 and k == nh - 1:
                A[m, m_down] = 1
                A[m, m_right] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -2 * WINDOW_LOSS

            # Up right far corner
            elif i == nw - 1 and j == nl - 1 and k == nh - 1:
                A[m, m_down] = 1
                A[m, m_left] = 1
                A[m, m_near] = 1
                A[m, m] = -6
                b[m] = -2 * WINDOW_LOSS
