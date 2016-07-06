# Pi_grammer
A shield for Raspberry Pi 2, used for programming AVR ICs. Includes capsense pad to engage, 3x2 ISP header for connectivity and status LEDs.

This project originated from Adafruits tutorial here:

https://learn.adafruit.com/program-an-avr-or-arduino-using-raspberry-pi-gpio-pins/overview

This shield makes it a bit easier to program AVRs with a headless Raspberry Pi.

This repo also contains some other useful files:

RCLOCAL - calls /home/pi/test.py and ensure that this python module will run automatically at boot up (useful when running headless)

AVRDUDE config file - sets the GPIO used for programming (in avrdude) to work with the shield design. It's located at the very end of this file.

test.py - the python module that is auto called during bootup. This also listens to the capsense IC and engages programming when pressed.

note, test.py called pi_program.sh to actually begin programming.

note, test.py also checks for MEDIA drives plugged into the USB ports of the Raspi. If there is a HEX file on the MEDIA drive (any name, it just has to have the ".hex" extension) it will copy it in and use that for programming.

