import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()

paddle_hit = pygame.mixer.Sound("background.mp3")


ball = pygame.Rect(295, 195, 10, 10)
ball_speed = [4, 4]
paddle_player = pygame.Rect(20, 150, 10, 100)
paddle_ai = pygame.Rect(570, 150, 10, 100)
score = [0, 0]
font = pygame.font.SysFont(None, 36)

max_score = 10
running = True
game_over = False

while running:
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (255, 255, 255), paddle_player)
    pygame.draw.rect(screen, (255, 255, 255), paddle_ai)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)

    if not game_over:
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.top <= 0 or ball.bottom >= 400:
            ball_speed[1] = -ball_speed[1]
            paddle_hit.play()

        if ball.colliderect(paddle_player) or ball.colliderect(paddle_ai):
            ball_speed[0] = -ball_speed[0]
            paddle_hit.play()

        if ball.left <= 0:
            score[1] += 1
            ball.x, ball.y = 295, 195
        elif ball.right >= 600:
            score[0] += 1
            ball.x, ball.y = 295, 195

        if score[0] == max_score or score[1] == max_score:
            game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle_player.top > 0:
            paddle_player.y -= 5
        if keys[pygame.K_s] and paddle_player.bottom < 400:
            paddle_player.y += 5

        if paddle_ai.centery < ball.centery and paddle_ai.bottom < 400:
            paddle_ai.y += 4
        if paddle_ai.centery > ball.centery and paddle_ai.top > 0:
            paddle_ai.y -= 4

    else:
        winner = "Player" if score[0] == max_score else "AI"
        win_text = font.render(f"{winner} Wins!", True, (0, 255, 0))
        screen.blit(win_text, (220, 180))
        restart_text = font.render("Press R to Restart", True, (200, 200, 200))
        screen.blit(restart_text, (180, 220))

    text = font.render(f"{score[0]} : {score[1]}", True, (255, 255, 255))
    screen.blit(text, (270, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            score = [0, 0]
            ball.x, ball.y = 295, 195
            game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
