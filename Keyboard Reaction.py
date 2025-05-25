import pygame
import random
import time

pygame.init()
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Keyboard Reaction Game")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

bg_image = pygame.image.load("key board image.jpg")
bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)

keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
key_names = {pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT", pygame.K_UP: "UP", pygame.K_DOWN: "DOWN"}

score = 0
reaction_time = 0
new_key = random.choice(keys)
prompt_time = time.time()

running = True
while running:
    screen.blit(bg_image, (0, 0))

    text = font.render(f"Press: {key_names[new_key]}", True, (255, 0, 0))
    screen.blit(text, (200, 150))

    score_text = font.render(f"Score: {score}", True, (0, 100, 0))
    screen.blit(score_text, (230, 250))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == new_key:
                reaction_time = time.time() - prompt_time
                score += 1
                new_key = random.choice(keys)
                prompt_time = time.time()
            else:
                score = max(0, score - 1)

    clock.tick(60)

pygame.quit()
