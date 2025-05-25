from ursina import *

app = Ursina()

window.title = 'Maze Puzzle Game'
window.borderless = False
camera.orthographic = True
camera.fov = 12

maze = [
    "WWWWWWWWWWWWWWW",
    "W S     W     W",
    "W WWWWWW W W WW",
    "W W    W W W  W",
    "W W WW W W W TW",
    "W W    W W W  W",
    "W WWWW W W WWWW",
    "W    W W     TW",
    "WWW WW WWWWW WW",
    "W    W    T   W",
    "W WWWWWWWW WWWW",
    "W        G    W",
    "WWWWWWWWWWWWWWW"
]

tile_size = 1
player = None
walls = []
goal = None
traps = []

player_health = 3
health_text = Text(text=f'Health: {player_health}', position=window.top_left + Vec2(0.12, -0.05), origin=(0,0), scale=2, color=color.red)

maze_width = len(maze[0]) * tile_size
maze_height = len(maze) * tile_size
offset_x = -maze_width / 2 + tile_size / 2
offset_y = maze_height / 2 - tile_size / 2

for y in range(len(maze)):
    for x in range(len(maze[y])):
        char = maze[y][x]
        world_x = x * tile_size + offset_x
        world_y = -y * tile_size + offset_y

        if char == "W":
            wall = Entity(model='quad', color=color.gray, position=(world_x, world_y), scale=(1,1), collider='box')
            walls.append(wall)
        elif char == "S":
            player = Entity(model='quad', color=color.orange, position=(world_x, world_y), scale=(0.9, 0.9), collider='box')
        elif char == "G":
            goal = Entity(model='quad', color=color.green, position=(world_x, world_y), scale=(0.9, 0.9), collider='box')
        elif char == "T":
            trap = Entity(model='quad', color=color.red, position=(world_x, world_y), scale=(0.9, 0.9))
            traps.append(trap)

def reset_trap_color(trap_entity):
    trap_entity.color = color.red

def positions_equal(pos1, pos2, tol=0.01):
    return (abs(pos1.x - pos2.x) < tol) and (abs(pos1.y - pos2.y) < tol)

game_over = False

def input(key):
    global player_health, game_over
    if game_over or not player:
        return

    move = Vec2(0, 0)
    if key == 'up arrow':
        move.y = 1
    elif key == 'down arrow':
        move.y = -1
    elif key == 'left arrow':
        move.x = -1
    elif key == 'right arrow':
        move.x = 1
    else:
        return

    target_pos = player.position + Vec3(move.x, move.y, 0)

    for wall in walls:
        if positions_equal(wall.position, target_pos):
            return

    player.position = target_pos

    for trap in traps:
        if positions_equal(player.position, trap.position):
            player_health -= 1
            health_text.text = f'Health: {player_health}'
            print("⚠️ Trap triggered! Health -1")
            trap.color = color.orange
            invoke(reset_trap_color, trap, delay=0.5)

            if player_health <= 0:
                print("💀 You died! Game Over.")
                health_text.text = "You died! Game Over."
                game_over = True
            break

    if goal and positions_equal(player.position, goal.position):
        print("🎉 You reached the goal!")
        goal.color = color.yellow
        health_text.text = "🎉 You Win!"
        game_over = True

app.run()
