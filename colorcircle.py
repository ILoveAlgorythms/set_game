import pygame
import config

class ColorCircle(pygame.sprite.Sprite):
    def __init__(self, sc):
        super().__init__()
        self.sc = sc
        self.onscreen = False
        self.image = pygame.transform.scale(pygame.image.load("colorcircle.png"),
                                            (config.CARD_W * 5, config.CARD_W * 5))
        self.rect = self.image.get_rect()
    def update(self):
        if self.onscreen:
            self.undraw()
        else:
            self.draw()

    def draw(self):
        self.sc.blit(pygame.transform.scale(pygame.image.load("colorcircle.png"),
                                       (config.CARD_W * 5, config.CARD_W * 5)),
                (config.CARD_W * 3 + 3.5 * config.NOTCH, config.NOTCH))


    def undraw(self):
        self.onscreen = False
        self.sc.fill(config.BLACK, (0, 0, config.W + config.CARD_W * 4 + config.NOTCH, config.H))