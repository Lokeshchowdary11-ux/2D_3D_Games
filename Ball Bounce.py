from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

app = Ursina()

ground = Entity(model='quad', scale=(16, 0.2), color=color.gray, position=(0, -4))
ball = Entity(model='circle', color=color.orange, scale=0.5, position=(0, 3))

jump_sound = Audio('ball sound.wav', autoplay=False)

gravity = -0.01
bounce_factor = 0.8
velocity_y = 0
direction = 1

def update():
    global velocity_y
    velocity_y += gravity
    ball.y += velocity_y
    if ball.y - ball.scale_y / 2 <= ground.y + ground.scale_y / 2:
        ball.y = ground.y + ground.scale_y / 2 + ball.scale_y / 2
        velocity_y = -velocity_y * bounce_factor
    if abs(velocity_y) < 0.005 and ball.y <= ground.y + ground.scale_y / 2 + ball.scale_y / 2 + 0.01:
        velocity_y = 0

def input(key):
    global velocity_y, direction
    if key == 'space':
        velocity_y = 0.2
        ball.x += direction * 1.5
        direction *= -1
        jump_sound.play()
    if key == 'r':
        ball.position = (0, 3)
        velocity_y = 0
        direction = 1

app.run()
