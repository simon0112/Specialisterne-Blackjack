import pygame as pg
#Game colors
GREENBG = pg.Color(45, 165, 45)

class Draw(object):
    def __init__(self) -> None:
        self.Surface : pg.surface.Surface = pg.display.set_mode((600,900))
        self.font : pg.font.Font = pg.font.SysFont("Times New Roman", 34)




    #
    #
    # HELPER FUNCTIONS
    #
    #

    def drawBG(self):
        self.Surface.fill(GREENBG)

    def placeText(self, screen: pg.Surface, text: str, position: tuple[int, int]) -> pg.Rect:
        return screen.blit(self.font.render(text, True, (0,0,0)), position)





    #
    #
    # DRAW HANDLING
    #
    #

    def drawMenu(self, Bet:int, Money:int, playerAmt: int, turn : int):

        NEWHANDBOX = pg.draw.rect(self.Surface, (15, 225, 15), pg.Rect(100, 25, 400, 200))
        if Money <= 0:
            self.placeText(self.Surface, "No more money,", (110, 90))
            self.placeText(self.Surface, "no gambling for you", (110, 120))
        elif Bet > Money:
            self.placeText(self.Surface, "Bet is too high", (190,105))
        else:
            self.placeText(self.Surface, "Play New Hand", (190,105))

        
        BETBORDERBOX = pg.draw.rect(self.Surface, (30, 195, 30), pg.Rect(95, 295, 410, 60))
        self.placeText(self.Surface, "Player {} Bet is: {}".format(turn, Bet), (200,240))
        
        NEG100BOX = pg.draw.rect(self.Surface, (15,225,15), pg.Rect(100, 300, 75, 50))
        self.placeText(self.Surface, "-100", (105,305))

        NEG10BOX = pg.draw.rect(self.Surface, (15,225,15), pg.Rect(180, 300, 60, 50))
        self.placeText(self.Surface, "-10", (185, 305))

        NEG1BOX = pg.draw.rect(self.Surface, (15,225,15), pg.Rect(245, 300, 40, 50))
        self.placeText(self.Surface, "-1", (250, 305))

        POS100BOX = pg.draw.rect(self.Surface, (15,225,15), pg.Rect(425, 300, 75, 50))
        self.placeText(self.Surface, "+100", (427, 305))

        POS10BOX = pg.draw.rect(self.Surface, (15,225,15), pg.Rect(360, 300, 60, 50))
        self.placeText(self.Surface, "+10", (362, 305))

        POS1BOX = pg.draw.rect(self.Surface, (15,225,15), pg.Rect(315, 300, 40, 50))
        self.placeText(self.Surface, "+1" , (317, 305))

        
        self.placeText(self.Surface, "Player {} money is: {}".format(turn, Money), (175,360))
        ADDMONEYBOX = pg.draw.rect(self.Surface, (15,225,15), pg.Rect(100, 400, 400, 75))
        self.placeText(self.Surface, "Add 100 to current player", (125, 418))

        if playerAmt <= 3:
            ADDPLAYERBOX = pg.draw.rect(self.Surface, (15, 225, 15), pg.Rect(100, 590, 195, 50))
            self.placeText(self.Surface, "Add player", (120, 595))

        if playerAmt >= 2:
            REMPLAYERBOX = pg.draw.rect(self.Surface, (15, 225, 15), pg.Rect(305, 590, 195, 50))
            self.placeText(self.Surface, "Rem. player", (320, 595))

        for x in range(playerAmt):
            pg.draw.rect(self.Surface, (15,225,15), pg.Rect(125+x*100, 530, 50, 50))
            self.placeText(self.Surface, "{}".format(str(x+1)), (142+x*100, 535))
        self.placeText(self.Surface, "number of players", (178, 485))

        EXITBOX = pg.draw.rect(self.Surface, (15, 225, 15), pg.Rect(100, 650, 400, 200))
        self.placeText(self.Surface, "Save & Exit", (210, 730))



    def drawGame(self, players, turn: int):

        playerx = 1
        
        for _, _, card in players[turn].Hand:
            card = pg.transform.scale(card, (207, 300))
            self.Surface.blit(card, (50+(playerx*50), 485))
            playerx += 1

        dealerx = 1

        for _, _, card in players[0].Hand:
            card = pg.transform.scale(card, (207, 300))
            self.Surface.blit(card, (50+(dealerx*50), 25))
            dealerx += 1

        UPDATEBOX = pg.draw.rect(self.Surface, GREENBG, pg.Rect(0, 325, 600, 160))

        self.placeText(self.Surface, "Dealer total: {}".format(players[0].Total), (215, 330))
        self.placeText(self.Surface, "{} total: {}".format(players[turn].name, players[turn].Total), (200, 425))

        INTBOX = pg.draw.rect(self.Surface, (15, 225, 15), pg.Rect(100, 795, 400, 60))
        
        HITBOX = pg.draw.rect(self.Surface, (255,255,255), pg.Rect(105, 800, 90, 50) )
        self.placeText(self.Surface, "Hit", (125, 805))

        STANDBOX = pg.draw.rect(self.Surface, (255,255,255), pg.Rect(205, 800, 90, 50) )
        self.placeText(self.Surface, "Stand", (210, 805))

        if len(players[turn].Hand) == 2 and players[turn].Money > 2*players[turn].Bet:
            DOUBLEBOX = pg.draw.rect(self.Surface, (255,255,255), pg.Rect(305, 800, 90, 50) )
            self.placeText(self.Surface, "x2", (335, 805))

            if  players[turn].Hand[0][0] == players[turn].Hand[1][0]:
                SPLITBOX = pg.draw.rect(self.Surface, (255,255,255), pg.Rect(405, 800, 90, 50) )
                self.placeText(self.Surface, "Split", (420, 805))



    def drawEnd(self, winners, draws, losers):
        self.placeText(self.Surface, "Winners: ", (50, 50))
        winnerYPlace = 1
        for player in winners:
            if player.name != "Dealer" or player.BlackJack:
                if player.BlackJack:
                    if player.name == "Dealer":
                        self.placeText(self.Surface, "{} won, blackjack".format(player.name, player.Bet*2.5), (50, 60+(40*winnerYPlace)))
                    else:
                        self.placeText(self.Surface, "{}, money won: {}, blackjack".format(player.name, player.Bet*2.5), (40, 60+(40*winnerYPlace)))
                else:
                    self.placeText(self.Surface, "{}, money won: {}".format(player.name, player.Bet*2), (50, 60+(40*winnerYPlace)))
                winnerYPlace += 1
        
        self.placeText(self.Surface, "Draws: ", (50, 250))
        drawYPlace = 1
        for player in draws:
            self.placeText(self.Surface, "{} got a draw, bet is returned as-is".format(player.name), (50, 260+(40*drawYPlace)))

        self.placeText(self.Surface, "Losers: ", (50, 430))
        losersYPlace = 1
        for player in losers:
            self.placeText(self.Surface, "{}, money lost: {}".format(player.name, player.Bet), (50, 440+(40*losersYPlace)))
            losersYPlace += 1

        BACKTOMENUBOX = pg.draw.rect(self.Surface, (15, 225, 15), pg.Rect(50, 610, 500, 280) )
        self.placeText(self.Surface, "Return to menu", (200, 732))