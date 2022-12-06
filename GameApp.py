from card import Card, Button
import pygame
import config
import functions as f


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
        text = self.font.render('нажмите 3 чтобы начать', True, (255, 255, 255), (0, 0, 0))
        xcenter = self.sc.get_rect().centerx
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
                    if text.get_rect().collidepoint(pos):
                        self.classic()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.sc.fill(config.BLACK, self.sc.get_rect())
                        self.classic()
                    elif event.key == pygame.K_SPACE:
                        game_goes = False

            pygame.display.flip()
            self.clock.tick(config.FPS)

    def classic(self):
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
        text = font.render('Your Score: ' + str(score), True, (255, 255, 255), (0, 0, 0))
        text_pos = text.get_rect(center=(config.CARD_W * 4 + 3.5 * config.NOTCH, config.CARD_W * 6))

        f.draw_text(sc, text_pos, font, score)
        nsp = (sc.get_width() - 4 * config.CARD_W, sc.get_height() - config.CARD_H / 2)  # not a set pos
        while game_goes:

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
                            f.draw_text(sc, text_pos, font, score)
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
                        if not (sc.get_at(pygame.mouse.get_pos()) == sc.get_at((0, 0))):
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

            if waiting > 0 and waiting != -1:
                waiting = waiting - 1
            else:
                waiting = -1
                sc.fill((0, 0, 0), (nsp[0], nsp[1], nsp[0] + 50, nsp[1] + 50))
            cardlist.draw(sc)
            pygame.display.flip()
            clock.tick(config.FPS)

    def tutorial(self):
        print("notfinished yet")
