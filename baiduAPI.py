#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json
import urllib.request
import uuid

def baiduvoice(speechfile, mac = uuid.UUID(int=uuid.getnode()).hex[-12:]):
    baiduserver = 'http://vop.baidu.com/server_api'
    with open(speechfile, 'rb') as f:
        speechdata = f.read()
    speechbase64 = base64.b64encode(speechdata).decode('utf-8')
    speechlen = len(speechdata)

    datadict = {'format': 'x-flac', 'rate':16000, 'channel':1, 'cuid':mac, 'token': '24.b2505062483a4eb55193bee969cca2b6.2592000.1469261719.282335-8292705','lan': 'zh', 'speech':speechbase64,'len':speechlen}
    jsondata = json.dumps(datadict).encode('utf-8')
    jsonlen = len(jsondata)

    request= urllib.request.Request(url = baiduserver)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Content-Length', jsonlen)
    res = urllib.request.urlopen(url=request, data=jsondata)

    result = res.read().decode('utf-8')
    jsonresp = json.loads(result)
    if jsonresp['err_msg'] == 'success.':
        command = jsonresp['result'][0].replace('，','')
    else:
        command = '识别失败'
    return command
