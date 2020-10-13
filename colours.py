# Script for mote light set for gently-undulating colour
# Will prompt for a colour name

import time
import math
from colorsys import hsv_to_rgb

from mote import Mote

DEFAULT = "pink"

COLORS = {
  "pink": 0.97,
  "purple": 0.8,
  "blue": 0.7,
  "green": 0.35,
  "red": 0.999,
  "yellow": 0.08
}

def get_color():
  print('We have these colours available:')
  for key in COLORS.keys():
    print(key)
  ans = input('Which colour are you using today?' + ' ')
  if ans.lower() in COLORS.keys():
    return COLORS[ans.lower()]
  else:
    return COLORS[DEFAULT]

# configure mote
mote = Mote()

mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

mote.clear()

# Set mode
colour = get_color()

# colours running
# Updated from: https://github.com/pimoroni/mote/blob/master/python/examples/rainbow.py
try:
  while True:
    h = time.time() * 100
    for channel in range(4):
      for pixel in range(16):
        hue = math.sin((h + (channel * 64) + (pixel * 4)) / 100) 
        r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/80 + colour, 1.0, 1.0)]
        mote.set_pixel(channel + 1, pixel, r, g, b)
    mote.show()
    time.sleep(0.01)

except KeyboardInterrupt:
    mote.clear()
    mote.show()