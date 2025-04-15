import time
import gc
import os

import board
import displayio
from fourwire import FourWire
import digitalio
import board
import storage

import adafruit_bme680
import adafruit_ssd1681
from adafruit_max1704x import MAX17048
import adafruit_sdcard
from adafruit_pcf8523.pcf8523 import PCF8523

settings = {
    'poll': 1, # seconds
    'refresh': 0, # seconds (0 = asap)
    'temp_offset': -5, # degrees
    'sea_level_pressure': 1013.25, # hPa
    'appearance': 1, # 0 = black, 1 = white
    'military_time': False, # 0 = 12 hour, 1 = 24 hour
}

class SpriteRenderer:
    def __init__(self, display):
        # TODO using map, but would like list or something. can deal with it in c
        # TODO dont like usage.bmp
        self.files = {
            img: f"/sprites/{img}.bmp" for img in [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
                                                    'alt', 'bat-low', 'bat', 'dot', 'minus',
                                                    'hum-high', 'hum-low', 'hum', 
                                                    'pres-high', 'pres-low', 'pres', 
                                                    'temp-high', 'temp-low', 'temp',
                                                    'err', 'gas', 'per', 'storage', 'time', 'usage', 'colon' ]
        }
        self.sprites = {}
        self.charset = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'a': 'alt', 'c': 'bat-low', 'b': 'bat', '.': 'dot', '-': 'minus',
            'd': 'hum-high', 'l': 'hum-low', 'h': 'hum',
            'n': 'pres-high', 'l': 'pres-low', 'p': 'pres',
            'j': 'temp-high', 'k': 'temp-low', 't': 'temp',
            'e': 'err', 'g': 'gas', '%': 'per', 's': 'storage', 'u': 'usage',
            'x': 'time', ':': 'colon',
        }
        self.display = display
    
    def __enter__(self):
        self.g = displayio.Group()
        return self  # Return value is assigned to variable after 'as'
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.display.root_group = self.g
        self.display.refresh()

        # have to close after refresh otherwise it will not show up
        for f in self.sprites:
            self.sprites[f].close()
        return False
    
    def write(self, data, x, y):
        for i, c in enumerate(f"{data}"):
            if c == ' ':
                continue
            pic = displayio.OnDiskBitmap(self._get(c))
            tile_grid = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
            tile_grid.x = x + int(i % 12) * 16
            tile_grid.y = y
            self.g.append(tile_grid)
    
    def _get(self, s):
        if s not in self.sprites:
            try:
                self._load(s)
            except ValueError:
                return self._get('e')
        return self.sprites[s]

    def _load(self, s):
        if s not in self.charset:
            raise ValueError(f"Sprite {s} not found")
        self.sprites[s] = open(self.files[self.charset[s]], "rb")
    
    def square(self, x, y, w, h, color=0xFFFFFF):
        # Create a bitmap with the desired width and height
        bitmap = displayio.Bitmap(w, h, 1)
        palette = displayio.Palette(1)
        palette[0] = color

        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette, x=x, y=y)
        self.g.append(tile_grid)

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

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25
# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = 0#-5

# sd card
sd_cs = digitalio.DigitalInOut(board.D11)
sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
samples = []

# sd_enable = digitalio.DigitalInOut(board.D10)
# sd_enable.direction = digitalio.Direction.OUTPUT
# # To enable SD card
# sd_enable.value = True

# battery
max17048 = MAX17048(i2c)
# Real Time Clock
rtc = PCF8523(i2c)

if False:  # change to True if you want to set the time!
    #                     year, mon, mday, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2024, 4,   14,   12+9, 10,  11,  0,    -1,   -1))
    rtc.datetime = t

# create the file if it doesn't exist
try:
    with open("/sd/log.csv", "r") as f:
        pass
except OSError:
    with open("/sd/log.csv", "w") as f:
        f.write("time,temp,humidity,pressure,gas,altitude,mem_usage,battery_voltage,battery_percent\n")

while True:
    temp = ((bme680.temperature + temperature_offset) * 9 / 5 + 32)
    mem_usage = gc.mem_alloc() / (gc.mem_alloc()+gc.mem_free()) * 100

    if display.time_to_refresh == 0:
        with SpriteRenderer(display) as sprite_renderer:
            sprite_renderer.square(0, 0, 200, 200, 0xFFFFFF)

            pad = 2 # good enough, not to worried since i am switching to c
            row = 0
            height = 16
            sprite_renderer.write('t', 0, height*row+(pad*(row+1)))
            sprite_renderer.write(temp, 32, height*row+(pad*(row+1)))
            row += 1
            sprite_renderer.write('h', 0, height*row+(pad*(row+1)))
            sprite_renderer.write(bme680.relative_humidity, 32, height*row+(pad*(row+1)))
            row += 1
            sprite_renderer.write('p', 0, height*row+(pad*(row+1)))
            sprite_renderer.write(bme680.pressure, 32, height*row+(pad*(row+1)))
            row += 1
            sprite_renderer.write('g', 0, height*row+(pad*(row+1)))
            sprite_renderer.write(bme680.gas, 32, height*row+(pad*(row+1)))
            row += 1
            sprite_renderer.write('a', 0, height*row+(pad*(row+1)))
            sprite_renderer.write(bme680.altitude, 32, height*row+(pad*(row+1)))
            row += 1
            sprite_renderer.write(f"u {mem_usage}%", 0, height*row+(pad*(row+1)))
            row += 1
            sprite_renderer.write(f"b {max17048.cell_percent}%", 0, height*row+(pad*(row+1)))
            row += 1
            now = rtc.datetime
            sprite_renderer.write(f"x {now.tm_mon}-{now.tm_mday}-{now.tm_year}", 0, height*row+(pad*(row+1)))
            row += 1
            hour = now.tm_hour if settings['military_time'] else now.tm_hour % 12
            sprite_renderer.write(f"    {hour}:{now.tm_min:02}", 0, height*row+(pad*(row+1)))
            row += 1

            stats = os.statvfs("/sd")

            # Calculate total and free space in bytes
            total_blocks = stats[2]
            free_blocks = stats[3]

            sprite_renderer.write('s', 0, height*row+(pad*(row+1)))
            sprite_renderer.write(f"{1 - free_blocks / total_blocks:.2f}%", 32, height*row+(pad*(row+1)))
        
        # might as well also write to the sd card
        # this will keep it in time with the display time
        with open("/sd/log.csv", "a") as f:
            for sample in samples:
                f.write(','.join([str(x) for x in sample]) + '\n')
        samples = []

    samples.append([time.mktime(now),temp,bme680.relative_humidity,bme680.pressure,bme680.gas,bme680.altitude,mem_usage,max17048.cell_voltage,max17048.cell_percent])

    time.sleep(1)
