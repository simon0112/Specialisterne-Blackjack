import pygame as pg
from pygame.locals import *

class EventCaller(object):
    def __init__(self) -> None:
        pass
    




    #
    #
    # HELPER FUNCTIONS
    #
    #

    def withinBounds(self, obj1: tuple[int, int], obj2: pg.Rect):
        return obj2.collidepoint(obj1)





    #
    #
    # CALL HANDLING
    #
    #

    def menuCaller(self, event:pg.event.Event) -> str:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = pg.mouse.get_pos()

            if self.withinBounds(pos, pg.Rect(100, 50, 400, 200)):
                return "STARTGAME"
            elif self.withinBounds(pos, pg.Rect(100, 650, 400, 200)):
                return "QUIT"
            
            elif self.withinBounds(pos, pg.Rect(100, 300, 75, 50)):
                return "DECREASE100"
            elif self.withinBounds(pos, pg.Rect(100, 300, 75, 50)):
                return "DECREASE10"
            elif self.withinBounds(pos, pg.Rect(245, 300, 40, 50)):
                return "DECREASE1"
            elif self.withinBounds(pos, pg.Rect(315, 300, 40, 50)):
                return "INCREASE1"
            elif self.withinBounds(pos, pg.Rect(360, 300, 60, 50)):
                return "INCREASE10"
            elif self.withinBounds(pos, pg.Rect(425, 300, 75, 50)):
                return "INCREASE100"
            
            elif self.withinBounds(pos, pg.Rect(100, 590, 195, 50)):
                return "ADDPLAYER"
            elif self.withinBounds(pos, pg.Rect(305, 590, 195, 50)):
                return "REMPLAYER"
            
            elif self.withinBounds(pos, pg.Rect(100, 400, 400, 75)):
                return "ADDMONEY"
            
            elif self.withinBounds(pos, pg.Rect(125, 530, 50, 50)):
                return "PLAYER1"
            elif self.withinBounds(pos, pg.Rect(225, 530, 50, 50)):
                return "PLAYER2"
            elif self.withinBounds(pos, pg.Rect(325, 530, 50, 50)):
                return "PLAYER3"
            elif self.withinBounds(pos, pg.Rect(425, 530, 50, 50)):
                return "PLAYER4"

    def gameCaller(self, event:pg.event.Event) -> str:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = pg.mouse.get_pos()

            if self.withinBounds(pos, pg.Rect(105, 800, 90, 50)):
                return "HIT"
            elif self.withinBounds(pos, pg.Rect(205, 800, 90, 50)):
                return "STAND"
            elif self.withinBounds(pos, pg.Rect(305, 800, 90, 50)):
                return "DOUBLE"
            elif self.withinBounds(pos, pg.Rect(405, 800, 90, 50)):
                return "SPLIT"

    def endCaller(self, event : pg.event.Event) -> str:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = pg.mouse.get_pos()

            if self.withinBounds(pos, pg.Rect(50, 610, 500, 280)):
                return "BACK TO MENU"