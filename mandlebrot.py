# based on initial code demo for the PiMoroni PicoDisplay for the RaspberyPiPico
# Forked from SpiderMaf, https://github.com/SpiderMaf/PiPicoDsply/blob/main/brot.py
# Have stuck to using base 0/8/16/32/64/128/255 values where possible. Higher iteration values will yield longer compute/render times.
# original comments left starting in lowercase

# Import
import time
import picoexplorer as display 

# Set up display
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

# Set the iteration count
iterations = 128

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
zoom = 1.09

# Set up the Plot window
RealStart = -2 * zoom
RealEnd= 1 * zoom
ImaginaryStart = -1 * zoom
ImaginaryEnd = 1 * zoom

#one of the issues on the video was it was displaying the old images whilst generating the new one. So added the update below to send a clear screen to the display
display.clear()
display.update()

# Define Go
Go = True

# Define timer functions
timerstart = time.time()
timerend = time.time()
timerstop = time.cancel()

# Compute and display the mandlebrot fractal, in a fetching blue/black scheme
while True:
    for x in range(0, width):
        for y in range(0, height):
            c = complex(RealStart + (x / width) * (RealEnd - RealStart),ImaginaryStart + (y / height) * (ImaginaryEnd - ImaginaryStart))
            m = mandelbrot(c)
            colour = 255 - int(m * 255 / iterations)
            colour = display.set_pen(0, 0, colour)
            display.pixel(x, y)
        display.update()  
    print("Completed in: "(timerend - timerstart), "Seconds")
    Go = False

exit()
