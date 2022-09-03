from random import choice, randint
from time import time
from tkinter import Canvas, Tk

CELL_SIZE = 40
GAME_WIDTH = 16
GAME_HEIGHT = 16
FPS = 1000 // 60
SCREEN_WIDTH = CELL_SIZE * GAME_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GAME_HEIGHT

widget = Tk()
widget.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
widget.title("Snake")

canvas = Canvas(widget, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()
canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill="black")

for x in range(0, SCREEN_WIDTH, CELL_SIZE):
  canvas.create_line(x, 0, x, SCREEN_HEIGHT, fill="gray")

for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
  canvas.create_line(0, y, SCREEN_WIDTH, y, fill="gray")

cells = {}

def getCellKey(x, y):
  return x + y * GAME_WIDTH

for x in range(0, GAME_WIDTH):
  for y in range(0, GAME_HEIGHT):
    cells[getCellKey(x, y)] = None

directions = ["up", "right", "down", "left"]
direction = choice(directions)
minSpeed = 2
maxSpeed = 20
minSnakeLen = 3
maxSnakeLen = GAME_WIDTH * GAME_HEIGHT
lastMove = 0

movement = {
  "up": {
    "x": 0,
    "y": -1
  },
  "right": {
    "x": 1,
    "y": 0
  },
  "down": {
    "x": 0,
    "y": 1
  },
  "left": {
    "x": -1,
    "y": 0
  }
}

snake = []
pending = []
fruit = {
  "x": 0,
  "y": 0
}

def isVacant(x, y):
  if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
    return False
  return cells[getCellKey(x, y)] == None

def drawCell(x, y, fill):
  if not isVacant(x, y):
    clearCell(x, y)
  cells[getCellKey(x, y)] = canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=fill)

def clearCell(x, y):
  if not isVacant(x, y):
    key = getCellKey(x, y)
    canvas.delete(cells[key])
    cells[key] = None

def getRandomAvailableCell():
  available = {}
  for x in range(0, GAME_WIDTH):
    for y in range(0, GAME_HEIGHT):
      if isVacant(x, y):
        available[getCellKey(x, y)] = { "x": x, "y": y }
  return choice(list(available.values()))

def updateFruit():
  cell = getRandomAvailableCell()
  if cell == None:
    return False

  fruit["x"] = cell["x"]
  fruit["y"] = cell["y"]
  drawCell(cell["x"], cell["y"], "green")
  return True

def addPart(x, y, isHead = False):
  drawCell(x, y, "gray")
  part = {
    "x": x,
    "y": y
  }
  if isHead:
    snake.insert(0, part)
  else:
    snake.append(part)

def shift():
  snakeLen = snake.__len__()

  oldHead = snake[0]
  oldTail = snake[snakeLen - 1]

  newHeadX = oldHead["x"] + movement[direction]["x"]
  newHeadY = oldHead["y"] + movement[direction]["y"]

  isFruit = newHeadX == fruit["x"] and newHeadY == fruit["y"]
  if not isFruit and not isVacant(newHeadX, newHeadY):
    return False

  addPart(newHeadX, newHeadY, True)

  for index, count in enumerate(pending):
      pending[index] = count - 1

  if pending.__len__() > 0 and pending[0] == 0:   
    pending.pop(0)
  else:
    snake.pop()
    clearCell(oldTail["x"], oldTail["y"])

  if isFruit:
    drawCell(newHeadX, newHeadY, "white")
    updateFruit()
    pending.append(snakeLen)
  
  return True

def update():
  if not step():
    print("Game Over!")
    return
  widget.update()
  widget.after(FPS, update)

def step():
  global lastMove
  now = time()
  elapsed = now - lastMove
  snakeLen = snake.__len__()
  snakePercent =  (snakeLen - minSnakeLen) / (maxSnakeLen - minSnakeLen)
  speed = minSpeed + (maxSpeed - minSpeed) * snakePercent
  if elapsed > 1 / speed:
    if not shift():
      return False
    lastMove = now
  return True

def setDirection(newDirection):
  global direction, lastMove
  if direction == newDirection or directions.index(direction) % 2 != directions.index(newDirection) % 2:
    direction = newDirection
    lastMove = 0

def onUp(e):
  setDirection("up")
def onDown(e):
  setDirection("down")
def onRight(e):
  setDirection("right")
def onLeft(e):
  setDirection("left")

widget.bind("<Up>", onUp)
widget.bind("<Right>", onRight)
widget.bind("<Down>", onDown)
widget.bind("<Left>", onLeft)

updateFruit()

initX = GAME_WIDTH // 2
initY = GAME_HEIGHT // 2
for i in range(0, minSnakeLen):
  addPart(initX - movement[direction]["x"] * i, initY - movement[direction]["y"] * i)

update()

widget.mainloop()
