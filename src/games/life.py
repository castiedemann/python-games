from random import random
from src.tile_game import TileGame

class Life(TileGame):
  def __init__(self):
    super().__init__(
      tileSize=10,
      tilesX=128,
      tilesY=72,
      title="Life",
      gridColor="green"
    )

    self.cells = {}
    self.init_random()

  def init_random(self):
    halfW = self.tilesX / 2
    halfH = self.tilesY / 2
    for tile in self.tiles:
      # More likely in the centerr
      probability = (1 - abs(halfW - tile["x"]) / halfW + 1 - abs(halfH - tile["y"]) / halfH) / 2
      if random() < 0.25 * probability:
        self.addCell(tile["x"], tile["y"])
  
  def addCell(self, x, y):
    index = self.get_tile_index(x, y)
    self.draw_tile_rect(x, y, "green")
    self.cells[index] = self.tiles[index]

  def removeCell(self, x, y):
    index = self.get_tile_index(x, y)
    self.clear_tile(x, y)
    del self.cells[index]

  def step(self):
    neighbourCounts = {}
    for index in self.cells:
      if index not in neighbourCounts:
        neighbourCounts[index] = 0
      tile = self.cells[index]
      self.countNeighbours(tile["x"], tile["y"], neighbourCounts)

    for index in neighbourCounts:
      tile = self.tiles[index]
      if index not in self.cells:
        if neighbourCounts[index] == 3:
          self.addCell(tile["x"], tile["y"])
      elif neighbourCounts[index] < 2 or neighbourCounts[index] > 3:
          self.removeCell(tile["x"], tile["y"])
    
    return True

  def countNeighbours(self, x, y, neighbourCounts):
    minX = max(x - 1, 0)
    maxX = min(x + 2, self.tilesX)
    minY = max(y - 1, 0)
    maxY = min(y + 2, self.tilesY)
    for xIndex in range(minX, maxX):
      for yIndex in range(minY, maxY):
        if xIndex != x or yIndex != y:
          index = self.get_tile_index(xIndex, yIndex)
          if index in neighbourCounts:
            neighbourCounts[index] += 1
          else:
            neighbourCounts[index] = 1

life = Life()
life.start()
