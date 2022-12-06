import pygame
import config

class ColorCircle(pygame.sprite.Sprite):
    def draw(self, sc):
        self.image = pygame.transform.scale(pygame.image.load("colorcircle.png"),
                                       (config.CARD_W * 5, config.CARD_W * 5))
        sc.blit(pygame.transform.scale(pygame.image.load("colorcircle.png"),
                                       (config.CARD_W * 5, config.CARD_W * 5)),
                (config.CARD_W * 3 + 3.5 * config.NOTCH, config.NOTCH))


    def undraw(self, sc):