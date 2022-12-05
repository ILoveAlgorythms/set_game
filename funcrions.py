from card import Card
import config
import random
from pygame import display

# def fill_with_sets(sc, cardlist, colors, unusing_cards):
#     while len(cardlist) < 12:
#         Card(cardlist, random.choice(unusing_cards), colors)


def showset(sc, cardlist):
    print(1)

def draw_text(sc, pos, font, score):
    text = font.render('Your Score: ' + str(score), True, (255, 255, 255), (0, 0, 0))
    sc.blit(text, pos)
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


    #print(newcard.groups())



def cardto12(cardlist, c, unusing_cards):
    a_ = list()
    while len(cardlist) < 12 :
        x = config.NOTCH + (len(cardlist) % 3) * config.CARD_W + (len(cardlist) % 3) * config.NOTCH#
        y = config.NOTCH + (len(cardlist) // 3) * config.CARD_H + (len(cardlist) // 3) * config.NOTCH
        a_.append(newcard(cardlist, c, x, y, unusing_cards))



def makeset(cardlist, c, unusing_cards):
    b = False
    for i in cardlist:
        for j in cardlist:
            if i.id != j.id:
                for k in cardlist:
                    if i.id != k.id and j.id != k.id:
                        if Card.checkset(i, j, k):
                            b = True
                            print("there is s set: ", i, j, k, sep="\n")
                            break
                        #return b

    while not b:
        for i in range(3):
            a = random.choice((cardlist.sprites()))
            print(a)
            newx = a.rect.x
            newy = a.rect.y
            unusing_cards.append(a.id)
            a.kill()
            newcard(cardlist, c, newx, newy, unusing_cards)
        print(unusing_cards)

        b = False
        for i in cardlist:
            for j in cardlist:
                if i.id != j.id:
                    for k in cardlist:
                        if i.id != k.id and j.id != k.id:
                            if Card.checkset(i, j, k):
                                b = True
                                print("  there is s set: ", i, j, k, sep="\n")
                                break