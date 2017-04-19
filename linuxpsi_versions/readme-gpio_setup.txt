Note, you will also need to insall the gpio control stuff for the hard reset to work.

Read more at tutorial here:

https://learn.sparkfun.com/tutorials/raspberry-gpio#c-wiringpi-setup

Or you can simply run these commands: (also note that you'll need to be connected to a hard line to the internet for this to pull the necessary git clone). And don't forget the darn "sudo" - oh how I loath permissions.

sudo mkdir code
sudo ch code


pi@raspberrypi ~/code $ sudo git clone git://git.drogon.net/wiringPi
pi@raspberrypi ~/code $ sudo cd wiringPi
pi@raspberrypi ~/code/wiringPi $ sudo git pull origin
pi@raspberrypi pi@raspberrypi ~/code/wiringPi/wiringPi $ sudo ./build

test gpio control like so:

pi@raspberrypi ~/code $ gpio -g mode 18 output
pi@raspberrypi ~/code $ gpio -g write 18 1
pi@raspberrypi ~/code $ gpio -g write 18 0