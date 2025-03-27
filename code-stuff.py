# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board

import adafruit_bme680
import gc
import analogio

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
