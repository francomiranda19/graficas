import numpy as np
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D

def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T

def catmullRomMatrix(P1, P2, P3, P4):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, P3, P4), axis = 1)

    # Catmull-Rom base matrix is a constant
    Mcr = 1 / 2 * np.array([[0, -1, 2, -1], [2, 0, -5, 3], [0, 1, 4, -3], [0, 0, -1, 1]])

    return np.matmul(G, Mcr)

# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T
        
    return curve