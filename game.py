#!/usr/local/bin/python3.10

import random
import turtle

turtle.Screen().setup(startx=800, width=640, height=640)
turtle.bgcolor('orange')

GRID_SIZE = 80
GRID_SPAN = 3
GRID_MAX = GRID_SIZE * GRID_SPAN

MOVE_BEAST_ODDS = 0.2
KARMA_MOVE = -20
KARMA_CAPTURE = 100

def line(x1, y1, x2, y2):
    turtle.up()
    turtle.goto(x1, y1)
    turtle.down()
    turtle.goto(x2, y2)

turtle.speed(0)
turtle.hideturtle()
turtle.color('dark orange')
turtle.width(15)

for i in range(-GRID_SPAN, GRID_SPAN+1):
    scaled_i = i * GRID_SIZE
    line(-GRID_MAX, scaled_i, GRID_MAX, scaled_i)
    line(scaled_i, -GRID_MAX, scaled_i, GRID_MAX)

def actor(image, *, color='black'):
    t = turtle.Turtle()
    if image.endswith('.gif'):
        turtle.register_shape(image)
    t.shape(image)
    t.color(color)
    t.up()
    return t

beast = actor('beast.gif')
player = actor('player.gif', color='white')
player.steps = 0
karma = actor('circle', color='gold')
karma.goto(0, GRID_MAX+42)

def move_player(dx, dy):
    x, y = player.position()
    player.goto(x + dx*GRID_SIZE, y + dy*GRID_SIZE)
    player.steps += 1
    attempt_capture()

def attempt_capture():
    if player.position() == beast.position():
        beast.circle(20, steps=7)
        update_karma(KARMA_CAPTURE)
        move_beast()
    else:
        update_karma(KARMA_MOVE)
        if random.random() < MOVE_BEAST_ODDS:
            move_beast()

def update_karma(dk):
    karma.forward(dk)
    karma_x, _ = karma.position()
    if karma_x >= GRID_MAX:
        end_game('Victory!')
    elif karma_x <= -GRID_MAX:
        end_game('Defeat...')

def end_game(message):
    player.write(
        message,
        align='center',
        font=('Helvetica', 64, 'bold'),
    )
    karma.write(
        f'{player.steps} steps',
        align='center',
        font=('Helvetica', 32, 'bold'),
    )
    for key in ('Up', 'Down', 'Left', 'Right'):
        turtle.onkey(None, key)

def move_beast():
    x = random.randint(-GRID_SPAN, GRID_SPAN)
    y = random.randint(-GRID_SPAN, GRID_SPAN)
    beast.goto(x*GRID_SIZE, y*GRID_SIZE)

turtle.listen()

turtle.onkey(lambda: move_player(0, 1), 'Up')
turtle.onkey(lambda: move_player(0, -1), 'Down')
turtle.onkey(lambda: move_player(-1, 0), 'Left')
turtle.onkey(lambda: move_player(1, 0), 'Right')

move_beast()

turtle.mainloop()
