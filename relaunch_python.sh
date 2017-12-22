#!/bin/bash

echo "Killing current python..."

# kill

sudo killall python

sleep 3

# change permissions on all related programming files, to avoid nasty debug errors

sudo chmod 777 flash_results.txt fuse_results.txt *.hex test.py pi_program.sh avrdude_gpio.conf

# launch

echo "Relaunching python test.py..."

sudo python test.py

