#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def musiclist(musicdir = '/home/pi/Music/'):
    filename = [x for x in os.listdir(musicdir)]
    files = []
    for n in filename:
        files.append(musicdir + n)
    return (filename, files)    
