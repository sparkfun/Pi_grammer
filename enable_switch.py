# Raspberry Pi stand alone AVR programmer
# Enable Isolation switch for programming via command line
# SparkFun Electronics
# Pete Lewis 7/13/2018

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

PGM_SWITCH = 36

GPIO.setup(PGM_SWITCH, GPIO.OUT)

GPIO.output(PGM_SWITCH, GPIO.HIGH)