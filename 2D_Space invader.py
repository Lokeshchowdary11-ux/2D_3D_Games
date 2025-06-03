import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Falling Aliens")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load static background image
try:
    background_image = pygame.image.load("bg img.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except:
    background_image = pygame.Surface((WIDTH, HEIGHT))
    background_image.fill(BLACK)

# Start screen background
try:
    start_bg_image = pygame.image.load("Bg image.jpg").convert()
    start_bg_image = pygame.transform.scale(start_bg_image, (WIDTH, HEIGHT))
except:
    start_bg_image = pygame.Surface((WIDTH, HEIGHT))
    start_bg_image.fill((30, 30, 60))

# Game Over screen background
try:
    game_over_bg_image = pygame.image.load("game over.jpg").convert()
    game_over_bg_image = pygame.transform.scale(game_over_bg_image, (WIDTH, HEIGHT))
except:
    game_over_bg_image = pygame.Surface((WIDTH, HEIGHT))
    game_over_bg_image.fill((50, 0, 0))

# Player
try:
    player_img = pygame.image.load("Player img.png").convert_alpha()
except:
    player_img = pygame.Surface((60, 40))
    player_img.fill(GREEN)

player_rect = player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
player_speed = 5

# Alien
try:
    alien_img = pygame.image.load("aline img.png").convert_alpha()
except:
    alien_img = pygame.Surface((40, 30))
    alien_img.fill((255, 0, 0))

# Bullet
bullet_img = pygame.Surface((5, 10))
bullet_img.fill((255, 255, 0))
bullet_speed = -7
bullets = []

# Sounds
try:
    shoot_sound = pygame.mixer.Sound("shooter sound.wav")
except:
    shoot_sound = None

try:
    enemy_killed_sound = pygame.mixer.Sound("enemy kill sound.wav")
except:
    enemy_killed_sound = None

# Fonts
font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60)

# Game state variables
aliens = []
alien_fall_speed = 2
alien_spawn_interval = 1000
last_alien_spawn_time = pygame.time.get_ticks()

score = 0
game_over = False
game_started = False
shoot_cooldown = 200
last_shot_time = 0
clock = pygame.time.Clock()

def draw_text(text, x, y, size=28, color=WHITE, center=False):
    used_font = big_font if size > 30 else font
    surface = used_font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def draw_button(rect, text, text_color=BLACK, button_color=GREEN):
    pygame.draw.rect(screen, button_color, rect)
    draw_text(text, rect.centerx, rect.centery, 30, text_color, center=True)

def spawn_alien():
    x = random.randint(0, WIDTH - 40)
    alien_rect = pygame.Rect(x, -30, 40, 30)
    aliens.append(alien_rect)

def reset_game():
    global aliens, bullets, score, player_rect, last_shot_time, last_alien_spawn_time, game_over
    aliens.clear()
    bullets.clear()
    score = 0
    player_rect.midbottom = (WIDTH // 2, HEIGHT - 20)
    last_shot_time = pygame.time.get_ticks()
    last_alien_spawn_time = pygame.time.get_ticks()
    game_over = False

# Main game loop
while True:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_started:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_started = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    game_started = True

        elif game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    reset_game()
                elif no_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()

    if not game_started:
        screen.blit(start_bg_image, (0, 0))
        draw_text("Random Falling Aliens", WIDTH // 2, 100, 60, center=True)
        play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        pygame.draw.rect(screen, GREEN, play_button)
        draw_text("PLAY NOW", WIDTH // 2, HEIGHT // 2, 30, BLACK, center=True)
        draw_text("Press ENTER to Start", WIDTH // 2, HEIGHT // 2 + 80, 24, center=True)

    elif not game_over:
        # Draw static background
        screen.blit(background_image, (0, 0))

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        # Shooting
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and (current_time - last_shot_time > shoot_cooldown):
            bullet_rect = bullet_img.get_rect(midbottom=player_rect.midtop)
            bullets.append(bullet_rect)
            last_shot_time = current_time
            if shoot_sound:
                shoot_sound.play()

        # Spawn aliens
        if current_time - last_alien_spawn_time > alien_spawn_interval:
            spawn_alien()
            last_alien_spawn_time = current_time

        # Move bullets
        for bullet in bullets[:]:
            bullet.y += bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move aliens
        for alien in aliens[:]:
            alien.y += alien_fall_speed
            if alien.colliderect(player_rect):
                game_over = True
            elif alien.top > HEIGHT:
                aliens.remove(alien)
                score -= 5

        # Bullet collision with aliens
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if bullet.colliderect(alien):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 10
                    if enemy_killed_sound:
                        enemy_killed_sound.play()
                    break

        # Drawing
        screen.blit(player_img, player_rect)
        for alien in aliens:
            screen.blit(alien_img, alien)
        for bullet in bullets:
            screen.blit(bullet_img, bullet)
        draw_text(f"Score: {score}", 10, 10)

    else:
        screen.blit(game_over_bg_image, (0, 0))
        draw_text("Do you want to play again?", WIDTH // 2, HEIGHT // 3 - 30, 28, center=True)

        yes_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 3 + 10, 100, 40)
        no_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 3 + 10, 100, 40)
        draw_button(yes_button, "YES")
        draw_button(no_button, "NO")

    pygame.display.flip()
