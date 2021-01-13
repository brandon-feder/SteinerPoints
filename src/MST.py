import numpy as np
from numba import jit

from settings import *

# Performs Prim's algorythm to find MST
@jit(nopython=True, parallel=True)
def calcMST(nodes):

    # Helper function to calculate distance between two points
    def dist(i, j, N):
        x1 = N[2*i]
        x2 = N[2*j]
        y1 = N[2*i+1]
        y2 = N[2*j+1]

        return ( (x2 - x1)**2 + (y2 - y1)**2 )**0.5

    # Get the number of total edges that will be searched through
    nEdges = 0
    for i in range(len(nodes)//2):
        for _ in range(i+1, len(nodes)//2):
            nEdges += 1

    # Will store the unfiltered edges, the forest found, and whether a given nodes is in a forest respectively
    edges = np.zeros((nEdges, 3), dtype=np.float32)
    forest = np.zeros((len(nodes)//2-1, 3), dtype=np.float32)
    isInForest = np.full((len(nodes)//2,), False)

    # Get all combinations of 2 edges
    indx = 0
    for i in range(len(nodes)//2):
        for j in range(i+1, len(nodes)//2):
            edges[indx] = np.array([ i, j, dist(i, j, nodes) ], dtype=np.float32)
            indx += 1

    # Add the first node to the forest
    isInForest[0] = True

    # Get the indecies that would sort the edges from least to most distance
    ind = np.argsort(edges[:,2])

    forest_indx = 0
    sum = 0

    # For the # of edges that are needed
    for _ in range(len(nodes)-1):

        # For each edge in the "sorted" array
        for e in ind:

            # Get the current edge and its corresponding vertecies
            edge = edges[e]
            u, v = int(edge[0]), int(edge[1])

            # Add the edge to the forest if needed
            if isInForest[u] != isInForest[v]:
                if isInForest[u]:
                    isInForest[v] = True
                else:
                    isInForest[u] = True

                forest[forest_indx] = np.array([u, v, edge[2]], dtype=np.float32)
                forest_indx += 1

                # Update the distance sum
                sum += edge[2]

                break

    # Return the forest and sum of that forest
    return forest, sum
