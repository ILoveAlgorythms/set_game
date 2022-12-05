from card import Card
import pygame
import config
import funcrions as f

pygame.init()
colorlist = [
    (255, 0, 0),
    (0, 255, 0),
    (122, 0, 255),
]
unusing_cards = list()  # ids of cards which not used
for i in range(81):
    unusing_cards.append(i)
cardlist = pygame.sprite.Group()

game_goes = True

clicked = list()
waiting = -1

# constants declaration
sc = pygame.display.set_mode((config.W + config.CARD_W * 4 + config.NOTCH, config.H),
                             pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("С Е Т")
pygame.display.set_icon(pygame.image.load("p.png"))
#     preparing window
score = 0

font = pygame.font.Font(None, 40)

text = font.render('Your Score: ' + str(score), True, (255, 255, 255), (0, 0, 0))
text_pos = text.get_rect(center=(config.CARD_W * 4 + 3.5 * config.NOTCH, config.CARD_W * 6))

f.draw_text(sc, text_pos, font, score)
nsp = (sc.get_width() - 4 * config.CARD_W, sc.get_height() - config.CARD_H / 2)  # not a set pos

while game_goes:
    sc.blit(pygame.transform.scale(pygame.image.load("colorcircle.png"),
                                   (config.CARD_W * 5, config.CARD_W * 5)),
            (config.CARD_W * 3 + 3.5 * config.NOTCH, config.NOTCH))
    if len(cardlist) < 12:
        f.cardto12(cardlist, colorlist, unusing_cards)
        f.makeset(cardlist, colorlist, unusing_cards)  # check sets

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_goes = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i in cardlist.sprites():
                if i.rect.collidepoint(pos):
                    if i not in clicked:
                        clicked.append(i)
                        i.click(colorlist)
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
                        f.newcard(cardlist, colorlist, newx, newy, unusing_cards)
                    cardlist.draw(sc)
                    clicked.clear()
                    f.cardto12(cardlist, colorlist, unusing_cards)
                    for i in cardlist:
                        i.click(colorlist)
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
                        colorlist[0] = sc.get_at(pygame.mouse.get_pos())
                        cardlist.update(colorlist[0], 0, colorlist)
                    elif event.key == pygame.K_w:
                        colorlist[1] = sc.get_at(pygame.mouse.get_pos())
                        cardlist.update(colorlist[1], 1, colorlist)
                    elif event.key == pygame.K_e:
                        colorlist[2] = sc.get_at(pygame.mouse.get_pos())
                        cardlist.update(colorlist[2], 2, colorlist)
                    cardlist.draw(sc)

    if waiting > 0 and waiting != -1:
        waiting = waiting - 1
    else:
        waiting = -1
        sc.fill((0, 0, 0), (nsp[0], nsp[1], nsp[0] + 50, nsp[1] + 50))
    cardlist.draw(sc)
    pygame.display.flip()
    clock.tick(config.FPS)
