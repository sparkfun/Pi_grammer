#!/bin/bash

echo "Programming beginning..."

# get firmware file name
firmware=$(find /home/pi/*.hex)
$firmware .= "/home/pi/$firmware"

# DEVICE 
# Here are some commonly used "part no"s in avrdude at SFE
# UN-comment the one you wish to use, or plug in something different
# Use "avrdude -p?" for a list of supported devices
DEVICE=atmega328p
#DEVICE=m32u4
#DEVICE=t2313

#FUSE BITS
HIGH_FUSE=0xD8
LOW_FUSE=0xFF
EXT_FUSE=0x05 # due to masking, 0x05 = 0xFD, 0x07 = 0xFF, ***Note on an ATMEGA2560, ext fuse writes and verifies as 0xFD
LOCK=0x0F # due to masking, 0x0F = 0xCF

#enable programming isolation switch
sudo python enable_switch.py

#erase and then write FUSE bits
sudo avrdude -p $DEVICE -C /home/pi/avrdude_gpio.conf -c linuxspi -P /dev/spidev0.0 -b 125000 -D -v -e -u -U hfuse:w:$HIGH_FUSE:m -u -U lfuse:w:$LOW_FUSE:m -u -U efuse:w:$EXT_FUSE:m 2>/home/pi/fuse_results.txt

sudo gpio -g mode 26 output
sudo gpio -g write 26 0
sleep 0.1
sudo gpio -g write 26 1
sleep 0.1

#program flash and lock bits
sudo avrdude -p $DEVICE -C /home/pi/avrdude_gpio.conf -c linuxspi -P /dev/spidev0.0 -b 2000000 -D -v -u -U flash:w:$firmware:i -u -U lock:w:$LOCK:m 2>/home/pi/flash_results.txt

#DISable programming isolation switch
sudo python disable_switch.py
