#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vlc

def playerinit(files):##initialize the music player
    player = vlc.MediaPlayer()
    medialist = vlc.MediaList(files)
    actplayer = vlc.MediaListPlayer()
    actplayer.set_media_player(player)
    actplayer.set_media_list(medialist)
    return (player, actplayer)

def gettitle(player):##return the title of the music
    media = player.get_media()
    title = media.get_meta(vlc.Meta.Title)
    return title

def getstatus(actplayer):## the status of player
    return actplayer.get_state()

def setvolume(player, updown):##up == 1 down == 0, set volume
    volume = player.audio_get_volume()
    if updown == 1 and volume <= 90:
        volume += 10
    if updown == 0 and volume >= 10:
        volume -= 10
    player.audio_set_volume(volume)
    

def changelist(actplayer, files):##change the list of the music
    actplayer.stop()
    medialist = vlc.MediaList(files)
    actplayer.set_media_list(medialist)
    actplayer.play()
