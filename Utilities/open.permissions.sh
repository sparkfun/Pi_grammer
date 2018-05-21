#!/bin/bash

echo Opening permissions now...
echo 
FOLDER=/home/pi
sudo chmod 777 $FOLDER/test.py $FOLDER/*hex $FOLDER/flash_results.txt $FOLDER/fuse_results.txt $FOLDER/avrdude_gpio.conf $FOLDER/pi_program.sh

sleep 2