#!/bin/bash

echo "Programming beginning..."

# get firmware file name
firmware=$(find *.hex)

#to verify that avrdude can connect to the chip
#sudo avrdude -p atmega328p -C ~/avrdude_gpio.conf -c pi_1 -v

#erase and fuse bits, note the -i 100 to add delay and slow down initial com to fresh chips
sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf -c pi_1 -D -v -e -u -U hfuse:w:0xDE:m -u -U lfuse:w:0xFF:m -u -U efuse:w:0x05:m 2>fuse_results.txt

#program flash and lock bits
# extended should be 0xFD, but they only verify at 0x05, 
# also lock fuses should be 0xCF, but they only verify at 0x0F
sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf  -c pi_1 -D -v -u -U flash:w:$firmware:i -u -U lock:w:0x0F:m 2>flash_results.txt

#program lock bits
#sudo avrdude -p atmega328p -C ~/avrdude_gpio.conf -c pi_1 -v -U lock:w:0xCF:m
