#!/usr/bin/python

import RPi.GPIO as GPIO
import time, os
from subprocess import *

vertical = [
    '1941', '1942', '1943', '1944',
    'gunbird', 'gunbird2',
    'mazinger'
    ]

trigger = 8
sleep_interval = 1
is_vertical = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigger, GPIO.OUT, initial=GPIO.LOW)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

while True:
    romname = ""
    ps_grep = run_cmd("ps -aux | grep advmame/bin/advmame | grep -v grep")
    if len(ps_grep) > 1: # Ingame
        romname = ps_grep.replace(" -quiet","").split()[-1]

    if romname in vertical:
        if is_vertical == False:
            is_vertical = True
            print "On"
            GPIO.output(trigger, GPIO.HIGH)
    else:
        if is_vertical == True:
            is_vertical = False
            print "Off"
            GPIO.output(trigger, GPIO.LOW)

    time.sleep(sleep_interval)
