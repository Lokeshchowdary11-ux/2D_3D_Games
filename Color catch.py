import pygame
import random

pygame.init()

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Color Catch Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 20)

# Load only background music
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

bucket_width, bucket_height = 80, 30
bucket_x = screen_width // 2 - bucket_width // 2
bucket_y = screen_height - bucket_height - 10
bucket_speed = 7

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
]

target_color = random.choice(colors)
bucket_color = target_color

falling_blocks = []
block_size = 30
falling_speed = 5
spawn_delay = 30
frame_count = 0

score = 0
lives = 3
game_over = False
paused = False

def draw_text(text, color, x, y, font_to_use=font):
    img = font_to_use.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global score, lives, falling_blocks, game_over, bucket_x, target_color, bucket_color, falling_speed, spawn_delay, frame_count
    score = 0
    lives = 3
    falling_blocks.clear()
    game_over = False
    bucket_x = screen_width // 2 - bucket_width // 2
    target_color = random.choice(colors)
    bucket_color = target_color
    falling_speed = 5
    spawn_delay = 30
    frame_count = 0
    pygame.mixer.music.play(-1)

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    if not paused and not game_over:
        frame_count += 1
        if score and score % 10 == 0:
            falling_speed = 5 + score // 10
            spawn_delay = max(10, 30 - score // 5)

        if frame_count % spawn_delay == 0:
            x_pos = random.randint(0, screen_width - block_size)
            color = random.choice(colors)
            block_rect = pygame.Rect(x_pos, -block_size, block_size, block_size)
            falling_blocks.append({'rect': block_rect, 'color': color})

        for block in falling_blocks[:]:
            block['rect'].y += falling_speed
            if block['rect'].y > screen_height:
                falling_blocks.remove(block)
                if block['color'] == target_color:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                        pygame.mixer.music.stop()

        bucket_rect = pygame.Rect(bucket_x, bucket_y, bucket_width, bucket_height)
        pygame.draw.rect(screen, bucket_color, bucket_rect)

        for block in falling_blocks:
            pygame.draw.rect(screen, block['color'], block['rect'])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bucket_x > 0:
            bucket_x -= bucket_speed
        if keys[pygame.K_RIGHT] and bucket_x < screen_width - bucket_width:
            bucket_x += bucket_speed

        for block in falling_blocks[:]:
            if bucket_rect.colliderect(block['rect']):
                if block['color'] == target_color:
                    score += 1
                    target_color = random.choice(colors)
                    bucket_color = target_color
                else:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                        pygame.mixer.music.stop()
                falling_blocks.remove(block)

    draw_text(f"Score: {score}", (0, 0, 0), 10, 10)
    draw_text(f"Lives: {lives}", (255, 0, 0), 10, 50)
    draw_text("Catch this color:", (0, 0, 0), 400, 10)
    pygame.draw.rect(screen, target_color, (550, 10, 30, 30))
    draw_text(f"FPS: {int(clock.get_fps())}", (0, 0, 0), 10, 90, small_font)

    if paused:
        draw_text("Game Paused. Press P to resume.", (0, 0, 0), 100, screen_height // 2)
    if game_over:
        draw_text("Game Over! Press R to Restart or Q to Quit.", (255, 0, 0), 50, screen_height // 2)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_r and game_over:
                reset_game()
            if event.key == pygame.K_q and game_over:
                pygame.quit()
                exit()
