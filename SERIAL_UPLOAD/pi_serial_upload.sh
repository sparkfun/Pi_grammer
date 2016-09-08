#!/bin/bash

echo "Programming beginning..."

# get firmware file name
firmware=$(find /home/pi/SERIAL_UPLOAD/*.hex)
$firmware .= "/home/pi/SERIAL_UPLOAD/$firmware"

#Serial upload via com port
sudo avrdude -p atmega2560 -P /dev/ttyUSB0 -c stk500v2 -b 115200 -C /home/pi/avrdude_gpio.conf -v -U flash:w:$firmware:i 2>/home/pi/SERIAL_UPLOAD/serial_upload__results.txt


