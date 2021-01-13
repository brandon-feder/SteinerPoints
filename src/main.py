import numpy as np
from numba import jit

from settings import *
from graghics import Graghics
from MST import *
from gradient_descent import *

def getNodes(cities, MAX_SUBSTATIONS):
    # Represents the multivariable function that will be optimized
    def f(S):
        nodes = np.concatenate((cities, S))
        return calcMST(nodes)[1]

    # Stores the best sum, forest, and substation locations found
    best_sum = None
    best_res = None
    best_forest = None

    # Get the min and max of the cities ( acts as a range to bound search for optimal substations )
    m = ( min(cities[0:len(cities)-1:2]), min(cities[1:len(cities):2]))
    M = ( max(cities[0:len(cities)-1:2]), max(cities[1:len(cities):2]))

    # For every number of substations to look for
    for nSubs in range(MAX_SUBSTATIONS+1):
        # initialize the empty array that will contain the starting cordinate for the gradient gradient descent
        start = np.ndarray((nSubs * 2,), dtype=np.float32)

        # Create a random cordinate the min and the max to input into the gradient descent
        for i in range(nSubs * 2):
            a = m[0] if i % 2 == 0 else m[1]
            r = ( M[0] - m[0] ) if i % 2 == 0 else ( M[1] - m[1] )

            start[i] = a + r*np.random.random()

        # Perform the gradient descent
            # res represents the cordinates of the substations
        res = gradient_descent(f, start)

        # Get more info about the cordinates of the substations found
        nodes = np.concatenate((cities, res))
        forest, sum = calcMST(nodes)

        sum = round(sum*SUM_ROUND_AMT)/SUM_ROUND_AMT

        # Update the best substation config found if needed
        if best_sum == None or sum < best_sum:
            best_sum = sum
            best_res = res
            best_forest = forest

    # Return the optimal substation configuration found
    return best_res, best_forest, best_sum

# Initialize pygame and the graghics class
Graghics.init()

# Start the loop for the visualization
Graghics.run(getNodes)

# Quit pygame
Graghics.quit()
