import random
import pygame as pg

# A dictionary that counts the total amount of each value and color isn't needed, 
# since it's highly unlikely that the same card, value and color, be chosen 8 times in the same game.

# Instead, random generators are used, from 0-3 and 1-13, one to decide the color and another to decide the value during runtime.
# a dict can be used as a selector for the textual name of the chosen card though:

Values = {
    1: "Ace of ",
    2: "Two of ",
    3: "Three of ",
    4: "Four of ",
    5: "Five of ",
    6: "Six of ",
    7: "Seven of ",
    8: "Eight of ",
    9: "Nine of ",
    10: "Ten of ",
    11: "Jack of ",
    12: "Queen of ",
    13: "King of"
}

Colors = {
    0: "Hearts",
    1: "Diamonds",
    2: "Spades",
    3: "Clubs"
}

class Player(object):
    def __init__(self, name: str) -> None:
        self.name : str = name
        self.Hand : list[tuple[int, str, pg.Surface]] = []
        self.In = True
        self.Total : int = 0
        self.Money : int = 0
        self.Bet : int = 0
        self.parent : Player = None
        self.BlackJack : bool = False
        self.Double : bool = False
    
    def isIn(self):
        return self.In

    def stand(self):
        self.In = False

    def drawCard(self):
        Value = random.randint(1, 13)
        Color = random.randint(0, 3)
        Name = Values[Value] + Colors[Color]
        path = Colors[Color]+"-"+str(Value)+".png"
        Card = pg.image.load("images/"+path)
        
        self.Hand.append((Value, Name, Card))

        self.calcTotal()
    
    def calcTotal(self):
        tot = 0
        for Value, _, _ in self.Hand:
            if Value > 10:
                tot += 10
            elif Value == 1 and self.Total < 12:
                tot += 11
            elif self.Hand[0][0] == 1 and self.Hand[1][0] == 1 and len(self.Hand) == 2:
                tot = 12
            else: 
                tot += Value
        
        self.Total = tot
    
    def checkStatus(self) -> str:
        if self.Total == 21 and len(self.Hand) == 2:
            return "{} BLACKJACK".format(self.name)
        elif self.Total > 21:
            self.In = False
            return "{} LOST".format(self.name)
        else:
            return "STILL IN"
    
    def emptyHand(self):
        self.Hand = []
        self.Total = 0

    def increaseBet(self, num: int):
        self.Bet += num

    def decreaseBet(self, num: int):
        self.Bet -= num

    def increaseMoney(self, num: int):
        self.Money += num
    
    def decreaseMoney(self, num: int):
        self.Money -= num