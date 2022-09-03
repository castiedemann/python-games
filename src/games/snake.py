from operator import indexOf
from random import choice, randint
from time import time
from tkinter import Canvas, Tk
from src.tile_game import TileGame

DIRECTIONS = ["up", "right", "down", "left"]
DIRECTION_VECTOR = {
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

def isHorizontal(direction):
  return DIRECTIONS.index(direction) % 2 == 1

TILE_SIZE = 40
TILES_X = 16
TILES_Y = 16
MIN_SPEED = 2
MAX_SPEED = 20
START_SNAKE_LEN = 3

class Snake(TileGame):
  def __init__(self):
    super().__init__(
      tileSize=TILE_SIZE,
      tilesX=TILES_X,
      tilesY=TILES_Y,
      title="Snake"
    )

    self.direction = choice(DIRECTIONS)
    self.lastMoveTime = 0
    self.pendingGrowCounters = []
    self.fruit = self.tiles[0]
    self.snake = []

    self.init_snake()
    self.update_fruit()

  def init_snake(self):
    vec = DIRECTION_VECTOR[self.direction]
    initX = TILES_X // 2 - vec["x"] * START_SNAKE_LEN
    initY = TILES_Y // 2 - vec["y"] * START_SNAKE_LEN
    for i in range(0, START_SNAKE_LEN):
      self.extend_snake(initX + vec["x"] * i, initY + vec["y"] * i)

  def step(self):
    now = time()
    elapsed = now - self.lastMoveTime
    speed = self.calculateSpeed()
    if elapsed > 1 / speed:
      if not self.shift():
        return False
      self.lastMoveTime = now
    return True
  
  def calculateSpeed(self):
    snakeLen = self.snake.__len__()
    maxSnakeLen = self.tilesX * self.tilesY
    snakePercent =  (snakeLen - START_SNAKE_LEN) / (maxSnakeLen - START_SNAKE_LEN)
    return MIN_SPEED + (MAX_SPEED - MIN_SPEED) * snakePercent

  def shift(self):
    snakeLen = self.snake.__len__()

    oldHead = self.snake[0]
    oldTail = self.snake[snakeLen - 1]

    newHeadX = oldHead["x"] + DIRECTION_VECTOR[self.direction]["x"]
    newHeadY = oldHead["y"] + DIRECTION_VECTOR[self.direction]["y"]

    if not self.is_within_bounds(newHeadX, newHeadY):
      return False
    
    newHead = self.get_tile(newHeadX, newHeadY)
    isFruit = newHead == self.fruit
    if not isFruit and not self.is_empty(newHeadX, newHeadY):
      return False

    self.extend_snake(newHeadX, newHeadY)

    for index, count in enumerate(self.pendingGrowCounters):
        self.pendingGrowCounters[index] = count - 1

    if self.pendingGrowCounters.__len__() > 0 and self.pendingGrowCounters[0] == 0:   
      self.pendingGrowCounters.pop(0)
    else:
      self.snake.pop()
      self.clear_tile(oldTail["x"], oldTail["y"])

    if isFruit:
      self.draw_tile_snake(newHeadX, newHeadY, "green")
      self.update_fruit()
      self.pendingGrowCounters.append(snakeLen)
    
    return True
    
  def get_random_available_tile(self):
    available = []
    for tile in self.tiles:
      if tile["canvasItemId"] == None:
        available.append(tile)
    return choice(available)

  def update_fruit(self):
    tile = self.get_random_available_tile()
    if tile != None:
      self.fruit = tile
      self.draw_tile_rect(tile["x"], tile["y"], "green")

  def extend_snake(self, x, y):
    self.draw_tile_snake(x, y)
    tile = self.get_tile(x, y)
    self.snake.insert(0, tile)

  def draw_tile_snake(self, x, y, color = "gray"):
    self.clear_tile(x, y)
    tile = self.get_tile(x, y)
    isHor = isHorizontal(self.direction)
    vec = DIRECTION_VECTOR[self.direction]
    offset = 3
    offsetW = offset if not isHor else 0
    offsetH = offset if isHor else 0
    offsetX = -vec["x"] * offset
    offsetY = -vec["y"] * offset
    
    tile["canvasItemId"] = self.canvas.create_rectangle(
      tile["rect"]["left"] + offsetW + offsetX,
      tile["rect"]["top"] + offsetH + offsetY,
      tile["rect"]["right"] - offsetW + offsetX,
      tile["rect"]["bottom"] - offsetH + offsetY,
      fill=color,
      outline=color
    )
  
  def set_direction(self, newDirection):
    if self.direction == newDirection or isHorizontal(self.direction) != isHorizontal(newDirection):
      self.direction = newDirection
      self.lastMoveTime = 0

  def on_key(self, e):
    direction = e.keysym.split().pop().lower()
    if DIRECTIONS.index(direction) != -1:
      self.set_direction(direction)

snake = Snake()
snake.start()
