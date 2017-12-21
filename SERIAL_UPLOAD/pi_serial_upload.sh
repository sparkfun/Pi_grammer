#!/bin/bash

echo "Serial Upload beginning..."

# Device and Baudrate. The default baudrate of 115200 will work with
# all chips above an 8mHz clock speed. 57600 is recommended for slower chips.
DEVICE=atmega328p
BAUD=115200

# get firmware file name
firmware=$(find /home/pi/SERIAL_UPLOAD/*.hex)
$firmware .= "home/pi/SERIAL_UPLOAD/$firmware"
echo "firmware: "
echo $firmware

sudo /usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -p$DEVICE -carduino -P/dev/ttyUSB0 -b$BAUD -D -Uflash:w:$firmware:i 2>/home/pi/SERIAL_UPLOAD/serial_upload_results.txt
