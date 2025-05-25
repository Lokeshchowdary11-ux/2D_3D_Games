from ursina import *

app = Ursina()

player = Entity(model='cube', color=color.orange, position=(0, 0, 0), scale=1.5)

def change_color():
    player.color = color.random_color()

def input(key):
    change_color()

button = Button(text='Change Color', color=color.lime, scale=(0.3, 0.1), position=(0, 0.45))
button.on_click = change_color

bg_music = Audio('background.mp3', loop=True, autoplay=True)

app.run()
