#!/bin/bash

echo "Programming beginning..."

# get firmware file name
firmware=$(find /home/pi/*.bin)
$firmware .= "/home/pi/$firmware"

sudo python /home/pi/espressif/esp32/tools/esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 write_flash -z --flash_freq 80m --flash_mode dio 0x1000 /home/pi/espressif/esp32/tools/sdk/bin/bootloader.bin 0x4000 /home/pi/espressif/esp32/tools/sdk/bin/partitions_singleapp.bin 0x10000 $firmware 1>/home/pi/flash_results.txt
