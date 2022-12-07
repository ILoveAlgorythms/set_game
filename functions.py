from card import Card
import config
import random
from pygame import display


def showset(sc, cardlist):
    print(1)


def draw_text(sc, pos, font, message):  # ПЕРЕДЕЛАТЬ
    text = font.render(message, True, (255, 255, 255), (0, 0, 0))
    text_pos = text.get_rect(center=pos)
    sc.blit(text, text_pos)
    display.update()


def notaset(sc, pos, font):
    text = font.render('This is not a set!', True, (255, 255, 255), (0, 0, 0))
    sc.blit(text, pos)
    display.update()


def newcard(cardlist, c, x, y, unusing_cards):
    newid = int(random.choice(unusing_cards))
    newcard_ = Card()
    newcard_.upd(newid, c, (x, y), unusing_cards)
    cardlist.add(newcard_)


def cardto12(cardlist, c, unusing_cards):
    a_ = list()
    while len(cardlist) < config.CARDS_ON_BOARD:
        x = config.NOTCH + (len(cardlist) % 3) * config.CARD_W + (len(cardlist) % 3) * config.NOTCH  #
        y = config.NOTCH + (len(cardlist) // 3) * config.CARD_H + (len(cardlist) // 3) * config.NOTCH
        a_.append(newcard(cardlist, c, x, y, unusing_cards))


def find_set(cardlist):
    for i in cardlist:
        for j in cardlist:
            if i.id != j.id:
                for k in cardlist:
                    if i.id != k.id and j.id != k.id:
                        if Card.checkset(i, j, k):
                            print("   There is a set: ", i, j, k, sep="\n")
                            return i, j, k
    return False


def makeset(cardlist, c, unusing_cards):
    set_on_table = find_set(cardlist)
    while not set_on_table:
        for i in range(3):
            a = random.choice((cardlist.sprites()))
            newx = a.rect.x
            newy = a.rect.y
            unusing_cards.append(a.id)
            a.kill()
            newcard(cardlist, c, newx, newy, unusing_cards)

        set_on_table = find_set(cardlist)
