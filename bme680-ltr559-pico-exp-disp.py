import time
import utime
import picoexplorer as display
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from breakout_ltr559 import BreakoutLTR559
from pimoroni_i2c import PimoroniI2C

# Configure breakouts and sensors
PINS_PICO_EXPLORER = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}
i2c = PimoroniI2C(**PINS_PICO_EXPLORER)
bme = BreakoutBME68X(i2c)
ltr = BreakoutLTR559(i2c)

# Setup pico explorer display 240x240 2-bytes per pixel (RGB565)
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)
display.clear()
display.update()
print("Taking readings...")

while True:
    
    temperature, pressure, humidity, gas, status, _, _ = bme.read(heater_temp=250, heater_duration=50)
    heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"
    light = ltr.get_reading()
    
    # Calibration adjusments can be configured here
    pressurehpa = pressure / 100 # Converts to hectoPascals
    temperature = temperature / 2
    pressure = pressure - 1.0
    humidity = humidity - 14.3
    gas = round(gas / 100)
 
    display.set_pen(0, 0, 128)
    display.rectangle(0, 0, 240, 240)
    display.set_pen(255, 255, 255)
    display.text("Env & Lux", 25, 10, 240, 4)
        
    display.set_pen(255, 0, 0)
    display.text("Temp", 10, 50, 100, 3)
    display.set_pen(224, 224, 224)
    display.text('{:.1f}'.format(temperature) + ' C', 90, 50, 240, 3)
    
    display.set_pen(0, 255, 0)
    display.text("Pres", 10, 80, 100, 3)
    display.set_pen(224, 224, 224)
    display.text('{:.1f}'.format(pressurehpa) + ' hPa', 90, 80, 240, 3)
    
    display.set_pen(0, 128, 255)
    display.text("Humi", 10, 110, 100, 3)
    display.set_pen(224, 224, 224)
    display.text('{:.1f}'.format(humidity) + ' %', 90, 110, 240, 3)
    
    display.set_pen(255, 255, 0)
    display.text(" Lux", 10, 140, 240, 3)
    display.set_pen(224, 224, 224)
    display.text(str(light[BreakoutLTR559.LUX]), 90, 140, 240, 3)
    
    display.set_pen(192, 192, 192)
    display.text(" Air", 10, 170, 240, 3)
    display.set_pen(224, 224, 224)
    display.text('{:.0f}'.format(gas) + '.M Ohm', 90, 170, 240, 3)
    
    display.set_pen(144, 144, 144)
    display.text("Heat", 10, 200, 100, 3)
    display.set_pen(224, 224, 224)
    display.text(str(heater, _), 90, 200, 240, 3)
    
    display.update()
    time.sleep(.25)
    
    # Printing of values to terminal needs fixing to add light as well. Issues with formatting string (fstring)
'''    
    print("{:0.2f}c, {:0.2f}hPa, {:0.2f}%, {:0.2f} %, Heater: {}, Light: {}".format(temperature, pressurehpa, humidity, gas, heater, light))
    print(str(light[BreakoutLTR559.LUX]))
'''    
