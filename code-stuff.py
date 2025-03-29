import time

import board

import adafruit_bme680
import gc
import analogio

import time

import board
import displayio
from fourwire import FourWire

import adafruit_ssd1681

displayio.release_displays()

spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.D5
epd_busy = board.D6

display_bus = FourWire(spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000)
time.sleep(1)

display = adafruit_ssd1681.SSD1681(
    display_bus,
    width=200,
    height=200,
    busy_pin=epd_busy,
    highlight_color=0xFF0000,
    rotation=180,
)

g = displayio.Group()

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25
# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

with open("/display-ruler.bmp", "rb") as f:
    pic = displayio.OnDiskBitmap(f)
    # CircuitPython 7 compatible only
    t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    g.append(t)

    display.root_group = g
    display.refresh()

    time.sleep(30)

while True:
    print("\nTemperature: %0.1f F" % ((bme680.temperature + temperature_offset) * 9 / 5 + 32))
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)

    mem_usage = gc.mem_alloc() / (gc.mem_alloc()+gc.mem_free()) * 100
    bat = analogio.AnalogIn(board.A6)

    print("mem: {:.2f}%".format(mem_usage))
    print("bat: {:.2f}%".format(bat.value / 65535 * 100))
    print("bat: {:.2f}V".format(bat.value / 65535 * 3.3))

    time.sleep(1)
