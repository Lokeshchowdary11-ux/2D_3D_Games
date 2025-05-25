import pygame
import random

pygame.init()
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dodge the Falling Objects")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

bg_image = pygame.image.load("Dodge bg image.jpg")
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

player_width, player_height = 50, 30
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 7
player_color = (0, 128, 255)

falling_width, falling_height = 30, 30
falling_color = (255, 0, 0)
falling_speed = 5
falling_objects = []

spawn_delay = 30
frame_count = 0

score = 0
game_over = False

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global player_x, falling_objects, score, falling_speed, game_over, frame_count
    player_x = screen_width // 2 - player_width // 2
    falling_objects = []
    score = 0
    falling_speed = 5
    game_over = False
    frame_count = 0

reset_game()

running = True
while running:
    clock.tick(60)
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        frame_count += 1
        if frame_count % spawn_delay == 0:
            x_pos = random.randint(0, screen_width - falling_width)
            falling_objects.append(pygame.Rect(x_pos, -falling_height, falling_width, falling_height))

        for obj in falling_objects[:]:
            obj.y += falling_speed
            if obj.y > screen_height:
                falling_objects.remove(obj)
                score += 1
                if score % 10 == 0:
                    falling_speed += 1

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(screen, player_color, player_rect)

        for obj in falling_objects:
            pygame.draw.rect(screen, falling_color, obj)
            if player_rect.colliderect(obj):
                game_over = True

    draw_text(f"Score: {score}", (255, 255, 255), 10, 10)

    if game_over:
        draw_text("Game Over! Press R to Restart", (255, 0, 0), screen_width // 4, screen_height // 2)

    pygame.display.flip()

pygame.quit()
