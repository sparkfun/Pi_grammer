# Raspberry Pi stand alone AVR programmer
# SparkFun Electronics
# Pete Lewis 7/1/2016
# More about Avrdude install/setup/use can be found at
# https://learn.adafruit.com/program-an-avr-or-arduino-using-raspberry-pi-gpio-pins/

# This python script bassically does this:
# Press a button to engage programming
# Programming BASH file is called pi_program.sh
# This contains all the calls to avrdude, including firmware, fuses and other flags
# Indicate status on a few LEDs - ideally we can show success at fuse bits, program, and lock bits.



import os, sys
import shutil
import serial
import time
import RPi.GPIO as GPIO

FAILLED = 11
PASSLED = 13
STATLED = 7
DETCLED = 15

SHUTDOWN = 29

BOOTLOADERPING = 31
BARRELNOW = 32
IO = 33
RESETBUTTONS = 36

BARRELNOW_LED_ON = False
RESET_LED_ON = False
STATLED_ON = False


msg = 'NERD'
runonce = 0
trigger = 0
resettimes1 = "0"
resettimes2 = "0"
resettimes3 = "0"
heard0 = False
heard1 = False
testresult = False
bootping = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DETCLED, GPIO.OUT)
GPIO.setup(STATLED, GPIO.OUT)
GPIO.setup(FAILLED, GPIO.OUT)
GPIO.setup(PASSLED, GPIO.OUT)

#GPIO.setup(SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # with internal pullup enabled
GPIO.setup(SHUTDOWN, GPIO.IN) # NO INTERNAL PULLUP

GPIO.setup(BOOTLOADERPING, GPIO.OUT)
GPIO.setup(BARRELNOW, GPIO.OUT)
GPIO.setup(IO, GPIO.OUT)
GPIO.setup(RESETBUTTONS, GPIO.OUT)

GPIO.output(BOOTLOADERPING, GPIO.LOW)
GPIO.output(BARRELNOW, GPIO.LOW)
GPIO.output(IO, GPIO.LOW)
GPIO.output(RESETBUTTONS, GPIO.LOW)


GPIO.output(DETCLED, GPIO.LOW)
GPIO.output(STATLED, GPIO.LOW)
GPIO.output(FAILLED, GPIO.LOW)
GPIO.output(PASSLED, GPIO.LOW)

global firmware_path_media
global new_hex
new_hex = False
global copy_flag
copy_flag = False


def update_firmware():
        global new_hex
        new_hex = False
        for root, dirs, files in os.walk('/media'):
                for name in files:
                        #print (os.path.join(root, name))
                        tempstring = (os.path.join(root, name))
                        if 'hex' in tempstring:
                                #print 'new hex file found!!'
                                global new_hex
                                new_hex = True
                                #print tempstring
                                global firmware_path_media
                                firmware_path_media = tempstring
        if(new_hex == False):
                #print 'no new hex'
                global copy_flag
                copy_flag = False
        elif((new_hex == True) and (copy_flag == False)):
                print 'new hex found'
                global firmware_path_media
                print firmware_path_media
                global copy_flag
                copy_flag = True
                print 'copying hex file to local folder /home/pi'
                shutil.copy(firmware_path_media, '/home/pi')
                print 'done'
                                
def shut_down():
        print "shutting down"
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

def program():
        command = "/usr/bin/sudo ./pi_program.sh"
        #command = "/usr/bin/sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf -c pi_1 -D -e 2>output1.txt"
        #command = "/usr/bin/sudo dir"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output
        print "...programming done."

def parse_results():
        f = open('fuse_results.txt', 'r')
        for line in f:
                if 'avrdude: 1 bytes of hfuse verified' in line:
                        print line
                elif 'avrdude: 1 bytes of lfuse verified' in line:
                        print line
                elif 'avrdude: 1 bytes of efuse verified' in line:
                        print line
                elif 'avrdude: AVR device not responding' in line:
                        print line
        f.close()

        f = open('flash_results.txt', 'r')
        for line in f:
                if 'avrdude: 32768 bytes of flash verified' in line:
                        print line                  
                elif 'avrdude: 1 bytes of lock verified' in line:
                        print line
                elif 'avrdude: AVR device not responding' in line:
                        print line
        f.close()        

def toggle_stat_led():
        global STATLED_ON
        if (STATLED_ON):
                GPIO.output(STATLED, GPIO.LOW)
                STATLED_ON = False
        else:
                GPIO.output(STATLED, GPIO.HIGH)
                STATLED_ON = True

def all_leds_on(): # used to indicate proper shutdown
        GPIO.output(BOOTLOADERPING, GPIO.HIGH)
        GPIO.output(BARRELNOW, GPIO.HIGH)
        GPIO.output(IO, GPIO.HIGH)
        GPIO.output(RESETBUTTONS, GPIO.HIGH)
        GPIO.output(DETCLED, GPIO.HIGH)
        GPIO.output(STATLED, GPIO.HIGH)
        GPIO.output(FAILLED, GPIO.HIGH)
        GPIO.output(PASSLED, GPIO.HIGH)

while True:
        toggle_stat_led() 
        time.sleep(.5)
        update_firmware()
        #print GPIO.input(SHUTDOWN)

        # press once to program, hold down to shutdown
        
        if GPIO.input(SHUTDOWN) == False:
                counter = 0
                while GPIO.input(SHUTDOWN) == False:
                        counter += 1
                        print counter
                        time.sleep(.5)
                if counter < 4:
                        program()
                        parse_results()
                if counter == 4:
                        all_leds_on()
                        shut_down()
