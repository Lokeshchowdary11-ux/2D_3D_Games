from ursina import *
from random import uniform

app = Ursina()

# Game settings
score = 0
game_duration = 30
game_started = False
start_time = 0

# 📷 Background image
background = Entity(
    model='quad',
    texture='3D Bg image.jpg',   # Replace with your image file
    scale=(16, 9),
    z=1
)

# 📝 UI Texts
score_text = Text('', position=(-0.85, 0.45), scale=2, color=color.white, enabled=False)
timer_text = Text('', position=(0.7, 0.45), scale=2, color=color.yellow, enabled=False)

game_over_text = Text('', origin=(0, 0), scale=2, color=color.red, enabled=False)
restart_text = Text('Press Enter to Restart', position=(0, -0.1), origin=(0, 0), scale=1.5, enabled=False)

# 🔊 Sound
click_sound = Audio('Button click.wav', autoplay=False)  # Ensure this file exists in your folder

# 🟦 3D Button
button = Button(
    model='cube',
    color=color.azure,
    scale=(0.5, 0.2, 0.5),
    position=(0, 0, 0),
    collider='box',
    enabled=False
)

# 🌊 Floating animation setup
float_speed = 2
float_amplitude = 0.05
base_y = button.y

# ✨ Particle effect
def show_particles(pos):
    p = Entity(model='sphere', scale=0.1, color=color.orange, position=pos)
    p.animate_scale(0, duration=0.5)
    p.fade_out(duration=0.5)
    destroy(p, delay=0.5)

# ▶️ Start the game
def start_game():
    global game_started, start_time, score
    score = 0
    start_time = time.time()
    game_started = True

    play_button.enabled = False
    game_over_text.enabled = False
    restart_text.enabled = False

    button.enabled = True
    score_text.enabled = True
    timer_text.enabled = True

    score_text.text = f"Score: {score}"
    timer_text.text = f"Time: {game_duration}"
    button.color = color.azure
    button.position = (0, 0, 0)

# 🔁 Restart with Enter
def input(key):
    if key == 'enter' and not game_started:
        start_game()

# 🖱️ Button click logic
def increase_score():
    global score
    if not game_started or time.time() - start_time >= game_duration:
        return

    click_sound.play()

    score += 1
    score_text.text = f"Score: {score}"
    button.color = color.random_color()
    button.position = (uniform(-1, 1), 0, uniform(-1, 1))
    show_particles(button.position + Vec3(0, 0.2, 0))

button.on_click = increase_score

# 🔄 Game update loop
def update():
    global game_started

    if game_started:
        # Floating button animation
        button.y = base_y + sin(time.time() * float_speed) * float_amplitude

        # Countdown timer
        time_left = max(0, game_duration - int(time.time() - start_time))
        timer_text.text = f"Time: {time_left}"

        if time_left <= 0:
            end_game()

# 🛑 Game over logic
def end_game():
    global game_started
    game_started = False

    button.enabled = False
    score_text.enabled = False
    timer_text.enabled = False

    game_over_text.text = f"Game Over! Final Score: {score}"
    game_over_text.enabled = True
    restart_text.enabled = True

# ▶️ Play Now button
play_button = Button(
    text='Play Now',
    color=color.green,
    scale=(0.3, 0.1),
    position=(0, 0),
    on_click=start_game
)

app.run()
