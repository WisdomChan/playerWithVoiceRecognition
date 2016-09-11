#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def APIdeal(APIresult, filesname, files):#处理API返回的结果
    if APIresult in ['开始播放', '播放', '播放歌曲']:
        return '播放', 0
    elif APIresult in ['停止','停止播放','暂停', '暂停播放']:
        return '暂停', 0
    elif APIresult in ['下一首', '播放下一首歌曲', '播放下一首歌', '播放下一首', '后一首', '播放后一首歌曲', '播放后一首歌', '播放后一首']:
        return '下一首', 0
    elif APIresult in ['上一首', '播放上一首歌曲', '播放上一首歌', '播放上一首','前一首', '播放前一首歌曲', '播放前一首歌', '播放前一首']:
        return '上一首', 0
    elif APIresult in ['随机播放', '随机']:
        return '随机播放', 0
    elif APIresult in ['小声一点', '降低音量', '减小音量']:
        return '降低音量', 0
    elif APIresult in ['大声一点', '增加音量', '加大音量']:
        return '增加音量', 0
    APIlist = list(APIresult)
    stopword = ['的']#停止词
    value = []
    for nfile in filesname:
        nCount = 0
        for nAPIlist in APIlist:
            if nAPIlist in nfile not in stopword:
                nCount += 1
        value.append(nCount)
    if sum(value) == 0:
        return '识别失败', 0
    else:
        newfiles = []
        maxvalue = max(value)
        for i, v in enumerate(value):
            if v == maxvalue:
                newfiles.append(files[i])
        return newfiles, 1#返回包括路径的音乐文件
    
    
    
    
    
