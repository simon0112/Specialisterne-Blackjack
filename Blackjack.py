import sys
import pygame as pg
from pygame.locals import *
import StateMachine as SM

pg.init()

#Game clock
FPS = pg.time.Clock()
FPS.tick(60)

# initialize state machine
statemachine = SM.StateMachine()
statemachine.startup()

#Game Loop
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        else:
            statemachine.handleEvent(event)

    statemachine.drawState()