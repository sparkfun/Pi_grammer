Note, you must follow some setup instructions on an SFE tutorial to get SPI setup correctly. 

You can find that here:

https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial#spi-on-pi


SPI on Pi
Configuration

The SPI peripheral is not turned on by default. To enable it, do the following.

Run sudo raspi-config.
Use the down arrow to select 9 Advanced Options
Arrow down to A6 SPI.
Select yes when it asks you to enable SPI,
Also select yes when it asks about automatically loading the kernel module.
Use the right arrow to select the <Finish> button.
Select yes when it asks to reboot.