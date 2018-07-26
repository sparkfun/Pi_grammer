SparkFun Pi AVR Programmer HAT
========================================

![SparkFun Raspberry Pi Stand-Alone Programmer w/ the Pi-Grammer Hat](https://cdn.sparkfun.com/r/600-600/assets/learn_tutorials/7/3/9/Pi_Grammer.jpg)

[*SparkFun Pi AVR Programmer HAT (DEV-14747)*](https://www.sparkfun.com/products/14747)

A shield for Raspberry Pi 2, used for programming AVR ICs. Includes capsense pad to engage, 2x3 ISP header for connectivity and status LEDs.

Documentation
--------------
* **[Hookup Guide](https://learn.sparkfun.com/tutorials/pi-avr-programmer-hat-hookup-guide)** - Basic hookup guide for the Pi AVR Programmer Hat.
* **[Raspberry Pi Stand-Alone Programmer](https://learn.sparkfun.com/tutorials/raspberry-pi-stand-alone-programmer)** - more information about the prototype can be found in the article.

Additional Notes
--------------
This project originated from Adafruits tutorial here:

https://learn.adafruit.com/program-an-avr-or-arduino-using-raspberry-pi-gpio-pins/overview

This shield makes it a bit easier to program AVRs with a headless Raspberry Pi.

This repo also contains some other useful files:

* **RCLOCAL** - calls /home/pi/test.py and ensure that this python module will run automatically at boot up (useful when running headless)

* **AVRDUDE config file** - sets the GPIO used for programming (in avrdude) to work with the shield design. It's located at the very end of this file.

* **test.py** - the python module that is auto called during bootup. This also listens to the capsense IC and engages programming when p ressed.

**Note:** test.py called pi_program.sh to actually begin programming.

**Note:** test.py also checks for MEDIA drives plugged into the USB ports of the Raspi. If there is a HEX file on the MEDIA drive (any name, it just has to have the ".hex" extension) it will copy it in and use that for programming.

KEYWORDS: RASPI PROGRAMMER

Troubleshooting Tips
--------------

1) USB port issues. If you are having trouble with com port enumeration. That is, you are plugging in something like an FTDI serial basic, and the Raspi will not recognize it. This may be fixed by using one of SparkFun Cerberus USB hub cables. We found that after plugging in 20+ FTDI basics into a pi, then it stops recognizing the devices. But if you use a hub (like the cerberus) inbetween the pi USB and the serial bridge IC, then it always pops up as "/dev/ttyUSB0" for 1000s of boards in a row. Wahoo!

![SparkFun Cerberus USB Cable](https://cdn.sparkfun.com/r/92-92/assets/parts/8/5/3/9/12016-01.jpg)

[SparkFun Cerberus USB Cable](https://www.sparkfun.com/products/12016)

License Information
-------------------

This product is _**open source**_! 

Please review the LICENSE.md file for license information. 

If you have any questions or concerns on licensing, please contact techsupport@sparkfun.com.

Distributed as-is; no warranty is given.

- Your friends at SparkFun.
