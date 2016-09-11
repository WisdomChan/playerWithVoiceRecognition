#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from key import keyinit
import time

import pyaudio
from record import record
import os

from baiduAPI import baiduvoice
from APIdeal import APIdeal

import vlc
from musiclist import musiclist
import musicplayer
import random

#12864 section
import ctypes



#button section
global keyschange
keyschange = [0, 0, 0, 0]

keys = [25, 17, 27, 22]

def keyscan():
    global keyschange
    for i, v in enumerate(keys):
        if GPIO.input(v) == 0:
            time.sleep(0.03)
            if GPIO.input(v) == 0:
                keyschange[i] = 1
                print('push the %d button' % i)
                while GPIO.input(v) == 0:
                    keyschange[i] = 1

#加载12864C语言驱动
ll = ctypes.cdll.LoadLibrary
lib = ll('/home/pi/musicproject/libpycall.so')

keyinit()
lib.init12864()#12864初始化
filename, files = musiclist()
player, actplayer = musicplayer.playerinit(files)
actplayer.play()
newfiles = 'wait'
pretitle = 'pretitle'

while True:
    keyscan()
    title = musicplayer.gettitle(player).replace('.mp3','')
    #print(title)
    if pretitle != title:
        pretitle = title
        lib.clearline(0)
        lib.clearline(1)
    lib.WriteWord_LCD12864_2(title.encode('utf-8'))
    if keyschange[0] == 1:
        if newfiles != '暂停':
            actplayer.pause()
        lib.clearline(2)
        lib.clearline(3)
        lib.write12864(2, '开始录音'.encode('utf-8'))
        record()
        os.system('ffmpeg -i /home/pi/musicproject/output.wav -ar 16000 -acodec flac /home/pi/musicproject/output.flac -y')
        
        print('录音结束，识别音频中')
        lib.clearline(2)
        lib.write12864(2, '识别音频中'.encode('utf-8'))
        lib.clearline(3)
        command = baiduvoice('/home/pi/musicproject/output.flac')#上传到云识别    
        print(command)
        
        lib.clearline(2)
        lib.write12864(2, '识别结果'.encode('utf-8'))
        
        if command != '识别失败':#云识别成功
            newfiles, showflag = APIdeal(command, filename, files)
            print(newfiles)
            #展示识别结果
            if showflag == 0:
                lib.write12864(3, newfiles.encode('utf-8'))
            else: #showflag == 1:
                lib.write12864(3, '识别成功'.encode('utf-8'))
                
            if newfiles != '识别失败':#本地命令识别成功
                if newfiles == '播放':
                    actplayer.play()
                elif newfiles == '暂停':
                    keyschange[0] = keyschange[0]
                elif newfiles == '下一首':
                    if actplayer.next() == -1:
                        actplayer.next()#没有下一首了
                elif newfiles == '上一首':
                    if actplayer.previous() == -1:
                        actplayer.previous()#没有前一首了
                elif newfiles == '随机播放':
                    random.shuffle(files) 
                    musicplayer.changelist(actplayer, files)
                elif newfiles == '降低音量':
                    musicplayer.setvolume(player, 0)
                    actplayer.play()
                elif newfiles == '增加音量':
                    musicplayer.setvolume(player, 1)
                    actplayer.play()
                else:#更新列表
                    musicplayer.changelist(actplayer, newfiles)
            else:
                actplayer.play()
        else:
            lib.write12864(3, '识别失败'.encode('utf-8'))
            actplayer.play()
        keyschange[0] = 0
        lib.clearline(0)
        lib.clearline(1)
        
    if keyschange[1] == 1:#通过按键1,播放前一首
        keyschange[1] = 0
        if actplayer.previous() == -1:
            actplayer.previous()#没有前一首了
        lib.clearline(0)
        lib.clearline(1)

    if keyschange[2] == 1:#通过按键2,暂停或播放
        keyschange[2] = 0
        if newfiles != '暂停':
            actplayer.pause()
            newfiles = '暂停'
        else:#已暂停
            actplayer.play()
            newfiles = 'wait'
        lib.clearline(0)
        lib.clearline(1)

    if keyschange[3] == 1:#通过按键3,播放下一首
        keyschange[3] = 0
        if actplayer.next() == -1:
            actplayer.next()#没有前一首了
        lib.clearline(0)
        lib.clearline(1)
    
    if musicplayer.getstatus(actplayer) == vlc.State.Ended:#播放结束，重新开始播放
        actplayer.play()
        
