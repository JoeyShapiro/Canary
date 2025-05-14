// Adafruit_ImageReader test for Adafruit E-Ink Breakouts.
// Demonstrates loading images from SD card or flash memory to the screen,
// to RAM, and how to query image file dimensions.
// Requires BMP file in root directory of QSPI Flash:
// blinka.bmp.

#include <SdFat.h>					  // SD card & FAT filesystem library

#define EPD_CS 9	// can be any pin, but required!
#define EPD_DC 10	// can be any pin, but required!
#define SRAM_CS -1	// can set to -1 to not use a pin (uses a lot of RAM!)
#define EPD_RESET 5 // can set to -1 and share with chip Reset (can't deep sleep)
#define EPD_BUSY 6	// can set to -1 to not use a pin (will wait a fixed delay)
#define SD_CS 11		// SD card chip select

SdFat SD;							 // SD card filesystem

void setup(void)
{
	Serial.begin(9600);
	while(!Serial);           // Wait for Serial Monitor before continuing

	// The Adafruit_ImageReader constructor call (above, before setup())
	// accepts an uninitialized SdFat or FatVolume object. This MUST
	// BE INITIALIZED before using any of the image reader functions!
	Serial.print(F("Initializing filesystem..."));
	// SPI or QSPI flash requires two steps, one to access the bare flash
	// memory itself, then the second to access the filesystem within...
	
	// SD card is pretty straightforward, a single call...
	if (!SD.begin(SD_CS, SD_SCK_MHZ(10)))
	{ // Breakouts require 10 MHz limit due to longer wires
		Serial.println(F("SD begin() failed"));
		for (;;)
			; // Fatal error, do not continue
	}
	
	Serial.println(F("OK!"));
	SD.ls(LS_SIZE);
}

void loop()
{
}