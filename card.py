import pygame
import config as g
import os

class Card(pygame.sprite.Sprite):
    id = 0

    def pr(self):
        return ("id:", self.id, self.shape, self.fill, self.numbers +  1, "COLOR:", self.color)

    def __init__(self):
        super().__init__()

    def update(self, *args):
        #print(self.color, args[1])
        if self.color == args[1]:
            image = pygame.transform.scale(pygame.image.load(
                "cards/" + str(self.numbers) + self.shape[0] + self.fill[0] + ".bmp"),
                                           (g.CARD_W, g.CARD_H))
            image.set_colorkey((255, 255, 255))
            self.image = pygame.Surface([g.CARD_W, g.CARD_H])
            self.image.fill(args[0], image.get_rect())
            self.image.blit(image, (0, 0))

    def upd(self, initid, colorlist, coords, unusing_cards):
        self.id = initid
        unusing_cards.remove(initid)
        #print("init by id", self.id)
        fill = ""
        if initid % 3 == 0:
            fill = "empty"
        elif initid %3 == 1:
            fill = "part"
        else:
            fill = "full"

        initid = initid // 3
        numbers = initid % 3
        initid = initid // 3
        shape = ""
        if initid % 3 == 0:
            shape = "oval"
        elif initid % 3 == 1:
            shape = "romb"
        else:
            shape = "zigzag"
        initid = initid // 3
        color = colorlist[initid]
        self.color = initid
        self.shape = shape
        self.numbers = numbers
        self.fill = fill
       # self.image = pygame.image.load(str(initid) + ".bmp").convert()
        #pygame.Surface.fill(colorlist[color])
       # image = pygame.Surface.fill(color, (20, 25))
        image = pygame.transform.scale(pygame.image.load("cards/"+ str(numbers) + shape[0] + fill[0] + ".bmp"), (g.CARD_W, g.CARD_H))
        image.set_colorkey((255, 255, 255))
        self.image = pygame.Surface([g.CARD_W, g.CARD_H])
        self.image.fill(color, image.get_rect())
        self.image.blit(image, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def gt(self, param):
        if param == "n":
            return self.numbers
        elif param == "s":
            return self.shape
        elif param == "f":
            return self.fill
        elif param == "c":
            return self.color

    def checksettable(self, card2, crad3, param):
        return (self.param == card2.param)

    def checkset(card1, card2, card3, *args):
        #print(card1.pr())
        a = ("n", "s", "f", "c")
        dic = {"n": "numbers", "s": "shape", "f": "fill", "c": "color"}
        for i in a:
            if (card1.gt(i) == card2.gt(i) and card3.gt(i) != card1.gt(i)) or \
                    (card2.gt(i) == card3.gt(i) and card1.gt(i) != card2.gt(i))\
                    or (card3.gt(i) == card1.gt(i) and card2.gt(i) != card3.gt(i)):
                if args != ():
                    print("\n   not a set because of :", dic[i])
                return False
        return True

