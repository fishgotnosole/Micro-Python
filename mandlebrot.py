# based on initial code demo for the PiMoroni PicoDisplay for the RaspberyPiPico
# Forked from SpiderMaf, https://github.com/SpiderMaf/PiPicoDsply/blob/main/brot.py
# Have tried to use base 0/8/16/32/64/128 etc values where possible. 
# original comments left starting in lowercase

# Import
import utime
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER, PEN_RGB565

# Set up display
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER, pen_type=PEN_RGB565)
display.set_backlight(1.0)
width, height = display.get_bounds()
display.clear()

#define pen colours here
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
GREY = display.create_pen(192, 192, 192)
RED = display.create_pen(255, 0, 0)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 224, 0)
MIDBLUE = display.create_pen(0, 192, 224)
BLUE = display.create_pen(0, 64, 255)
DARKBLUE = display.create_pen(0, 0, 64)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)

# Set the iteration count, in a whole number. Higher iteration values will yield longer compute/render times.
# Low values will compute faster but with less visual qualty.
iterations = 32

# Define mandlebrot function
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iterations:
        z = z*z + c
        n += 1
    return n

# Allow zooming, for best results can be left in region of 1.0
'''change the zoom below to zoom in - the smaller the number the greater the zoom.
zoom too much on the wrong part may give no visible part of the fractal on the display
the smaller the zoom amount the longer the picture may take to generate.'''
zoom = 1.1

# Set up the Plot window
RealStart = -2 * zoom
RealEnd= 1 * zoom
ImaginaryStart = -1 * zoom
ImaginaryEnd = 1 * zoom

# one of the issues on the video was it was displaying the old images whilst generating the new one.
# so added the update below to send a clear screen to the display
display.set_pen(BLACK)
display.clear()
display.update()

# Compute and display the mandlebrot fractal, in a fetching Black, grey & white scheme
for q in range(1):
        the_start = utime.ticks_ms()
        for x in range(0, width):
            for y in range(0, height):
                c = complex(RealStart + (x / width) * (RealEnd - RealStart), ImaginaryStart + (y / height) * (ImaginaryEnd - ImaginaryStart))
                m = mandelbrot(c)
                colour = 255 - int(m * 255 / iterations)
                PLOTBLUE = display.create_pen(colour, colour, colour)
                colour = display.set_pen(PLOTBLUE)
                display.pixel(x, y)
            display.update()
            the_end = utime.ticks_ms()

print("Render stats:", (iterations), "iterations", (the_end - the_start) /1000, "secs")
print("Render stats:", (iterations), "iterations", (the_end - the_start) /60000, "mins")

