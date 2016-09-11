#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

#25 语音识别
#17 上一首
#27 暂停/开始
#22 下一首
keys = [25, 17, 27, 22]
keyschange = [0, 0, 0, 0]

def keyinit():
    GPIO.setmode(GPIO.BCM)
    for k in keys:
        GPIO.setup(k, GPIO.IN, pull_up_down = GPIO.PUD_UP)

##def keyscan():
##    global change
##    for i, v in enumerate(keys):
##        if GPIO.input(v) == 0:
##            time.sleep(0.03)
##            if GPIO.input(v) == 0:
##                keyschange[i] = 1
##                print('push the %d button' % i)
##                while GPIO.input(v) == 0:
##                    keyschange[i] = 1
