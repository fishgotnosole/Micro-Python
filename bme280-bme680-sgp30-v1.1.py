import time
import utime
from breakout_bme280 import BreakoutBME280
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from breakout_sgp30 import BreakoutSGP30
from pimoroni_i2c import PimoroniI2C
import picoexplorer as display

PINS_PICO_EXPLORER = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}
i2c = PimoroniI2C(**PINS_PICO_EXPLORER)

bme680 = BreakoutBME68X(i2c, 0x77)
bme280 = BreakoutBME280(i2c, 0x76)
sgp30 = BreakoutSGP30(i2c)

# setup pico explorer display 240x240 2-bytes per pixel (RGB565)
width = 240
height = 240
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)
display.clear()
display.update()

j = 0

while True:

    display.set_pen(0, 0, 64)
    display.rectangle(0, 0, 240, 240)
    
    temperature280, pressure280, humidity280, = bme280.read()
    temperature680, pressure680, humidity680, gas, status, _, _ = bme680.read()
    heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"
    air_quality = sgp30.get_air_quality()
    eCO2 = air_quality[BreakoutSGP30.ECO2]
    TVOC = air_quality[BreakoutSGP30.TVOC]
    air_quality_raw = sgp30.get_air_quality_raw()
    H2 = air_quality_raw[BreakoutSGP30.H2]
    ETHANOL = air_quality_raw[BreakoutSGP30.ETHANOL]
    
    # Calibration adjusments can be configured here
    temperature280 = temperature280 / 5 * 4
    temperature680 = temperature680 / 5 * 4
    pressure280 = pressure280 / 100 # Converts to hectoPascals
    pressure680 = pressure680 / 100 # Converts to hectoPascals 
    humidity280 = humidity280 / 4 * 3
    humidity680 = humidity680 / 4 * 3
    gas = round(gas / 100, 2)
 
    display.set_pen(255, 0, 0)
    display.text("280:", 0, 0, 100, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.2f}'.format(temperature280) + ' C', 70, 0, 240, 3)
    
    display.set_pen(255, 128, 0)
    display.text("680:", 0, 20, 100, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.2f}'.format(temperature680) + ' C', 70, 20, 240, 3)
    
    display.set_pen(0, 255, 0)
    display.text("280:", 0, 40, 100, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.1f}'.format(pressure280) + ' hPa', 70, 40, 240, 3)
    
    display.set_pen(192, 255, 0)
    display.text("680:", 0, 60, 100, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.1f}'.format(pressure680) + ' hPa', 70, 60, 240, 3)
    
    display.set_pen(0, 0, 255)
    display.text("280:", 0, 80, 100, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.1f}'.format(humidity280) + ' %RH', 70, 80, 240, 3)
    
    display.set_pen(0, 128, 255)
    display.text("680:", 0, 100, 100, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.1f}'.format(humidity680) + ' %RH', 70, 100, 240, 3)
    
    display.set_pen(224, 224, 0)
    display.text("GAS: ", 0, 160, 100, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.1f}'.format(gas) + ' Mohm', 70, 160, 240, 3)
    
    display.set_pen(224, 0, 224)
    display.text("co2:", 0, 120, 240, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.0f}'.format(eCO2) + ' ppm ', 70, 120, 240, 3)    

    display.set_pen(255, 0, 255)
    display.text("VOC:", 0, 140, 240, 3)
    display.set_pen(255, 255, 255)
    display.text('{:.0f}'.format(TVOC) + ' ppb', 70, 140, 240, 3)
    
    display.set_pen(192, 192, 0)
    display.text("Heater:", 0, 180, 240, 3)
    display.set_pen(192, 192, 192)
    display.text('{:.}'.format(heater) + '', 110, 180, 240, 3)
        
    # prints values to the terminal
    print("bme680: {:0.2f} °C, {:0.2f} hPa, {:0.2f} %RH, {:0.2f} MΩ, Heater: {}".format(temperature680, pressure680, humidity680, gas, heater))
    print("bme280: {:0.2f} °C, {:0.2f} hPa, {:0.2f} %RH".format(temperature280, pressure280, humidity280))
    
    '''print("bme680: {:0.2f} °C, {:0.2f} hPa, {:0.2f} %RH, {:0.2f} MΩ, Heater: {}".format(
        temperature680 / 4 * 3 - .5, pressure680 / 100, humidity680 / 4 * 3, gas / 100, heater
        ))    
    print("bme280: {:0.2f} °C, {:0.2f} hPa, {:0.2f} %RH".format(
        temperature280 / 4 * 3, pressure280 / 100, humidity280 / 4 * 3
        ))'''
    
    j += 1
    air_quality = sgp30.get_air_quality()
    eCO2 = air_quality[BreakoutSGP30.ECO2]
    TVOC = air_quality[BreakoutSGP30.TVOC]

    air_quality_raw = sgp30.get_air_quality_raw()
    H2 = air_quality_raw[BreakoutSGP30.H2]
    ETHANOL = air_quality_raw[BreakoutSGP30.ETHANOL]

    print(j, ": CO2 ", eCO2, " TVOC ", TVOC, ", raw ", H2, " ", ETHANOL, sep="")
    if j == 30:
        print("Resetting device")
        sgp30.soft_reset()
        time.sleep(0.5)
        print("Restarting measurement, waiting 15 secs before returning")
        sgp30.start_measurement(True)
        print("Measurement restarted, now read every second")
    
    display.set_pen(160, 160, 160)
    display.text("Counter:", 0, 200, 240, 3)
    display.set_pen(192, 192, 192)
    display.text(str(j), 0, 220, 240, 3)

    display.update()
    time.sleep(1)
