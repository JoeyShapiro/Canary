import adafruit_sdcard
import digitalio
import board
import storage

# Connect to the card and mount the filesystem.
spi = board.SPI()  # Uses SCK and MOSI
cs = digitalio.DigitalInOut(board.D11)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Use the filesystem as normal.
with open("/sd/test.txt", "w") as f:
    f.write("Hello world\n")