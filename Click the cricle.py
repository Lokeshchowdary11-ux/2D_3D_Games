import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

background = pygame.image.load('bg image.jpg')
background = pygame.transform.scale(background, (600, 400))

score = 0
circle_radius = 30
circle_pos = (random.randint(50, 550), random.randint(50, 350))
circle_color = (255, 0, 0)

def get_random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

running = True
while running:
    screen.blit(background, (0, 0))
    pygame.draw.circle(screen, circle_color, circle_pos, circle_radius)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] - circle_pos[0])**2 + (mouse_pos[1] - circle_pos[1])**2 <= circle_radius**2:
                score += 1
                circle_pos = (random.randint(50, 550), random.randint(50, 350))
                circle_color = get_random_color()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
