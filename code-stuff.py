import time
import gc

import board
import analogio
import displayio
from fourwire import FourWire

import adafruit_bme680
import adafruit_ssd1681
from adafruit_max1704x import MAX17048

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

# Create a bitmap with 2 colors
bitmap = displayio.Bitmap(128, 128, 3)  # 16x16 pixels, 2 colors

# Create a palette with the colors
palette = displayio.Palette(3)
palette[0] = 0x000000  # Black
palette[1] = 0xFFFFFF  # White
palette[2] = 0xFF0000  # Red

# fill white
for x in range(128):
    for y in range(128):
        bitmap[x, y] = 1

# Create the TileGrid using the bitmap and palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
tile_grid.x = 0  # Position on screen
tile_grid.y = 0

g.append(tile_grid)

display.root_group = g
display.refresh()

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

    time.sleep(1)
