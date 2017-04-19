#!/bin/bash

echo "Programming beginning..."

# get firmware file name
firmware=$(find /home/pi/*.hex)
$firmware .= "/home/pi/$firmware"

#FUSE BITS
HIGH_FUSE=0xDA
LOW_FUSE=0xFF
EXT_FUSE=0x07 # due to masking, 0x05 = 0xFD, 0x07 = 0xFF
LOCK=0x0F #due to masking, 0x0F = 0xCF

#erase and fuse bits, note the -i 100 to add delay and slow down initial com to fresh chips
sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf -c linuxspi -P /dev/spidev0.0 -b 125000 -D -v -e -u -U hfuse:w:$HIGH_FUSE:m -u -U lfuse:w:$LOW_FUSE:m -u -U efuse:w:$EXT_FUSE:m 2>/home/pi/fuse_results.txt

# hard toggle of reset line, necessary to see successful programming on fresh ICs
sudo gpio -g mode 26 output
sudo gpio -g write 26 0
sleep 0.1
sudo gpio -g write 26 1
sleep 0.1

#program flash and lock bits
sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf  -c linuxspi -P /dev/spidev0.0 -b 3000000 -D -v -u -U flash:w:$firmware:i -u -U lock:w:$LOCK:m 2>/home/pi/flash_results.txt
