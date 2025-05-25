from ursina import *

app = Ursina()

player = Entity(model='cube', color=color.orange, position=(0, 0, 0), scale=1.5)

bg_sound = Audio('background.mp3', autoplay=False)

def on_button_click():
    player.color = color.random_color()
    btn.text = 'Clicked!'
    bg_sound.play()

btn = Button(text='Change Player Color', color=color.azure, scale=(0.3, 0.1), position=(0, 0.45))
btn.on_click = on_button_click

app.run()
