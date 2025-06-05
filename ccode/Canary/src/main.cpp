// Adafruit_ImageReader test for Adafruit E-Ink Breakouts.
// Demonstrates loading images from SD card or flash memory to the screen,
// to RAM, and how to query image file dimensions.
// Requires BMP file in root directory of QSPI Flash:
// blinka.bmp.

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <SdFat.h>					  // SD card & FAT filesystem library
#include "RTClib.h"

#define EPD_CS 9	// can be any pin, but required!
#define EPD_DC 10	// can be any pin, but required!
#define SRAM_CS -1	// can set to -1 to not use a pin (uses a lot of RAM!)
#define EPD_RESET 5 // can set to -1 and share with chip Reset (can't deep sleep)
#define EPD_BUSY 6	// can set to -1 to not use a pin (will wait a fixed delay)
#define SD_CS 11		// SD card chip select

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME680 bme; // I2C
SdFat SD;							 // SD card filesystem
RTC_PCF8523 rtc;

// good so far
// different, but more control
// seems
// althought, might be importing too much, but c can figure it out

struct Sample
{
	uint32_t timestamp; // Unix timestamp in seconds
	float temperature; // Temperature in degrees Celsius
	float pressure; // Pressure in hPa
	float humidity; // Humidity in %
	float gas_resistance; // Gas resistance in Ohms
	float altitude; // Altitude in meters
};


void setup(void)
{
	Serial.begin(9600);
	// while(!Serial);           // Wait for Serial Monitor before continuing
	
	if (!rtc.begin()) {
		Serial.println(F("RTC initialization failed!"));
		while (1);
	}

	if (!bme.begin()) {
		Serial.println(F("Could not find a valid BME680 sensor, check wiring!"));
		while (1);
	}
	// Set up oversampling and filter initialization
	bme.setTemperatureOversampling(BME680_OS_8X);
	bme.setHumidityOversampling(BME680_OS_2X);
	bme.setPressureOversampling(BME680_OS_4X);
	bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
	bme.setGasHeater(320, 150); // 320*C for 150 ms

	bme.performReading();
  
	Serial.print(F("Temperature = "));
	Serial.print(bme.temperature);
	Serial.println(F(" *C"));
  
	Serial.print(F("Pressure = "));
	Serial.print(bme.pressure / 100.0);
	Serial.println(F(" hPa"));
  
	Serial.print(F("Humidity = "));
	Serial.print(bme.humidity);
	Serial.println(F(" %"));
  
	Serial.print(F("Gas = "));
	Serial.print(bme.gas_resistance / 1000.0);
	Serial.println(F(" KOhms"));
  
	Serial.print(F("Approx. Altitude = "));
	Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
	Serial.println(F(" m"));
	
	// SD card is pretty straightforward, a single call...
	if (!SD.begin(SD_CS, SD_SCK_MHZ(10)))
	{ // Breakouts require 10 MHz limit due to longer wires
		Serial.println(F("SD begin() failed"));
		while (1);
	}
	
	SD.ls(LS_SIZE);

	Serial.println(rtc.initialized() ? F("RTC is running!") : F("RTC is NOT running!"));
	Serial.println(rtc.lostPower() ? F("RTC lost power!") : F("RTC is not lost power!"));

	rtc.start();
	DateTime now = rtc.now();

    Serial.print(now.year(), DEC);
    Serial.print('-');
    Serial.print(now.month(), DEC);
    Serial.print('-');
    Serial.print(now.day(), DEC);
	Serial.print(' ');
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.println();
}

void loop()
{
}