#!/bin/bash

echo "Programming beginning..."

# get firmware file name
firmware=$(find /home/pi/SERIAL_UPLOAD/*.hex)
$firmware .= "/home/pi/SERIAL_UPLOAD/$firmware"
echo "firmware: "
echo $firmware

sudo /usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf -v -V -patmega328p -carduino -P/dev/ttyUSB0 -b115200 -D -Uflash:w:$firmware:i 2>/home/pi/SERIAL_UPLOAD/serial_upload_results.txt
