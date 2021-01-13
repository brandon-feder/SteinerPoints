import pygame
import numpy as np

from settings import *

class Graghics:
    # Contains the main pygame surface object
    __screen = None
    __bestSum = None
    __bestSubstations = None
    __bestEdgeList = None

    # Initializes pygame
    @staticmethod
    def init():
        pygame.init()
        Graghics.__screen = pygame.display.set_mode([CANVAS_HEIGHT, CANVAS_WIDTH])

    # Main graghical loop
    @staticmethod
    def run(getNodes):
        # # of substations to look for
        MAX_SUBSTATIONS = 1

        # Initial city config
        cities = np.array([0, 0, 0, 2, 1, 0, 1, 2], dtype=np.float32)

        # User input vars
        DRAGING = False
        DRAG_OFFSET = None
        DRAGED_CITY = -1

        # Flag that tells whether loop is running or not
        running = True
        while running:

            # Handle events
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    running = False

                # Right click down event
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    city_indx = Graghics.__onCity(cities)
                    if city_indx >= 0:
                        cities = np.delete(cities, [2*city_indx, 2*city_indx+1])
                    else:
                        mousePos = pygame.mouse.get_pos()
                        cities = np.append(cities, Graghics.__fromPygameCord(mousePos[0], mousePos[1]))
                    Graghics.__bestSum = None

                # Left click down event
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    city_indx = Graghics.__onCity(cities)
                    if city_indx >= 0:
                        DRAGING = True
                        mX, mY = pygame.mouse.get_pos()
                        mX, mY = Graghics.__fromPygameCord(mX, mY)
                        cX, cY = cities[2*city_indx], cities[2*city_indx+1]

                        DRAG_OFFSET = (cX - mX, cY - mY)
                        DRAGED_CITY = city_indx
                        Graghics.__bestSum = None

                # Left click up event
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    DRAGING = False

                # up and down arrow events
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        MAX_SUBSTATIONS += 1
                    else:
                        event.key == pygame.K_DOWN
                        MAX_SUBSTATIONS = max(0, MAX_SUBSTATIONS - 1)
                    Graghics.__bestSum = None

            # Do stuff if the user is draging a city
            if DRAGING:
                mX, mY = pygame.mouse.get_pos()
                mX, mY = Graghics.__fromPygameCord(mX, mY)
                cities[2*DRAGED_CITY] = mX + DRAG_OFFSET[0]
                cities[2*DRAGED_CITY+1] = mY + DRAG_OFFSET[1]
                Graghics.__bestSum = None

            # Fill the background with white
            Graghics.__screen.fill((255, 255, 255))

            # Get cities and substations
            substations, edge_list, sum = getNodes(cities, MAX_SUBSTATIONS)

            # Update the best configuration found if needed
            if Graghics.__bestSum == None or Graghics.__bestSum > sum or ( Graghics.__bestSum == sum and len(Graghics.__bestSubstations) > len(substations) ):
                Graghics.__bestSum = sum
                Graghics.__bestEdgeList = edge_list
                Graghics.__bestSubstations = substations
            elif Graghics.__bestSum < sum or ( Graghics.__bestSum == sum and len(Graghics.__bestSubstations) < len(substations) ):
                sum = Graghics.__bestSum
                edge_list = Graghics.__bestEdgeList
                substations = Graghics.__bestSubstations

            # concatenate
            nodes = np.concatenate((cities, substations))

            for edge in edge_list:
                c1 = Graghics.__toPygameCord(nodes[2*int(edge[0])], nodes[2*int(edge[0])+1])
                c2 = Graghics.__toPygameCord(nodes[2*int(edge[1])], nodes[2*int(edge[1])+1])

                pygame.draw.line(Graghics.__screen, LINE_COLOR, c1, c2)

            # Render cities
            for i in range(len(cities)//2):
                pygame.draw.circle(
                    Graghics.__screen,
                    CITY_COLOR,
                    Graghics.__toPygameCord(cities[2*i], cities[2*i+1]),
                    CITY_RADIUS
                )

            # Render substations
            for i in range(len(substations)//2):
                pygame.draw.circle(
                    Graghics.__screen,
                    SUBSTATION_COLOR,
                    Graghics.__toPygameCord(substations[2*i], substations[2*i+1]),
                    SUBSTATION_RADIUS
                )

            # Create new surface with fonts
            info_font_A = pygame.font.SysFont('Comic Sans', 30)
            info_font_B = pygame.font.SysFont('Comic Sans', 30)
            info_font_C = pygame.font.SysFont('Comic Sans', 30)
            info_font_D = pygame.font.SysFont('Comic Sans', 30)
            textsurface_A = info_font_A.render('# Cities: ' + str(len(cities)//2), False, (0, 0, 0))
            textsurface_B = info_font_B.render('# Substations: ' + str(len(substations)//2), False, (0, 0, 0))
            textsurface_C = info_font_C.render('Total Length: ' + str(sum), False, (0, 0, 0))
            textsurface_D = info_font_D.render('Max # Substations: ' + str(MAX_SUBSTATIONS), False, (0, 0, 0))

            # Blit font surface to screen
            Graghics.__screen.blit(textsurface_A, (10, 10))
            Graghics.__screen.blit(textsurface_B, (10, 40))
            Graghics.__screen.blit(textsurface_C, (10, 70))
            Graghics.__screen.blit(textsurface_D, (10, 100))

            for i in range(len(nodes)//2):
                id_font = pygame.font.SysFont('Comic Sans', 30)
                surface_font = id_font.render(str(i), False, (50, 50, 50))
                Graghics.__screen.blit(surface_font, Graghics.__toPygameCord(nodes[2*i], nodes[2*i+1]))

            # Flip the display
            pygame.display.flip()

    # Quit pygame
    @staticmethod
    def quit():
        pygame.quit()

    # Maps pygame cords to "better" cordinates
    @staticmethod
    def __toPygameCord(x, y):
        return (
            SCALE*x+CANVAS_WIDTH//2,
            SCALE*y+CANVAS_HEIGHT//2
        )

    @staticmethod
    def __fromPygameCord(x, y):
        return (
            (x-CANVAS_WIDTH//2)/SCALE,
            (y-CANVAS_HEIGHT//2)/SCALE
        )

    # Get whether the user is on a city
    @staticmethod
    def __onCity(cities):
        mX, mY = pygame.mouse.get_pos()
        for i in range(len(cities)//2):
            cX, cY = Graghics.__toPygameCord(cities[2*i], cities[2*i+1])
            dist = ( (mX-cX)**2 + (mY-cY)**2 )**0.5

            if dist <= CITY_RADIUS:
                return i

        return -1
