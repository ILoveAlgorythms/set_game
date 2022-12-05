import pygame
import config


class Card(pygame.sprite.Sprite):
    id = 0

    def __str__(self):
        return ' '.join(["id:", str(self.id), str(self.shape), str(self.fill), str(self.numbers + 1), "color:", str(self.color)])

    def __repr__(self):
        return str(self.id)

    def __init__(self):
        super().__init__()

    def click(self, colorlist):
        image = pygame.transform.scale(pygame.image.load("cards/template.bmp"),
                                       (config.CARD_W, config.TEMPLATE))
        image.set_colorkey((255, 255, 255))
        fon = pygame.Surface([config.CARD_W, config.TEMPLATE])
        fon.fill(colorlist[self.color])
        fon.blit(image, (0, 0))
        oldimage = self.image
        self.image = pygame.Surface([config.CARD_W, config.CARD_H + config.TEMPLATE])
        self.image.blit(oldimage, (0, 0))
        self.image.blit(fon, (0, config.CARD_H))

    def unclick(self, sc):
        black = pygame.Surface([config.CARD_W, config.TEMPLATE])
        black.fill(config.BLACK, black.get_rect())

        image = pygame.Surface([config.CARD_W, config.CARD_H])
        image.blit(self.image, (0, 0, config.CARD_W, config.CARD_H))
        sc.blit(black, ((self.rect.x, self.rect.y + config.CARD_H)))
        self.image = image

    def update(self, newcolor, oldcolor, colorlist):
        if self.color == oldcolor:
            image = pygame.transform.scale(pygame.image.load(
                "cards/" + str(self.numbers) + self.shape[0] + self.fill[0] + ".bmp"),
                (config.CARD_W, config.CARD_H))
            image.set_colorkey((255, 255, 255))
            self.image = pygame.Surface([config.CARD_W, self.image.get_height()])
            self.image.fill(newcolor, image.get_rect())
            self.image.blit(image, (0, 0))
            if self.image.get_height() > config.CARD_H:
                self.click(colorlist)

    def upd(self, initid, colorlist, coords, unusing_cards):
        self.id = initid
        unusing_cards.remove(initid)
        if initid % 3 == 0:
            fill = "empty"
        elif initid % 3 == 1:
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
        image = pygame.transform.scale(pygame.image.load("cards/" + str(numbers) + shape[0] + fill[0] + ".bmp"), (config.CARD_W, config.CARD_H))
        image.set_colorkey(config.WHITE)
        self.image = pygame.Surface([config.CARD_W, config.CARD_H])
        self.image.fill(color, image.get_rect())
        self.image.blit(image, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    def get_parametr(self, parametr):
        if parametr == "n":
            return self.numbers
        elif parametr == "s":
            return self.shape
        elif parametr == "f":
            return self.fill
        elif parametr == "c":
            return self.color

    def checksettable(self, card2, crad3, param):
        return self.param == card2.param

    def checkset(card1, card2, card3, *args):
        dic = {"n": "numbers", "s": "shape", "f": "fill", "c": "color"}
        for i in dic.keys():
            if (card1.get_parametr(i) == card2.get_parametr(i) and card3.get_parametr(i) != card1.get_parametr(i)) or \
                    (card2.get_parametr(i) == card3.get_parametr(i) and card1.get_parametr(i) != card2.get_parametr(i)) \
                    or (card3.get_parametr(i) == card1.get_parametr(i) and card2.get_parametr(i) != card3.get_parametr(i)):
                if args != ():
                    print("\n   not a set because of :", dic[i])
                    print(card1, card2, card3, '', sep="\n")
                return False
        return True
