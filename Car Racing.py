import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

bg_image = pygame.transform.scale(pygame.image.load("road_0.png"), (400, 600))
player_car = pygame.transform.scale(pygame.image.load("car.png"), (40, 80))
obstacle_car = pygame.transform.scale(pygame.image.load("car (2).png"), (40, 80))
crash_image = pygame.transform.scale(pygame.image.load("fender-bender.png"), (60, 60))

pygame.mixer.music.load("car sound (2).wav")
pygame.mixer.music.play(-1)
crash_sound = pygame.mixer.Sound("car crash sound.mp3")

WHITE = (255, 255, 255)
lanes = [80, 180, 280]

def reset_game():
    global player_x, player_y, obstacle_x, obstacle_y, obstacle_speed, score, bg_y, crashed
    player_x = lanes[1]
    player_y = 500
    obstacle_x = random.choice(lanes)
    obstacle_y = -100
    obstacle_speed = 5
    score = 0
    bg_y = 0
    crashed = False

def draw_start_screen():
    screen.fill((50, 50, 50))
    title = font.render("Car Racing Game", True, (255, 255, 255))
    button = pygame.Rect(100, 250, 200, 60)
    pygame.draw.rect(screen, (0, 200, 0), button)
    text = font.render("Play Now", True, (255, 255, 255))
    screen.blit(title, (110, 180))
    screen.blit(text, (button.x + 40, button.y + 15))
    pygame.display.flip()
    return button

start_button = draw_start_screen()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                waiting = False

reset_game()
running = True

while running:
    screen.fill(WHITE)
    screen.blit(bg_image, (0, bg_y))
    screen.blit(bg_image, (0, bg_y - 600))
    bg_y += 5
    if bg_y >= 600:
        bg_y = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if crashed and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()

    if not crashed:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > lanes[0]:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < lanes[-1]:
            player_x += 5

        obstacle_y += obstacle_speed
        if obstacle_y > 600:
            obstacle_y = -100
            obstacle_x = random.choice(lanes)
            score += 1
            obstacle_speed += 0.3

        player_rect = pygame.Rect(player_x, player_y, 40, 80)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, 40, 80)
        if player_rect.colliderect(obstacle_rect):
            crash_sound.play()
            screen.blit(crash_image, (player_x - 10, player_y - 10))
            pygame.display.flip()
            pygame.time.wait(1000)
            crashed = True

        screen.blit(player_car, (player_x, player_y))
        screen.blit(obstacle_car, (obstacle_x, obstacle_y))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        game_over = font.render("Game Over!", True, (255, 0, 0))
        final_score = font.render(f"Score: {score}", True, (0, 0, 0))
        restart_msg = font.render("Press Space key restart", True, (0, 0, 0))
        screen.blit(game_over, (120, 240))
        screen.blit(final_score, (140, 280))
        screen.blit(restart_msg, (60, 320))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
