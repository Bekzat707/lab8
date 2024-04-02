import pygame
import random

pygame.init()

W, H = 1200, 800
FPS = 60
pygame.display.set_caption("aka Ackanoid")
icon=pygame.image.load('ackanoid/game.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
bg = (0, 0, 0)


paddleW = 150
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)


ballRadius = 20
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

game_score = 0
game_score_fonts = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (255, 255, 255))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)

collision_sound = pygame.mixer.Sound(r"c:\Users\bekza\OneDrive\Документы\GitHub\lab8\ackanoid\ackanoid_olen.mp3")

block_list = [pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(random.randrange(0, 255), random.randrange(0, 255),  random.randrange(0, 255)) for _ in range(len(block_list))]

unbreakable_bricks = [pygame.Rect(10 + 120 * i, 10, 100, 50) for i in range(5)]

losefont = pygame.font.SysFont('comicsansms', 40)
losetext = losefont.render('Game Over', True, (255, 255, 255))
losetextRect = losetext.get_rect()
losetextRect.center = (W // 2, H // 2)


winfont = pygame.font.SysFont('comicsansms', 40)
wintext = winfont.render('You win yay', True, (0, 0, 0))
wintextRect = wintext.get_rect()
wintextRect.center = (W // 2, H // 2)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(bg)

    [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]

    for brick in unbreakable_bricks:
        pygame.draw.rect(screen, (255, 255, 0), brick)

    pygame.draw.rect(screen, pygame.Color(255, 255, 255), paddle)
    pygame.draw.circle(screen, pygame.Color(255, 0, 0), ball.center, ballRadius)

    
    ball.x += ballSpeed * dx
    ball.y += ballSpeed * dy

    # Collision left/right
    if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
        dx = -dx

   
    if ball.centery < ballRadius + 50:
        dy = -dy

   
    if ball.colliderect(paddle) and dy > 0:
        dy = -dy
        collision_sound.play()

   
    hitIndex = ball.collidelist(block_list)
    if hitIndex != -1:
        block_list.pop(hitIndex)
        color_list.pop(hitIndex)
        dy = -dy
        game_score += 1
        collision_sound.play()

   
    game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (255, 255, 255))
    screen.blit(game_score_text, game_score_rect)

  
    if ball.bottom > H:
        screen.fill((0, 0, 0))
        screen.blit(losetext, losetextRect)
    elif not len(block_list):
        screen.fill((255, 255, 255))
        screen.blit(wintext, wintextRect)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddleSpeed
    if key[pygame.K_RIGHT] and paddle.right < W:
        paddle.right += paddleSpeed

    pygame.display.flip()
    clock.tick(FPS)