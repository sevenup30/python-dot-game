import pygame as pg
import dots
import random
import time

class Spicies():

    def __init__(self, nb, dotStartingPos, window, id, step):
        self.population = self.populatespicies(nb, dotStartingPos, window, step)
        self.fitnesssum = 0
        self.bestdot = None
        self.window = window
        self.populationnumber = len(self.population)
        self.dotstartingpos = dotStartingPos
        self.id = id

    def populatespicies(self, nb, dotStartingPos, window, step):
        population = []
        (x, y) = dotStartingPos
        for i in range(0, nb):
            #population.append(dots.Dots((0, 0, 0), (x+random.randrange(-10,10)), (y+random.randrange(-10,10)), 5, window, i, step))
            population.append(dots.Dots((0, 0, 0), x, y, 5, window, i, step))
            population[i].drawDots()
        return population

    def getbestdot(self):
        max = 0
        maxIndex = 0
        for i in range(self.populationnumber):
            if self.population[i].fitness > max:
                max = self.population[i].fitness
                maxIndex = i
        bestdot = self.population[maxIndex]
        return bestdot

    def checkdotsalive(self):
        for i in range(self.populationnumber):
            if self.population[i].dead is False and self.population[i].reachedGoal is False:
                return False

    def calculfitness(self):
        for i in range(0, self.populationnumber):
            self.population[i].calculatefitness()

    def calculfitnesssum(self):
        self.fitnesssum = 0
        for i in range(0, self.populationnumber):
            self.fitnesssum += self.population[i].fitness

    def selectparent(self):
        rand = random.uniform(0, self.fitnesssum)
        runningsum = 0
        for i in range(0, self.populationnumber):
            runningsum += self.population[i].fitness
            if runningsum > rand:
                return self.population[i]
        return None

    # def keeppreviousspicies(self):
    #     global previousSpicies, currentSpicies
    #     if previousSpiciesFitnessSum > currentSpiciesFitnessSum:
    #         currentSpicies = previousSpicies

