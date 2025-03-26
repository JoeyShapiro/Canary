import board
import digitalio
import adafruit_bme680

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D10)  # Make sure this is the correct pin!
cs.direction = digitalio.Direction.OUTPUT
cs.value = True  # Start with CS high (inactive)

bme680 = adafruit_bme680.Adafruit_BME680_SPI(spi, cs)

# Change this to match your local sea level pressure
bme680.sea_level_pressure = 1013.25

# You can also create the sensor using SPI if preferred
# import digitalio
# spi = board.SPI()
# cs = digitalio.DigitalInOut(board.D10)
# bme680 = adafruit_bme680.Adafruit_BME680_SPI(spi, cs)

# Main loop
while True:
    current_temp = bme680.temperature
    current_gas = bme680.gas
    current_humid = bme680.relative_humidity
    current_pressure = bme680.pressure
    current_altitude = bme680.altitude

    # Print the values
    print("Temperature: %0.1f C" % current_temp)
    print("Gas: %d ohm" % current_gas)
    print("Humidity: %0.1f %%" % current_humid)
    print("Pressure: %0.3f hPa" % current_pressure)
    print("Altitude = %0.2f meters" % current_altitude)
    print("\n")

    # Wait 2 seconds
    time.sleep(2)