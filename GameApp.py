from card import Card, Button
import pygame
import config
import functions as f
from colorcircle import ColorCircle
import time

class GameApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("С Е Т")
        pygame.display.set_icon(pygame.image.load("p.png"))
        self.sc = pygame.display.set_mode((config.W + config.CARD_W * 4 + config.NOTCH, config.H),
                                          pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)
        self.colorlist = [
            (255, 0, 0),
            (0, 255, 0),
            (122, 0, 255),
        ]

    def menu(self):
        xcenter = self.sc.get_rect().centerx
        text = self.font.render('нажмите 3 чтобы начать', True, (255, 255, 255), (0, 0, 0))
        text_pos = text.get_rect(center=(xcenter, config.CARD_H))
        self.sc.blit(text, text_pos)
        pygame.display.update()
        game_goes = True
        buttons = pygame.sprite.Group()
        classic_button = Button("classic", self.colorlist, 0, (xcenter, 2 * config.BUTTON_H))
        tutorial_button = Button("tutorial", self.colorlist, 1, (xcenter, config.NOTCH + 3 * config.BUTTON_H))
        endless_buton = Button("endless", self.colorlist, 2, (xcenter, 2 * config.NOTCH + 4 * config.BUTTON_H))
        buttons.add(classic_button, tutorial_button, endless_buton)
        buttons.draw(self.sc)
        while game_goes:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_goes = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if classic_button.rect.collidepoint(pos):
                        self.sc.fill(config.BLACK, self.sc.get_rect())
                        self.classic(1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.sc.fill(config.BLACK, self.sc.get_rect())
                        self.classic(1)
                    elif event.key == pygame.K_SPACE:
                        game_goes = False

            pygame.display.flip()
            self.clock.tick(config.FPS)

    def classic(self, number_of_sets):
        timestart = time.time()
        unusing_cards = list()  # ids of cards which not used
        for i in range(81):
            unusing_cards.append(i)
        cardlist = pygame.sprite.Group()
        game_goes = True

        clicked = list()
        waiting = -1
        # constants declaration
        sc = self.sc
        clock = self.clock
        score = 0

        font = self.font
        f.draw_text(sc, config.SET_POS, font, 'Your Score: ' + str(score))

        colorwheel = ColorCircle(sc)
        nsp = (sc.get_width() - 4 * config.CARD_W, sc.get_height() - config.CARD_H / 2)  # not a set pos
        while game_goes and score < number_of_sets:  # 27 -- максимальное количество сетов
            if len(cardlist) < config.CARDS_ON_BOARD:
                f.cardto12(cardlist, self.colorlist, unusing_cards)
                f.makeset(cardlist, self.colorlist, unusing_cards)  # check sets

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_goes = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i in cardlist.sprites():
                        if i.rect.collidepoint(pos):
                            if i not in clicked:
                                clicked.append(i)
                                i.click(self.colorlist)
                            else:
                                i.unclick(sc)
                                clicked.remove(i)
                    if len(clicked) == 3:
                        if Card.checkset(clicked[0], clicked[1], clicked[2], 0):
                            score = score + 1
                            print("\n   set! score:", score)
                            f.draw_text(sc, config.SET_POS, font, 'Your Score: ' + str(score))
                            for i in clicked:
                                cardlist.remove(i)
                                i.kill()
                            for a in clicked:
                                newx = a.rect.x
                                newy = a.rect.y
                                a.kill()
                                f.newcard(cardlist, self.colorlist, newx, newy, unusing_cards)
                            cardlist.draw(sc)
                            clicked.clear()
                            f.cardto12(cardlist, self.colorlist, unusing_cards)
                            for i in cardlist:
                                i.click(self.colorlist)
                                i.unclick(sc)
                        else:
                            for i in clicked:
                                i.unclick(sc)
                            waiting = config.NOT_A_SET_TICKS
                            f.notaset(sc, nsp, font)
                            clicked.clear()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_goes = False
                    elif event.key in (pygame.K_q, pygame.K_w, pygame.K_e):
                        if not colorwheel.rect.collidepoint(pygame.mouse.get_pos()):
                            if event.key == pygame.K_q:
                                self.colorlist[0] = sc.get_at(pygame.mouse.get_pos())
                                cardlist.update(self.colorlist[0], 0, self.colorlist)
                            elif event.key == pygame.K_w:
                                self.colorlist[1] = sc.get_at(pygame.mouse.get_pos())
                                cardlist.update(self.colorlist[1], 1, self.colorlist)
                            elif event.key == pygame.K_e:
                                self.colorlist[2] = sc.get_at(pygame.mouse.get_pos())
                                cardlist.update(self.colorlist[2], 2, self.colorlist)
                            cardlist.draw(sc)
                    elif event.key == pygame.K_TAB:
                        colorwheel.draw()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        colorwheel.undraw()

            if waiting > 0 and waiting != -1:
                waiting = waiting - 1
            else:
                waiting = -1
                sc.fill((0, 0, 0), (nsp[0], nsp[1], nsp[0] + 50, nsp[1] + 50))
            cardlist.draw(sc)
            pygame.display.flip()
            clock.tick(config.FPS)
        self.sc.fill(config.BLACK, sc.get_rect())
        f.draw_text(sc, (self.sc.get_rect().centerx, 1.5 * config.CARD_H), font, "Total time:  " + str(time.ctime(time.time() - timestart))[-10:-5])

    def tutorial(self):
        print("notfinished yet")
