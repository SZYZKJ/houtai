# -*- coding: utf-8 -*-
# filename: basic.py
from builtins import print

import requests
import time


class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self, apptype):
        # BonjourAI
        # appId = "wxe76eb9f73643f074"
        # appSecret = "520cd136d20a3d33ec94e40ab4342fe9"
        # BonjourChat
        gzhappId = "wxc1deae6a065dffa9"  # 公众号
        gzhappSecret = "c41de1c8444ae79798ff0f1a5880295a"  # 公众号
        appId = "wxa9ef833cef143ce1"  # 小程序
        appSecret = "574ba86bc66b664ab42e4d60276afb7c"  # 小程序
        if apptype == 'xcx':
            getUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
            appId, appSecret))
        elif apptype == 'gzh':
            getUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                gzhappId, gzhappSecret))
        urlResp = requests.get(getUrl)
        urlResp = urlResp.json()
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_access_token(self, apptype):
        if self.__leftTime < 10:
            self.__real_get_access_token(apptype)
        return self.__accessToken

    def run(self):
        while (True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()
