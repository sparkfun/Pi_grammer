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

STAT = 7
FUSE_P = 15
FUSE_F = 13
FLASH_P = 31
FLASH_F = 11
LOCK_P = 32
LOCK_F = 22

CAPSENSE = 33
SHUTDOWN = 29

STATLED_ON = False # Used for toggling stat led on and off during main loop

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(STAT, GPIO.OUT)
GPIO.setup(FUSE_P, GPIO.OUT)
GPIO.setup(FUSE_F, GPIO.OUT)
GPIO.setup(FLASH_P, GPIO.OUT)
GPIO.setup(FLASH_F, GPIO.OUT)
GPIO.setup(LOCK_P, GPIO.OUT)
GPIO.setup(LOCK_F, GPIO.OUT)

GPIO.setup(SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # with internal pullup enabled - trying this out to avoid accidental shutdowns.
#GPIO.setup(SHUTDOWN, GPIO.IN) # NO INTERNAL PULLUP
GPIO.setup(CAPSENSE, GPIO.IN)

GPIO.output(STAT, GPIO.LOW)
GPIO.output(FUSE_P, GPIO.LOW)
GPIO.output(FUSE_F, GPIO.LOW)
GPIO.output(FLASH_P, GPIO.LOW)
GPIO.output(FLASH_F, GPIO.LOW)
GPIO.output(LOCK_P, GPIO.LOW)
GPIO.output(LOCK_F, GPIO.LOW)

firmware_path_media = ' '
new_hex = False
copy_flag = False

bash_path_media = ' '
new_bash = False
copy_flag_bash = False

stat_blink_counter = 0

def all_leds_on():
        GPIO.output(STAT, GPIO.HIGH)
        GPIO.output(FUSE_P, GPIO.HIGH)
        GPIO.output(FUSE_F, GPIO.HIGH)
        GPIO.output(FLASH_P, GPIO.HIGH)
        GPIO.output(FLASH_F, GPIO.HIGH)
        GPIO.output(LOCK_P, GPIO.HIGH)
        GPIO.output(LOCK_F, GPIO.HIGH)

def all_leds_off():
        GPIO.output(STAT, GPIO.LOW)
        GPIO.output(FUSE_P, GPIO.LOW)
        GPIO.output(FUSE_F, GPIO.LOW)
        GPIO.output(FLASH_P, GPIO.LOW)
        GPIO.output(FLASH_F, GPIO.LOW)
        GPIO.output(LOCK_P, GPIO.LOW)
        GPIO.output(LOCK_F, GPIO.LOW)

def blink_circle():
        GPIO.output(FUSE_P, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(FUSE_P, GPIO.LOW)
        GPIO.output(FLASH_P, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(FLASH_P, GPIO.LOW)
        GPIO.output(LOCK_P, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(LOCK_P, GPIO.LOW)
        GPIO.output(LOCK_F, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(LOCK_F, GPIO.LOW)
        GPIO.output(FLASH_F, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(FLASH_F, GPIO.LOW)        
        GPIO.output(FUSE_F, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(FUSE_F, GPIO.LOW)
        
        
def update_firmware_and_bash():
        global new_hex
        new_hex = False
        global firmware_path_media
        global copy_flag
        
        global new_bash
        new_bash = False
        global bash_path_media
        global copy_flag_bash
        
        for root, dirs, files in os.walk('/media'):
                for name in files:
                        #print (os.path.join(root, name))
                        tempstring = (os.path.join(root, name))
                        if 'hex' in tempstring and 'SERIAL_UPLOAD' not in tempstring:
                                #print 'new hex file found!!'
                                new_hex = True
                                #print tempstring
                                firmware_path_media = tempstring
                        if 'pi_program.sh' in tempstring:
                                #print 'new bash file found!!'
                                new_bash = True
                                #print tempstring
                                bash_path_media = tempstring                                
        if(new_hex == False):
                #print 'no new hex'
                copy_flag = False
        elif((new_hex == True) and (copy_flag == False)):
                blink_circle()
                print 'new hex found'
                print firmware_path_media
                # first, delete the old hex file
                for root, dirs, files in os.walk('/home/pi'):
                        for name in files:
                                #print (os.path.join(root, name))
                                old_firmware_path = (os.path.join(root, name))
                                if 'hex' in old_firmware_path and 'SERIAL_UPLOAD' not in old_firmware_path:
                                        print 'old hex file found!!'
                                        print 'deleting old firmware file:'
                                        print old_firmware_path
                                        os.remove(old_firmware_path)
                                        print 'done'
                copy_flag = True # to avoid copying the file EVERY loop, we only need to do it once
                print 'copying hex file to local folder /home/pi'
                shutil.copy(firmware_path_media, '/home/pi')
                print 'done'
        if(new_bash == False):
                #print 'no new bash'
                copy_flag_bash = False
        elif((new_bash == True) and (copy_flag_bash == False)):
                blink_circle()
                print 'new bash found'
                print bash_path_media
                # first, delete the old bash file
                print 'deleting old bash file: /home/pi/pi_program.sh'
                os.remove('/home/pi/pi_program.sh')
                print 'done'            
                copy_flag_bash = True # to avoid copying the file EVERY loop, we only need to do it once
                print 'copying bash file to local folder /home/pi'
                shutil.copy(bash_path_media, '/home/pi')
                print 'done'
                                
def shut_down():
        print "shutting down"
        command = "/usr/bin/sudo /sbin/shutdown -h now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output
        
def clean_results():
        f = open('/home/pi/fuse_results.txt', 'w')
        f.truncate()
        f.close()
        f = open('/home/pi/flash_results.txt', 'w')
        f.truncate()
        f.close()
        
def program():
        clean_results()
        #command = "/usr/bin/sudo ./pi_program.sh"
        #command = "sudo ./pi_program.sh"
        command = "sh /home/pi/pi_program.sh"
        #command = "/usr/bin/sudo avrdude -p atmega328p -C /home/pi/avrdude_gpio.conf -c pi_1 -D -e 2>output1.txt"
        #command = "/usr/bin/sudo dir"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output
        print "...programming done."

def program_serial():
        print "serial programming beginning..."
        command = "sh /home/pi/SERIAL_UPLOAD/pi_serial_upload.sh"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output
        print "serial programming done."        

def parse_results():
        #variables to store success/failure of each programming step
        hfuse = False
        lfuse = False
        efuse = False
        flash = False
        lock = False
        f = open('/home/pi/fuse_results.txt', 'r')
        for line in f:
                if 'avrdude: 1 bytes of hfuse verified' in line:
                        print line
                        hfuse = True
                elif 'avrdude: 1 bytes of lfuse verified' in line:
                        print line
                        lfuse = True
                elif 'avrdude: 1 bytes of efuse verified' in line:
                        print line
                        efuse = True
                elif 'avrdude: AVR device not responding' in line:
                        print line
        f.close()

        f = open('/home/pi/flash_results.txt', 'r')
        FLASH_SIZE = '00000'    # the flash size can vary slightly depending on the hex file (I think)
                                # I've seen 32652, 32768, and 32650 in the three examples I've tried,
                                # So pulling in this variable became necessary to use in verifying the correct message
                                # when parsing flash_results.txt
        for line in f:
                if 'avrdude: writing flash (' in line:  # This is the line that contains the flash file size
                                                        # The complete line looks like this:
                                                        # "avrdude: writing flash (32670 bytes):"
                        FLASH_SIZE = line[24:(line.find('byte')-1)]
                        print 'FLASH_SIZE:' + FLASH_SIZE
                elif 'avrdude: ' + FLASH_SIZE + ' bytes of flash verified' in line: # Look for complete verification line
                        print line
                        flash = True                       
                elif 'avrdude: 1 bytes of lock verified' in line:
                        print line
                        lock = True
                elif 'avrdude: AVR device not responding' in line:
                        print line
        f.close()        
        ## display results on all 6 stat LEDs
        if((hfuse == True) and (lfuse == True) and (efuse == True)):
                GPIO.output(FUSE_P, GPIO.HIGH)
        else:
                GPIO.output(FUSE_F, GPIO.HIGH)
        if(flash == True):
                GPIO.output(FLASH_P, GPIO.HIGH)
        else:
                GPIO.output(FLASH_F, GPIO.HIGH)
        if(lock == True):
                GPIO.output(LOCK_P, GPIO.HIGH)
        else:
                GPIO.output(LOCK_F, GPIO.HIGH)                  
        
def toggle_stat_led():
        global STATLED_ON
        if (STATLED_ON):
                GPIO.output(STAT, GPIO.LOW)
                STATLED_ON = False
        else:
                GPIO.output(STAT, GPIO.HIGH)
                STATLED_ON = True

def blink_all():
        all_leds_on()
        time.sleep(.1)
        all_leds_off()

time.sleep(3) # let 3.3V line settle to avoid accidental shutdowns
while True:
        time.sleep(.1)
        stat_blink_counter += 1
        if(stat_blink_counter > 5):
                toggle_stat_led()
                stat_blink_counter = 0
        
        update_firmware_and_bash()
        #print GPIO.input(SHUTDOWN)
        
        if GPIO.input(SHUTDOWN) == False:
                counter = 0
                while GPIO.input(SHUTDOWN) == False:
                        counter += 1
                        print counter
                        blink_all()
                        time.sleep(.5)
                        if counter > 4:
                                all_leds_on()
                                shut_down()

        if GPIO.input(CAPSENSE) == True:
                blink_all()
                GPIO.output(STAT, GPIO.HIGH) #indicate programming attempt
                program()
                parse_results()
                if os.path.exists('/home/pi/SERIAL_UPLOAD/pi_serial_upload.sh') == True:
                        program_serial()
                else:
                        time.sleep(3) # led leds stay on for 3 secs
                all_leds_off()
