import time
import gc

import board
import analogio
import displayio
from fourwire import FourWire

import adafruit_bme680
import adafruit_ssd1681
from adafruit_max1704x import MAX17048

class Spritesheet:
    def __init__(self, resource):
        self.resource = resource
    
    def __enter__(self):
        print(f"Acquiring {self.resource}")
        return self.resource  # Return value is assigned to variable after 'as'
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing {self.resource}")
        return False

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


# TODO test all colors in ruler
sprites = [
    open(f"/sprites/{i}.bmp", "rb") for i in [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
                                              'bat-low', 'bat', 'dot', 
                                              'hum-high', 'hum-low', 'hum', 
                                              'pres-high', 'pres-low', 'pres', 
                                              'temp-high', 'temp-low', 'temp' ]
]

for i, f in enumerate(sprites):
    pic = displayio.OnDiskBitmap(f)
    tile_grid = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    # convert i to x y position
    tile_grid.x = int(i % 12) * 16
    tile_grid.y = int(i / 12) * 16
    g.append(tile_grid)

temp = ((bme680.temperature + temperature_offset) * 9 / 5 + 32)
for i, c in enumerate(f"{temp}"):
    if c != ".":
        pic = displayio.OnDiskBitmap(sprites[int(c)])
        tile_grid = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
        tile_grid.x = int(i % 12) * 16
        tile_grid.y = 48
        g.append(tile_grid)

display.root_group = g
display.refresh()

for f in sprites:
    f.close()

# battery
max17048 = MAX17048(i2c)

while True:
    print("\nTemperature: %0.1f F" % ((bme680.temperature + temperature_offset) * 9 / 5 + 32))
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude: %0.2f meters" % bme680.altitude)

    mem_usage = gc.mem_alloc() / (gc.mem_alloc()+gc.mem_free()) * 100

    print("mem: {:.2f}%".format(mem_usage))
    print(f"Battery voltage: {max17048.cell_voltage:.2f} V")
    print(f"Battery percentage: {max17048.cell_percent:.1f} %")

    time.sleep(180)
