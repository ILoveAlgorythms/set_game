from card import Card
import pygame
import config as g
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
waiting = -1

# constans declaration
sc = pygame.display.set_mode((g.W + g.CARD_W * 4 + g.NOTCH, g.H),
                             pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("С Е Т")
pygame.display.set_icon(pygame.image.load("p.png"))
#     preparing window
score = 0

font = pygame.font.Font(None, 40)

text = font.render('Your Score: ' + str(score), True, (255, 255, 255), (0, 0, 0))
text_pos = text.get_rect(center=(g.CARD_W * 4 + 3.5 * g.NOTCH, g.CARD_W * 6))

f.draw_text(sc, text_pos, font, score)
nsp = (sc.get_width() - 4 * g.CARD_W, sc.get_height() - g.CARD_H/2) # not a set pos

while game_goes:
    sc.blit(pygame.transform.scale(pygame.image.load("colorcircle.png"),
                                   (g.CARD_W * 5, g.CARD_W * 5)),
            (g.CARD_W * 3 + 3.5 * g.NOTCH, g.NOTCH))
    # за один тик нужно: дополнить до 12 карт, убирать/прибавлять, пока нет сетов
    if len(cardlist) < 12:
        f.cardto12(cardlist, c, unusing_cards)
        f.makeset(cardlist, c, unusing_cards)## check sets

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_goes = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i in cardlist.sprites():
                if i.rect.collidepoint(pos):
                    if i not in clicked:
                        clicked.append(i)
                        i.click(c)
                    else:
                        i.unclick(sc)
                        clicked.remove(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_goes = False
            if event.key in (pygame.K_q, pygame.K_w, pygame.K_e):
                if not (sc.get_at(pygame.mouse.get_pos()) == sc.get_at((0, 0))):
                    if event.key == pygame.K_q:
                        c[0] = sc.get_at(pygame.mouse.get_pos())
                        cardlist.update(c[0], 0, c)
                    elif event.key == pygame.K_w:
                        c[1] = sc.get_at(pygame.mouse.get_pos())
                        cardlist.update(c[1], 1, c)
                    elif event.key == pygame.K_e:
                        c[2] = sc.get_at(pygame.mouse.get_pos())
                        cardlist.update(c[2], 2, c)
                    cardlist.draw(sc)
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
                    f.newcard(cardlist, c, newx, newy, unusing_cards)
                cardlist.draw(sc)
                clicked.clear()
                f.cardto12(cardlist, c, unusing_cards)
                for i in cardlist:
                    i.click(c)
                    i.unclick(sc)
            else:
                for i in clicked:
                    i.unclick(sc)
                waiting = g.NOT_A_SET_TICKS
                f.notaset(sc, nsp, font)
                clicked.clear()
                print("not a set!")

    if waiting > 0 and waiting != -1:
        waiting = waiting - 1
    else:
        waiting = -1
        sc.fill((0, 0, 0), (nsp[0], nsp[1], nsp[0] + 50, nsp[1] + 50) )
    cardlist.draw(sc)
    pygame.display.flip()
    clock.tick(g.FPS)
