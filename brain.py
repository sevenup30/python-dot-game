import math
import pygame as pg
import random
vec = pg.math.Vector2

class Brain:
    def __init__(self, size):
        self.size = size #Nombre d'instruction du cerveau
        self.directions = []
        self.step = 0

    def randomize(self):
        for i in range(self.size):
            randomangle = random.uniform(0, 2*math.pi)
            self.directions.append([randomangle, 0])

    def mutate(self):
        mutationRate = 0.01
        for i in range(self.size):
            rand = random.uniform(0, 1)
            if rand < mutationRate:
                randomangle = random.uniform(0, 2 * math.pi)
                self.directions[i][0] = randomangle
            # self.directions[i][1] = 0
        # for i in range(self.size):
        #     if self.directions[i][1] == 1:
        #         randomangle = random.uniform(0, 2 * math.pi)
        #         self.directions[i][0] = randomangle