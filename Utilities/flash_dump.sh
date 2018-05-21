#!/bin/bash

# read flash and save it to a hex file names flash_dump.hex

# save results to a text file named flash_dump_results.txt

sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf  -c linuxspi -P /dev/spidev0.0 -b 1000000 -D -v -u -U flash:r:flash_dump.hex:i 2>flash_dump_results.txt
