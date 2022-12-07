from card import Card, Button
import pygame
import config
from config import NOT_A_SET_POSITION as nsp
import functions as f
from colorcircle import ColorCircle
import time
import json


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

    def paintitblack(self):
        self.sc.fill(config.BLACK, self.sc.get_rect())

    def reset_scores(self):
        xcenter = self.sc.get_rect().centerx
        game_goes = True
        waiting = -1
        buttons = pygame.sprite.Group()
        f.draw_text(self.sc, (xcenter, 2 * config.NOTCH), self.font, "are you sure you want to delete all you scores?")
        yes_button = Button("yes", self.colorlist, 0, (xcenter - (config.BUTTON_W + config.NOTCH) / 2, 2 * config.BUTTON_H))
        no_button = Button("no", self.colorlist, 1, (xcenter + (config.BUTTON_W + config.NOTCH) / 2, 2 * config.BUTTON_H))
        buttons.add(yes_button, no_button)
        buttons.draw(self.sc)
        while game_goes:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_goes = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if no_button.rect.collidepoint(pos):
                        self.paintitblack()
                        return
                    elif yes_button.rect.collidepoint(pos):
                        for i in ('quick.json', 'classic.json', 'endless.json'):
                            with open(i, "w") as file:
                                json.dump(dict(), file)
                        waiting = config.NOT_A_SET_TICKS
                        f.draw_text(self.sc, (xcenter, 3 * config.BUTTON_H), self.font, "deleted")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_goes = False
            if waiting > 0:
                waiting = waiting - 1
            elif waiting == 0:
                game_goes = False
            buttons.draw(self.sc)
            pygame.display.flip()
            self.clock.tick(config.FPS)
        self.paintitblack()

    def menutext(self):
        f.draw_text(self.sc, (self.sc.get_rect().centerx, 2 * config.NOTCH), self.font, "press space to exit")

    def menu(self):
        xcenter = self.sc.get_rect().centerx
        game_goes = True
        buttons = pygame.sprite.Group()
        classic_button = Button("classic", self.colorlist, 0, (xcenter - (config.BUTTON_W + config.NOTCH) / 2, 2 * config.BUTTON_H))
        reset_button = Button("reset", self.colorlist, 1, (xcenter - (config.BUTTON_W + config.NOTCH) / 2, config.NOTCH + 3 * config.BUTTON_H))
        endless_buton = Button("endless", self.colorlist, 2, (xcenter + (config.BUTTON_W + config.NOTCH) / 2, 2 * config.BUTTON_H))
        quick_button = Button("quick", self.colorlist, 0, (xcenter + (config.BUTTON_W + config.NOTCH) / 2, config.NOTCH + 3 * config.BUTTON_H))
        buttons.add(classic_button, reset_button, endless_buton, quick_button)
        buttons.draw(self.sc)
        self.menutext()
        while game_goes:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_goes = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if reset_button.rect.collidepoint(pos):
                        self.paintitblack()
                        self.reset_scores()
                        self.menutext()
                    else:
                        for i in buttons:
                            if i.rect.collidepoint(pos):
                                self.paintitblack()
                                self.game(i.gamemode)
                                self.paintitblack()
                                self.menutext()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_goes = False
            buttons.draw(self.sc)
            pygame.display.flip()
            self.clock.tick(config.FPS)

    def render(self, buttons, cardlist, colorwheel, waiting):
        buttons.draw(self.sc)
        cardlist.draw(self.sc)
        colorwheel.draw() if colorwheel.onscreen else 0
        pygame.display.flip()
        if waiting > 0:
            return (waiting - 1)
        elif waiting == 0:
            self.sc.fill(config.BLACK, (nsp[0] - 100, nsp[1] - 100, nsp[0] + 100, nsp[1] + 100))
            return -1
        else:
            return waiting

    def color_change_handler(self, pos, key, cardlist):
        newcolor = self.sc.get_at(pos)
        if not (newcolor in self.colorlist or newcolor == config.BLACK):
            if key == pygame.K_q:
                self.colorlist[0] = self.sc.get_at(pos)
                cardlist.update(self.colorlist[0], 0, self.colorlist)
            elif key == pygame.K_w:
                self.colorlist[1] = self.sc.get_at(pos)
                cardlist.update(self.colorlist[1], 1, self.colorlist)
            elif key == pygame.K_e:
                self.colorlist[2] = self.sc.get_at(pos)
                cardlist.update(self.colorlist[2], 2, self.colorlist)

    def clicked_handler(self, clicked, cardlist, unusing_cards, score, endless):
        if Card.checkset(clicked[0], clicked[1], clicked[2], 0):
            print("\n   set! score:", score)
            f.draw_text(self.sc, config.SET_POS, self.font, 'Your Score: ' + str(score + 1))
            for i in clicked:
                unusing_cards.append(i.id) if endless else 0
                cardlist.remove(i)
                i.kill()
            for a in clicked:
                newx = a.rect.x
                newy = a.rect.y
                a.kill()
                f.newcard(cardlist, self.colorlist, newx, newy, unusing_cards)
            cardlist.draw(self.sc)
            clicked.clear()
            f.cardtofull(cardlist, self.colorlist, unusing_cards, self.sc, config.CARDS_ON_BOARD)
            f.makeset(cardlist, self.colorlist, unusing_cards)
            for i in cardlist:
                i.click(self.colorlist)
                i.unclick(self.sc)
            return True
        else:
            for i in clicked:
                i.unclick(self.sc)
            f.draw_text(self.sc, nsp, self.font, 'NOT A SET!', color=(self.colorlist[0]))
            clicked.clear()
            return False

    def clickset(self, cardlist, unusing_cards, remove_set_from_deck):  # читкод для отладки
        clicked = list(f.find_set(cardlist))
        self.clicked_handler(clicked, cardlist, unusing_cards, -1, not remove_set_from_deck)

    def mouse_button_handler(self, cardlist, clicked, showset_button):
        pos = pygame.mouse.get_pos()
        for i in cardlist.sprites():
            if i.rect.collidepoint(pos):
                if (i not in clicked):
                    clicked.append(i)
                    i.click(self.colorlist)
                else:
                    i.unclick(self.sc)
                    clicked.remove(i)
        if showset_button.rect.collidepoint(pos):
            f.showset(self.sc, cardlist)

    def end_of_game(self, result, gamemode, wascheating):
        self.paintitblack()
        if gamemode in ('quick', 'classic'):
            score = str(time.ctime(time.time() - result))[-10:-5]
        elif gamemode in ('', 'endless'):
            score = str(result)
        else:
            score = "looks like its an error!"

        if gamemode in ('quick', 'classic'):
            message = "Total time:  " + score
        elif gamemode in ('', 'endless'):
            message = "Total time:  " + score
        else:
            message = "looks like its an error!"

        f.draw_text(self.sc, (self.sc.get_rect().centerx, config.CARD_H), self.font, message)
        f.draw_text(self.sc, (self.sc.get_rect().centerx, 1.5 * config.CARD_H + config.NOTCH), self.font, "previous scores:")

        with open(gamemode + ".json", "r") as file:
            previous_scores = json.load(file)
        if not wascheating:
            previous_scores[time.ctime(time.time())] = score
            with open(gamemode + ".json", "w") as file:
                json.dump(previous_scores, file)

        toscreen = sorted(previous_scores.keys(), key=lambda x: previous_scores[x])[0:5]
        score_string_pos = 1
        font = pygame.font.SysFont(size=30, bold=False, italic=False, name='consolas')
        for i in toscreen:
            f.draw_text(self.sc, (self.sc.get_rect().centerx, 2 * config.CARD_H + score_string_pos * config.NOTCH), font, str(score_string_pos) + "   " + i[4:10] + ":    " + previous_scores[i])
            score_string_pos += 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 0

            self.clock.tick(config.FPS)

    def game(self, gamemode):
        buttons, cardlist = pygame.sprite.Group(), pygame.sprite.Group()
        showset_button = Button('showset', self.colorlist, 0, (config.NOTCH + config.BUTTON_W / 2, 2.6 * config.NOTCH + config.BUTTON_H / 2))
        colorwheel = ColorCircle(self.sc)
        buttons.add(showset_button)
        number_of_sets = config.GAMEMODENUMBERS.get(gamemode, 27)
        unusing_cards = [i for i in range(config.CARDS_QUANTITY)]  # ids of cards which not used
        game_goes, sv_cheats = True, 0
        timestart = time.time()
        clicked = []
        waiting, score = -1, 0
        while len(cardlist) < config.CARDS_ON_BOARD:
            f.cardtofull(cardlist, self.colorlist, unusing_cards, self.sc, config.CARDS_ON_BOARD)
            f.makeset(cardlist, self.colorlist, unusing_cards)  # check sets
        while game_goes and (score < number_of_sets or gamemode == 'endless'):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sv_cheats = 1
                    game_goes = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_handler(cardlist, clicked, showset_button)
                    if len(clicked) == 3:
                        if self.clicked_handler(clicked, cardlist, unusing_cards, score, gamemode == 'endless'):
                            score += 1
                        else:
                            waiting = config.NOT_A_SET_TICKS
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        sv_cheats = 1
                        game_goes = False
                    elif event.key in (pygame.K_q, pygame.K_w, pygame.K_e):
                        pos = pygame.mouse.get_pos()
                        if not colorwheel.rect.collidepoint(pos):
                            self.color_change_handler(pos, event.key, cardlist)
                    elif event.key == pygame.K_TAB:
                        colorwheel.onscreen = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        colorwheel.undraw()
                        f.draw_text(self.sc, config.SET_POS, self.font, 'Your Score: ' + str(score))
            waiting = self.render(buttons, cardlist, colorwheel, waiting)
            if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_l]:  # читкод для отладки
                self.clickset(cardlist, unusing_cards, gamemode != 'endless')
                number_of_sets += -1
                sv_cheats = 1
            self.clock.tick(config.FPS)
        self.end_of_game(score if gamemode == 'endless' else timestart, gamemode, sv_cheats == 1)
        return 0
