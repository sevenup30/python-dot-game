import pygame as pg
import dots
import random
import spicies
import copy
import time
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
TEXTCOLOR = (0,   0,  0)


(width, height) = (800, 800)
dotStartPos = (int(width/2), height - 100)
spiciesPopulationNumber = 100
currentSpicies = []
window = pg.display.set_mode((width, height))
newSpicies = []
minStep = 1000
spiciescount = 1
running = True
goalPos = (int(width/2), 0)
dotssprite = pg.sprite.Group()
alldotsaredead = False


def main():
    global running, window, currentSpicies, dotssprite, spiciescount, FONT, alldotsaredead
    
    pg.init()
    FONT = pg.font.Font("freesansbold.ttf", 15)

    window.fill(WHITE)
    clock = pg.time.Clock()
    pg.display.update()
    currentSpicies = spicies.Spicies(spiciesPopulationNumber, dotStartPos, window, spiciescount, minStep)
    [dotssprite.add(d) for d in currentSpicies.population]
    pg.draw.circle(window, RED, goalPos, 5)
    dotssprite.draw(window)
    text_count_surf = FONT.render("spicies number : " + str(spiciescount), True, BLACK)
    text_count_rect = text_count_surf.get_rect(center=(60, 30))
    window.blit(text_count_surf, text_count_rect)
    pg.draw.line(window, BLACK, (2, 300), (600, 300), 15)
    pg.draw.line(window, BLACK, (300, 100), (800, 100), 15)
    pg.draw.line(window, BLACK, (400, 150), (400, 250), 15)
    pg.display.flip()
    surface = pg.Surface((window.get_width(), window.get_height()))
    surface.fill((255, 255, 255))
    rundots()
    while running:
        ev = pg.event.get()
        for event in ev:
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    spiciescount += 1
                    resetscreen(spiciescount)
                    mutatespicies()
        if alldotsaredead is False:
            rundots()
            alldotsaredead = currentSpicies.checkdotsalive()
            # window.blit(surface, (0, 10))
            # text_count_surf = FONT.render("spicies number : " + str(spiciescount), True, BLACK)
            # text_count_rect = text_count_surf.get_rect(center=(70, 30))
            # window.blit(text_count_surf, text_count_rect)
        else:
            spiciescount += 1
            resetscreen(spiciescount)
            mutatespicies()

        updatescreen()
        clock.tick(100)
        

def resetscreen(spiciescount):
    global dotssprite
    window.fill(WHITE)
    text_count_surf = FONT.render("spicies number : " + str(spiciescount), True, BLACK)
    text_count_rect = text_count_surf.get_rect(center=(70, 30))
    window.blit(text_count_surf, text_count_rect)
    pg.draw.circle(window, RED, goalPos, 5)
    pg.draw.line(window, BLACK, (2, 300), (600, 300), 15)
    pg.draw.line(window, BLACK, (300, 100), (800, 100), 15)
    pg.draw.line(window, BLACK, (400, 150), (400, 250), 15)
    pg.display.update()
    dotssprite.empty()


def updatescreen():
    global dotssprite
    window.fill(WHITE)
    text_count_surf = FONT.render("spicies number : " + str(spiciescount), True, BLACK)
    text_count_rect = text_count_surf.get_rect(center=(70, 30))
    window.blit(text_count_surf, text_count_rect)
    pg.draw.circle(window, RED, goalPos, 5)
    pg.draw.line(window, BLACK, (2, 300), (600, 300), 15)
    pg.draw.line(window, BLACK, (300, 100), (800, 100), 15)
    pg.draw.line(window, BLACK, (400, 150), (400, 250), 15)
    dotssprite.draw(window)
    pg.display.update()


def mutatespicies():
    global currentSpicies, dotssprite, alldotsaredead, minStep
    currentSpicies.calculfitness()
    currentSpicies.calculfitnesssum()
    bestdot = copy.copy(currentSpicies.getbestdot())
    if bestdot.reachedGoal is True:
        minStep = bestdot.brain.step
    newSpicies = spicies.Spicies(spiciesPopulationNumber, dotStartPos, window, spiciescount, minStep)

    print("newbrain")
    print(bestdot.brain.directions)

    for i in range(1, spiciesPopulationNumber):
        parent = currentSpicies.selectparent()
        newSpicies.population[i].brain = copy.deepcopy(parent.brain)
        newSpicies.population[i].brain.step = 0
        newSpicies.population[i].brain.mutate()
        newSpicies.population[i].id = str(i)+' ---- child of '+str(parent.id)
    newSpicies.population[0].isBest = True
    newSpicies.population[0].id = "BestDOT from" + str(bestdot.id)
    newSpicies.population[0].brain = copy.deepcopy(bestdot.brain)
    newSpicies.population[0].brain.step = 0
    print("newbrain", newSpicies.population[0].id)
    print(newSpicies.population[0].brain.directions)
    currentSpicies = newSpicies
    dotssprite.empty()
    [dotssprite.add(d) for d in currentSpicies.population]
    alldotsaredead = False
    for i in currentSpicies.population:
        i.drawDots()


def rundots():
    dotssprite.update()


if __name__ == '__main__':
    main()
