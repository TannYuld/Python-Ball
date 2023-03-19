import pygame, Sprite, Path

pygame.init()
screen = pygame.display.set_mode((700,384))
clock = pygame.time.Clock()
running = True
#pygame.mouse.set_visible(False)

text_font = pygame.font.Font(Path.font_path, 36)

def text(text, font, text_col, pos_x, pos_y):
    img = font.render(text, True, text_col)
    screen.blit(img, (pos_x, pos_y))

def change_score_text():
    global score_text

    if Sprite.score < 9:
        score_text = "0 0 "+str(Sprite.score)
    elif Sprite.score < 99:
        score_text = "0 "+str(get_digit(Sprite.score, 1))+" "+str(get_digit(Sprite.score, 0))
    else:
        score_text = str(get_digit(Sprite.score, 2))+" "+str(get_digit(Sprite.score, 1))+" "+str(get_digit(Sprite.score, 0))
        pass
    pass

def get_digit(number, n):
    return number // 10**n % 10

background = Sprite.Background(Path.background, 0, 0, screen)
score_board = Sprite.Sprite(Path.score_board, 670, 57)
healt_bar = Sprite.Healt_Bar(Path.healt_bar_3, 690, 110)
basket_hole = Sprite.Hole(Path.hole, 75, 290, screen)
basket_hole_1 = Sprite.Hole_Child(Path.hole, 75, 290, basket_hole, 700)
basket_hole_2 = Sprite.Hole_Child(Path.hole, 75, 290, basket_hole, -700)
ball_1 = Sprite.Ball(Path.ball, 75, 175, healt_bar, screen)
ball_2 = Sprite.Ball(Path.ball, 75, 175, healt_bar, screen)
ball_3 = Sprite.Ball(Path.ball, 75, 175, healt_bar, screen)
ball_4 = Sprite.Ball(Path.ball, 75, 175, healt_bar, screen)
ball_5 = Sprite.Ball(Path.ball, 75, 175, healt_bar, screen)
ball_6 = Sprite.Ball(Path.ball, 75, 175, healt_bar, screen)
ball_7 = Sprite.Ball(Path.ball, 75, 175, healt_bar, screen)
ball_8 = Sprite.Ball(Path.ball, 75, 175, healt_bar, screen)
second_hole = Sprite.Second_Hole(Path.hole_mask, 75, 290, basket_hole)

score_text = "0 0 0"

def change_score(val):
    Sprite.score = val
    change_score_text()
    pass

pressed_keys = pygame.key.get_pressed()

while running:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()

        if event.type == pygame.KEYUP:
            pressed_keys = pygame.key.get_pressed()

            if event.key == pygame.K_RIGHT:
                basket_hole.un_press()
                pass

            if event.key == pygame.K_LEFT:
                basket_hole.un_press()

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            raise SystemExit

    if pressed_keys[pygame.K_RIGHT]:
        basket_hole.go_right()

    if pressed_keys[pygame.K_LEFT]:
        basket_hole.go_left()

    if Sprite.score <= -1:
        running = False
        pygame.quit()
        raise SystemExit
        pass

    for ball in Sprite.balls:
        if second_hole.rect.colliderect(ball.rect):
            ball.enter_collider()
        pass

    text(score_text, text_font, (255,255,255),597, 35)

    change_score_text()

    pygame.display.flip()
    screen.blit(pygame.image.load(Path.black_background), (0,0))
    Sprite.sprites.draw(screen)
    Sprite.sprites.update()
    clock.tick(60)
    pass

pygame.quit()