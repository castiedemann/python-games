from tkinter import Canvas, Tk

FPS = 1000 // 60

class TileGame:
  def __init__(self, tileSize, tilesX, tilesY, title, gridColor = None):
    self.tileSize = tileSize
    self.tilesX = tilesX
    self.tilesY = tilesY
    self.title = title

    self.screenWidth = tileSize * tilesX
    self.screenHeight = tileSize * tilesY

    self.init_canvas()

    if gridColor != None:
      self.init_grid(gridColor)

    self.init_tiles()

  def init_canvas(self):
    self.widget = Tk()
    self.widget.geometry(f"{self.screenWidth}x{self.screenHeight}")
    self.widget.title(self.title)

    self.canvas = Canvas(self.widget, width=self.screenWidth, height=self.screenHeight)
    self.canvas.pack()
    self.canvas.create_rectangle(0, 0, self.screenWidth, self.screenHeight, fill="black")

  def init_tiles(self):
    self.tiles = [None] * self.tilesX * self.tilesY

    for x in range(0, self.tilesX):
      for y in range(0, self.tilesY):
        self.init_tile(x, y)

  def init_tile(self, x, y):
    index = self.get_tile_index(x, y)
    left = x * self.tileSize
    top = y * self.tileSize
    self.tiles[index] = {
      "canvasItemId": None,
      "rect": {
        "left": left,
        "top": top,
        "right": left + self.tileSize,
        "bottom": top + self.tileSize
      },
      "x": x,
      "y": y,
      "index": index
    }

  def init_grid(self, gridColor):
    for x in range(0, self.tilesX):
      self.canvas.create_line(
        x0=x,
        x1=x,
        y0=0,
        y1=self.screenHeight,
        fill=gridColor
      )

    for y in range(0, self.tilesY):
      self.canvas.create_line(
        x0=0,
        x1=self.screenWidth,
        y0=y,
        y1=y,
        fill=gridColor
      )
  
  def is_within_bounds(self, x, y):
    return x >= 0 and x < self.tilesX and y >= 0 and y < self.tilesY

  def is_empty(self, x, y):
    return self.is_within_bounds(x, y) and self.get_tile(x, y)["canvasItemId"] == None

  def for_each_tile(self, func):
    for x in range(0, self.tilesX):
      for y in range(0, self.tilesY):
        index = self.get_tile_index(x, y)
        func(x, y, index, self.tiles[index])

  def get_tile_index(self, x, y):
    return x + y * self.tilesX

  def get_tile(self, x, y):
    return self.tiles[self.get_tile_index(x, y)]

  def clear_tile(self, x, y):
    tile = self.get_tile(x, y)
    if tile["canvasItemId"] != None:
      self.canvas.delete(tile["canvasItemId"])
      tile["canvasItemId"] = None
  
  def draw_tile_rect(self, x, y, color):
    self.clear_tile(x, y)
    tile = self.get_tile(x, y)
    tile["canvasItemId"] = self.canvas.create_rectangle(
      tile["rect"]["left"],
      tile["rect"]["top"],
      tile["rect"]["right"],
      tile["rect"]["bottom"],
      fill=color,
      outline=color
    )

  def update(self):
    if not self.step():
      print("Game Over!")
      return
    self.widget.update()
    self.widget.after(FPS, self.update)

  def step(self):
    return False

  def on_key(self, e):
    print("key", e)

  def start(self):
    self.widget.bind("<Key>", self.on_key)
    self.widget.after(500, self.update)
    self.widget.mainloop()