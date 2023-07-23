#!/usr/local/bin/python3.7

import itertools
import time
import tkinter as tk
import random
import sys

MINS = 60
try:
    minutes = int(sys.argv[1])
except:
    minutes = 45
EXPIRES = time.time() + MINS * minutes

CANVAS_WIDTH = 120
CANVAS_HEIGHT = 60
CANVAS_CENTER_X = CANVAS_WIDTH // 2
CANVAS_CENTER_Y = CANVAS_HEIGHT // 2

root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparent", True)
root.config(bg='systemTransparent')
root.lift()

canvas = tk.Canvas(
    root,
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    bg='systemTransparent',
    bd=0,
    highlightthickness=0,
)
canvas.pack()
canvas_items = []

text_deltas = list(
    itertools.product((-1, 0, 1), (-1, 0, 1))
)
text_deltas.remove((0, 0))

def display(s, fg='white', bg='black',
            font=('Helvetica', 32, 'bold')):
    for dx, dy in text_deltas:
        canvas_items.append(canvas.create_text(
            CANVAS_CENTER_X+dx,
            CANVAS_CENTER_Y+dy,
            text=s,
            fill=bg,
            font=font,
        ))
    canvas_items.append(canvas.create_text(
        CANVAS_CENTER_X,
        CANVAS_CENTER_Y,
        text=s,
        fill=fg,
        font=font,
    ))

x = root.winfo_screenwidth() - canvas.winfo_reqwidth()
y = root.winfo_screenheight() - canvas.winfo_reqheight()
root.geometry(f'+{x}+{y}')

def time_format(seconds):
    mins, secs = divmod(abs(seconds), MINS)
    return f'{mins}:{secs:02d}'

def tick():
    delta = round(EXPIRES - time.time())
    time_str = time_format(delta)
    for item_id in canvas_items:
        canvas.itemconfig(item_id, text=time_str)
    if delta < 0:
        canvas.configure(bg='red')
    else:
        canvas.pack_forget()
        canvas.pack()
        root.update()
    x = root.winfo_screenwidth() - canvas.winfo_reqwidth()
    y = root.winfo_screenheight() - canvas.winfo_reqheight()
    root.geometry(f'+{x}+{y}')
    canvas.after(random.randint(10_500, 21_000), tick)

display('')
tick()
root.mainloop()
