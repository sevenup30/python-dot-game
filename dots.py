import pygame as pg
import brain
import math
import random
vec = pg.math.Vector2

class Dots(pg.sprite.Sprite):
    def __init__(self, color, x, y, radius, window, id, step):
        pg.sprite.Sprite.__init__(self)
        self.maxspeed = 4
        self.id = id
        self.window = window
        self.color = color
        self.x = x
        self.y = y
        self.pos = vec(self.x, self.y)
        self.radius = radius
        self.image = pg.Surface((10, 10), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.dead = False
        self.reachedGoal = False
        self.isBest = False
        self.brain = brain.Brain(step)
        self.brain.randomize()
        self.fitness = 0
        self.closestdistance = self.pos.distance_to(vec((self.window.get_width()/2), 0))

    def update(self):
        if self.dead is False and self.reachedGoal is False:
            self.getnewpos(self.brain.directions[self.brain.step][0])
            if (300 <= self.pos.y <= 315) and (2 <= self.pos.x <= 600):
                self.dead = True
            if (100 <= self.pos.y <= 115) and (300 <= self.pos.x <= 800):
                self.dead = True
            if self.pos.x < 2 or self.pos.x > self.window.get_width()-2:
                self.dead = True
            if self.pos.y > self.window.get_height() -2 or self.pos.y < 2:
                self.dead = True
            if self.closestdistance <= 10:
                self.reachedGoal = True
            if self.brain.step == self.brain.size:
                self.dead = True
            if (150 <= self.pos.y <= 250) and (400 <= self.pos.x <= 410):
                self.dead = True

        # elif self.dead is True:
        #     print("capasse")
        #     for i in range(int(self.brain.step-2), self.brain.step):
        #         self.brain.directions[i][1] = 1


        
    def getnewpos(self, angle):
        if self.vel.length() > self.maxspeed:
            self.vel.scale_to_length(self.maxspeed)
        if len(self.brain.directions) > self.brain.step:
            self.accel = [math.cos(angle), math.sin(angle)]
        else:
            self.dead = True
        self.vel += self.accel
        self.pos += self.vel
        self.rect.center = self.pos
        # self.image = pg.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        currentpos = self.pos.distance_to(vec((self.window.get_width() / 2), 0))
        if currentpos < self.closestdistance:
            self.closestdistance = currentpos
        # elif currentpos > self.closestdistance:
        #     self.brain.directions[self.brain.step][1] = 1
        self.brain.step += 1


    def drawDots(self):
        if self.isBest is True:
            pg.draw.ellipse(self.image, (0, 255, 0), [0, 0, 10, 10], 0)
        else:
            pg.draw.ellipse(self.image, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), [0, 0, 5, 5], 0)
#        pg.draw.circle(self.window, self.color, self.pos, self.radius)
#        pg.display.update()

    def calculatefitness(self):
        if self.reachedGoal is True:
            self.fitness = (1.0/16.0) + 10000.0/(self.brain.step * self.brain.step)
        else:
            finalPos = self.pos.distance_to(vec((self.window.get_width() / 2), 0))
            self.fitness = 1/(finalPos * finalPos)

