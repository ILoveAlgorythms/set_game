from card import Card
import pygame
import config as g
import random
import funcrions as f

pygame.init()
c = [
    (255, 0, 0),
    (0, 255, 0),
    (122, 0, 255),
]
unusing_cards = list() # ids of cards which not used
for i in range(81):
    unusing_cards.append(i)
cardlist = pygame.sprite.Group()
game_goes = True
clicked = list()
# constans declaration
sc = pygame.display.set_mode((g.W + g.CARD_W * 4 + g.NOTCH, g.H),
                             pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("С Е Т")
pygame.display.set_icon(pygame.image.load("p.png"))
#     preparing window
score = 0


while game_goes:
    sc.blit(pygame.transform.scale(pygame.image.load("colorcircle.png"),
                                   (g.CARD_W * 5, g.CARD_W * 5)),
            (g.CARD_W * 4, g.NOTCH))
    # за один тик нужно: дополнить до 12 карт, убирать/прибавлять, пока нет сетов
    if len(cardlist) < 12:
        f.cardto12(cardlist, c, unusing_cards)
        f.makeset(cardlist, c, unusing_cards)## check sets

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_goes = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #print(sc.get_at(pos))
            for i in cardlist.sprites():
                if i.rect.collidepoint(pos):
                    if i not in clicked:
                        clicked.append(i)
                        #print(i.shape, i.numbers)
                        # print("___________", i.r)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_goes = False
            if event.key == pygame.K_q:
                c[0] = sc.get_at(pygame.mouse.get_pos())
                cardlist.update(c[0], 0)
            elif event.key == pygame.K_w:
                c[1] = sc.get_at(pygame.mouse.get_pos())
                cardlist.update(c[1], 1)
            elif event.key == pygame.K_e:
                c[2] = sc.get_at(pygame.mouse.get_pos())
                cardlist.update(c[2], 2)
            cardlist.draw(sc)
        if len(clicked) == 3:
            if Card.checkset(clicked[0], clicked[1], clicked[2], 0):
                #print("\n set!", clicked[0].shape, clicked[1].shape, clicked[2].shape)
                score = score + 1
                print("\n   set! score:", score)
                for i in clicked:
                    cardlist.remove(i)
                    i.kill()
                for a in clicked:
                    newx = a.rect.x
                    newy = a.rect.y
                    a.kill()
                    f.newcard(cardlist, c, newx, newy, unusing_cards)
                cardlist.draw(sc)
                clicked.clear()
                f.cardto12(cardlist, c, unusing_cards)
            else:
                clicked.clear()
                print("not a set!")
        # if event.type == pygame.KEYDOWN: чтобы колео появлялось по нажатию
        #     if event.key == pygame.K_TAB:
        #         wheelsc = (pygame.transform.scale(pygame.image.load("colorcircle.png"), (g.CARD_W * 5, g.CARD_W * 5)) )
        #         sc.blit(wheelsc, (0, 0))
    cardlist.draw(sc)
    pygame.display.flip()
    clock.tick(g.FPS)
