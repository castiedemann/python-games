from random import random
from time import sleep
from tkinter import Canvas, Tk

GRID_SIZE = 10
FPS = 1000 // 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

cells = {}

widget = Tk()
widget.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
widget.title("Game of life")

canvas = Canvas(widget, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()
canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill="black")

for x in range(0, SCREEN_WIDTH, GRID_SIZE):
  canvas.create_line(x, 0, x, SCREEN_HEIGHT, fill="green")

for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
  canvas.create_line(0, y, SCREEN_WIDTH, y, fill="green")

def getCellKey(x, y):
  return x + y * SCREEN_WIDTH

def addCell(x, y):
  key = getCellKey(x, y)
  cells[key] = canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, fill="green")

def removeCell(x, y):
  key = getCellKey(x, y)
  canvas.delete(cells[key])
  del cells[key]

for x in range(0, SCREEN_WIDTH // GRID_SIZE):
  for y in range(0, SCREEN_HEIGHT // GRID_SIZE):
    if random() < 0.5:
      addCell(x, y)

def update():
  step()
  widget.update()
  widget.after(FPS, update)

def countNeighbours(x, y, neighbourCounts):
  for i in range(-1, 2):
    for j in range(-1, 2):
      if i == 0 and j == 0:
        continue
      neighbourKey = getCellKey(x + i, y + j)
      if neighbourKey in neighbourCounts:
        neighbourCounts[neighbourKey] += 1
      else:
        neighbourCounts[neighbourKey] = 1

def step():
  neighbourCounts = {}
  for key in cells:
    if key not in neighbourCounts:
      neighbourCounts[key] = 0
    x = key % SCREEN_WIDTH
    y = key // SCREEN_WIDTH
    countNeighbours(x, y, neighbourCounts)

  for key in neighbourCounts:
    x = key % SCREEN_WIDTH
    y = key // SCREEN_WIDTH
    if key not in cells:
      if neighbourCounts[key] == 3:
        addCell(x, y)
    elif neighbourCounts[key] < 2 or neighbourCounts[key] > 3:
        removeCell(x, y)

update()

widget.mainloop()
