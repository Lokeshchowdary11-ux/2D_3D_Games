from ursina import *

app = Ursina()

background = Entity(
    model='quad',
    texture='mouse.jpg',
    scale=(16, 9),
    z=1
)

bounce_sound = Audio("ball bounce sounds.wav", autoplay=False)

window.show_cursor = False

cursor_emoji = "🎯"
cursor = Text(text=cursor_emoji, color=color.white, origin=(0, 0), scale=3, background=True)

def update():
    cursor.position = Vec2(mouse.x, mouse.y)

def input(key):
    global cursor_emoji
    if key == '1':
        cursor_emoji = " smooth "
    elif key == '2':
        cursor_emoji = " smile"
    elif key == '3':
        cursor_emoji = "Magic "
    cursor.text = cursor_emoji

app.run()
