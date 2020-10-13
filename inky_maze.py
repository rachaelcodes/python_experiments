# Script for an inky Pi hat to draw a randomly-generated maze

from PIL import Image, ImageDraw
from inky import InkyPHAT
import math, random

print("""Inky pHAT maze:

Generate a maze on the inky pHAT

""")

# setup file
inky_display = InkyPHAT('red')
scale_size = 1
padding = 0

width = inky_display.WIDTH
height = inky_display.HEIGHT
inky_display.set_border(inky_display.RED)

im = Image.new('P', (width, height))
draw = ImageDraw.Draw(im)

# setup image
w = 10
cols = math.floor(width / w)
rows = math.floor(height / w)

grid = []
stack = []

# utility functions
def index(i, j):
  if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
    return False
  return int(i) + int(j * cols)

def removeWalls(a, b):
  x = a.i - b.i
  if x == 1:
    a.walls[3] = False
    b.walls[1] = False
  elif x == -1:
    a.walls[1] = False
    b.walls[3] = False
  
  y = a.j - b.j
  if y == 1:
    a.walls[0] = False
    b.walls[2] = False
  elif y == -1:
    a.walls[2] = False
    b.walls[0] = False

# individual cell
class Cell:
  def __init__(self, i, j):
    self.i = i
    self.j = j
    self.walls = [True, True, True, True]
    self.visited = False

  def checkNeighbours(self):
    neighbours = []
    topIndex = index(self.i, self.j-1)
    rightIndex = index(self.i+1, self.j)
    bottomIndex = index(self.i, self.j+1)
    leftIndex = index(self.i-1, self.j)

    if topIndex and (not grid[topIndex].visited):
      neighbours.append(grid[topIndex])
    if rightIndex and (not grid[rightIndex].visited):
      neighbours.append(grid[rightIndex])
    if bottomIndex and (not grid[bottomIndex].visited):
      neighbours.append(grid[bottomIndex])
    if leftIndex and (not grid[leftIndex].visited):
      neighbours.append(grid[leftIndex])

    if (len(neighbours) > 0):
      r = math.floor(random.randint(0, len(neighbours)-1))
      return neighbours[r]
    else:
      return None

  def show(self):
    x = self.i * w
    y = self.j * w

    if self.walls[0]:
      draw.line((x, y, x+w, y), fill=inky_display.BLACK, width=1)
    if self.walls[1]:
      draw.line((x+w, y, x+w, y+w), fill=inky_display.BLACK, width=1)
    if self.walls[2]:
      draw.line((x+w, y+w, x, y+w), fill=inky_display.BLACK, width=1)
    if self.walls[3]:
      draw.line((x, y+w, x, y), fill=inky_display.BLACK, width=1)

# setup grid
for j in range(0, rows):
  for i in range(0, cols):
    cell = Cell(i, j)
    grid.append(cell)

current = grid[0]
stack.append(current)

# run maze calculations
while len(stack) > 0:
  next = current.checkNeighbours()
  if next:
    next.visited = True
    stack.append(current)
    removeWalls(current, next)
    current = next
  else:
    current = stack.pop()

# drawing
for k in range(0, len(grid)):
  grid[k].show()

inky_display.set_image(im)
inky_display.show()