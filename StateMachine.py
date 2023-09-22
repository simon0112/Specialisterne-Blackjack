import sys
import pygame as pg
import Draw as D
import EventCaller as E
import Player as P
import io


# 0: Menu
# 1: Active game
# 2: Ended game
# 10: Launch-state
class StateMachine(object):
    def __init__(self) -> None:
        self.State : int = 10
        self.Players : list[P.Player] = []
        self.Drawer : D.Draw = D.Draw()
        self.Caller : E.EventCaller = E.EventCaller()
        self.Winners : list[P.Player] = []
        self.Draws : list[P.Player] = []
        self.Losers : list[P.Player] = []
        self.Stands : int = 0
        self.turn : int = 1
        self.displayedPlayer : int = 1





    #
    #
    # HELPER FUNCTIONS
    #
    #

    def changeState(self, state: int):
        self.State = state
    
    def readState(self):
        return self.State

    def findPlayerFromName(self, name):
        for player in self.Players:
            if player.name == name:
                return player

    def startup(self):
        self.Players.append(P.Player("Dealer"))
        self.Players.append(P.Player("Player 1"))

        # different players could be split by newlines

        f = io.open("save.txt", "r")
        val = f.read()
        if val == '':
            val = 500
        else:
            val = int(val)
        f.close()

        self.Players[1].Money = val

        self.changeState(0)

    def newGame(self):
        self.Winners = []
        self.Draws = []
        self.Losers = []

        self.Stands = 0

        self.turn = 1

        for player in reversed(self.Players[1:]):
            if player.Bet > player.Money or (player.Money == 0 and player.name != "Dealer"):
                self.Players.remove(player)
            player.In = True
            player.drawCard()

        for player in self.Players:
            player.drawCard()

        self.changeState(1)

    def nextTurn(self):
        self.turn += 1
        if self.turn >= len(self.Players):
            for x in reversed(range(len(self.Players))):
                if x == 0:
                    continue
                if self.Players[x].isIn():
                    self.turn = x

        if self.Stands == len(self.Players[1:]):
            self.turn = 1

    def dealerTurn(self):
        self.turn = 1

        while self.Players[0].Total < 17:
            self.Players[0].drawCard()
            self.drawState()
            pg.time.delay(750)
            

        if self.Players[0].Total > 21:
            for player in self.Players[1:]:
                if player.Total <= 21 and self.playerNotOut(player):
                    self.Winners.append(player)
            self.Draws.clear()
            self.Losers.clear()

            self.changeState(2)

        for player in self.Players[1:]:
            if self.Players[0].Total > player.Total or player.Total > 21:
                if self.playerNotOut(player):
                    self.Losers.append(player)
            elif self.Players[0].Total == player.Total:
                if self.playerNotOut(player):
                    self.Draws.append(player)
            else:
                if self.playerNotOut(player):
                    self.Winners.append(player)

        self.changeState(2)

    def playerNotOut(self, player : P.Player):
        if player not in self.Losers and player not in self.Draws and player not in self.Winners:
            return True
        return False
    
    def checkBlackJack(self, player : P.Player):
        status = player.checkStatus()

        if status == "Dealer BLACKJACK":
            for nondealer in self.Players[1:]:
                if self.playerNotOut(nondealer):
                    self.Losers.append(nondealer)
                nondealer.stand()
                self.Stands += 1
            player.BlackJack = True
            if self.Players[0] not in self.Winners:
                self.Winners.append(self.Players[0])
            self.changeState(2)

        elif status == "dealer LOST":
            for nondealer in self.Players[1:]:
                if nondealer.Total <= 21:
                    if self.playerNotOut(nondealer):
                        self.Winners.append(nondealer)
                    nondealer.stand()
                    self.Stands += 1
            self.changeState(2)

        elif status[-9:] == "BLACKJACK":
            if self.playerNotOut(player):
                self.Winners.append(player)
            player.BlackJack = True
            self.Stands += 1
            player.stand()





    #
    #
    # STATE HANDLING
    #
    #

    def drawState(self):
        self.Drawer.drawBG()
        match self.State:
            case 0:
                self.Drawer.drawMenu(self.Players[self.displayedPlayer].Bet, 
                                     self.Players[self.displayedPlayer].Money,
                                     len(self.Players)-1,
                                     self.displayedPlayer)

            case 1:
                self.Drawer.drawGame(self.Players, self.turn)

            case 2:
                self.Drawer.drawEnd(self.Winners, self.Draws, self.Losers)
        
        pg.display.update()
    
    def handleEvent(self, event: pg.event.Event):
        match self.State:
            case 0:
                choice = self.Caller.menuCaller(event)

                match choice:
                    case "STARTGAME":
                        if self.Players[self.turn].Money > 0 and self.Players[self.turn].Money >= self.Players[self.turn].Bet:
                            self.newGame()
                    case "QUIT":
                        f = io.open("save.txt", "w")
                        f.write(str(self.Players[1].Money))
                        f.close()
                        pg.quit()
                        sys.exit()

                    case "INCREASE100":
                        self.Players[self.displayedPlayer].increaseBet(100)
                    case "INCREASE10":
                        self.Players[self.displayedPlayer].increaseBet(10)
                    case "INCREASE1":
                        self.Players[self.displayedPlayer].increaseBet(1)
                    case "DECREASE1":
                        self.Players[self.displayedPlayer].decreaseBet(1)
                    case "DECREASE10":
                        self.Players[self.displayedPlayer].decreaseBet(10)
                    case "DECREASE100":
                        self.Players[self.displayedPlayer].decreaseBet(100)

                    case "ADDPLAYER":
                        if len(self.Players)-1 <= 3:
                            self.Players.append(P.Player("Player {}".format(len(self.Players))))
                    case "REMPLAYER":
                        if len(self.Players)-1 >= 2:
                            if self.displayedPlayer == len(self.Players)-1:
                                self.displayedPlayer -= 1
                            self.Players.pop()

                    case "ADDMONEY":
                        self.Players[self.displayedPlayer].Money += 100

                    case "PLAYER1":
                        self.displayedPlayer = 1
                    case "PLAYER2":
                        if len(self.Players)-1 >= 2:
                            self.displayedPlayer = 2
                    case "PLAYER3":
                        if len(self.Players)-1 >= 3:
                            self.displayedPlayer = 3
                    case "PLAYER4":
                        if len(self.Players)-1 >= 4:
                            self.displayedPlayer = 4
                        
                    


            case 1:
                # run through every player and check if there's a blackjack
                for player in self.Players:
                    self.checkBlackJack(player)

                # jump to the next turn if the current player is not in
                if not self.Players[self.turn].isIn():
                    self.nextTurn()

                # check how many people are standing, if all players are standing it becomes the dealer's turn
                if self.Stands == len(self.Players) - 1:
                    self.dealerTurn()

                # pass on the event to the gameCaller and get what button is interacted with
                choice = self.Caller.gameCaller(event)
                
                # match the button hit with the functionality that the button should have
                match choice:
                    case "HIT":
                        # Player draws a card
                        self.Players[self.turn].drawCard()
                        # the player's total is checked, and if the total is over 21,
                        if self.Players[self.turn].Total > 21:
                            # then the player stands
                            self.Players[self.turn].stand()
                            # and the number of people standing is incremented
                            self.Stands += 1

                        # then it moves to the next turn no matter what
                        self.nextTurn()

                    case "STAND":
                        # player stands, as they chose to do so
                        self.Players[self.turn].stand()
                        # the number of people standing is incremented
                        self.Stands += 1

                    case "DOUBLE":
                        # Check whether a double can even happen
                        if len(self.Players[self.turn].Hand) == 2 and self.Players[self.turn].Money > 2*self.Players[self.turn].Bet:
                            # Denote in the player-object that they have chosen a double
                            self.Players[self.turn].Double = True
                            # double the player's bet
                            self.Players[self.turn].increaseBet(self.Players[self.turn].Bet)
                            # player draws a card
                            self.Players[self.turn].drawCard()
                            # player stands, as they are not allowed to draw any more cards
                            self.Players[self.turn].stand()
                            # the number of people standing is incremented
                            self.Stands += 1

                    case "SPLIT":
                        # check if a split is even allowed to happen
                        if self.Players[self.turn].Money > 2*self.Players[self.turn].Bet:
                            # collect the index of the current player in the list of players
                            playerIndex = self.Players.index(self.findPlayerFromName("Player {}".format(self.turn)))
                            # add an extra hand dubbed '(player object name)'s split'
                            self.Players.insert(playerIndex+1,
                                                # find the index of the currently active and add 1 to get the index the split will be placed at
                                                P.Player("{}'s split".format(self.Players[playerIndex].name)))
                                                # Initialize a new player object to hold it
                            
                            # set the split hand's parent to be the current player
                            self.Players[playerIndex+1].parent = self.Players[playerIndex]

                            # move the latest card from the current player to the hand of the split
                            self.Players[playerIndex+1].Hand.append(self.Players[playerIndex].Hand.pop())

                            # move money over to the split
                            self.Players[playerIndex].Money -= self.Players[playerIndex].Bet
                            self.Players[playerIndex+1].Money += self.Players[playerIndex].Bet
                            self.Players[playerIndex+1].Bet = self.Players[playerIndex].Bet

                            # both 'players' draw a card
                            self.Players[playerIndex].drawCard()
                            self.Players[playerIndex+1].drawCard()

            case 2:
                choice = self.Caller.endCaller(event)

                match choice:
                    case "BACK TO MENU":
                        for player in self.Winners:
                            if player.Total == 21 and len(player.Hand) == 2:
                                player.BlackJack = True
                                player.Money += player.Bet * 2.5
                            else:
                                player.Money += player.Bet * 2

                        for player in self.Losers:
                            player.Money -= player.Bet

                        for player in reversed(self.Players):
                            if player.parent != None:
                                player.parent.Money += player.Money
                            player.emptyHand()
                            if "split" in player.name:
                                self.Players.remove(player)
                        
                        for player in self.Players:
                            player.Total = 0
                            player.In = True
                            player.BlackJack = False
                            if player.Double:
                                player.decreaseBet(player.Bet/2)

                        self.changeState(0)