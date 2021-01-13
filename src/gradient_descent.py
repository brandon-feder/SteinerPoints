import numpy as np

from settings import *

# Performs a gradient descent on the multibariable function f starting from point a
def gradient_descent(f, a):
    # For every optimization iteration
    for i in range(MAX_OPTIMIZATION_ITERATIONS):
        # Stores the local gradient that will be calculated
        D_f = np.ndarray(a.shape, dtype=np.float64)

        # Calculate the multidemensional gradient around cordinate a
        for dim in range(len(a)):
            b1 = np.copy(a)
            b2 = np.copy(a)

            b1[dim] += EPSILON/2.0
            b2[dim] -= EPSILON/2.0

            D_f[dim] = (f(b1) - f(b2))/EPSILON

        # calculate the new cordinate of a using the calculate gradient
        a = a - ALPHA * D_f

    # Return the optimal point found
    return a
