#!/bin/bash

echo "Programming beginning..."

# get firmware file name
firmware=$(find /home/pi/*.hex)
$firmware .= "/home/pi/$firmware"

#FUSE BITS
HIGH_FUSE=0xD6
LOW_FUSE=0xFF
EXT_FUSE=0x05 # due to masking, 0x05 = 0xFD
LOCK=0x0F #due to masking, 0x0F = 0xCF

#erase and fuse bits, note the -i 100 to add delay and slow down initial com to fresh chips
sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf -c pi_1 -D -v -e -u -U hfuse:w:$HIGH_FUSE:m -u -U lfuse:w:$LOW_FUSE:m -u -U efuse:w:$EXT_FUSE:m 2>/home/pi/fuse_results.txt

#program flash and lock bits
sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf  -c pi_1 -D -v -u -U flash:w:$firmware:i -u -U lock:w:$LOCK:m 2>/home/pi/flash_results.txt