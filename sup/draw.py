import board
import displayio
import adafruit_ssd1681
import analogio
from fourwire import FourWire
import time

# TODO could do labels and text, but i wont be able to use it on c anyway

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

main_group = displayio.Group()

# Create a bitmap with 2 colors
bitmap = displayio.Bitmap(16, 16, 2)  # 16x16 pixels, 2 colors

# Fill bitmap with a pattern (example: checkerboard)
for x in range(16):
    for y in range(16):
        if (x + y) % 2 == 0:
            bitmap[x, y] = 1  # Set to color index 1
        else:
            bitmap[x, y] = 0  # Set to color index 0

# Create a palette with the colors
palette = displayio.Palette(2)
palette[0] = 0x000000  # Black
palette[1] = 0xFF0000  # Red

# Create the TileGrid using the bitmap and palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
tile_grid.x = 20  # Position on screen
tile_grid.y = 20

# Add the TileGrid to the main group to display it
main_group.append(tile_grid)

display.root_group = main_group
display.refresh()

time.sleep(180)
