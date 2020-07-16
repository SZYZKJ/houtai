from elasticsearch import Elasticsearch
from elasticsearch import helpers
import csv
import os
import time
import json
import random
import requests
import pymongo

datapath = '/home/ubuntu/data/lianaihuashu/data'
os.chdir(datapath)

es = Elasticsearch([{"host": "182.254.227.188", "port": 9218}])

# openid='oz7z64liSPmlzHped8ATXf23jqyI'#
# unionid='ofIsD1YLw3q_1v4d2NgX9GrS3ZEM'#庞宇明
# unionid='ofIsD1eQd-BlNZ5S0ftjwarnCUVk'#罗尼
# unionid='ofIsD1T87U3XmGr7yr-9P6pv8GUo'#周先生
# openid='oz7z64isIQQZ3oLczZ3hcl978dco'
# unionid='ofIsD1Xa9EqFkDLahXdiGZWH7sUo'


# def getaccess_token(apptype):
#     gzhappId = "wxc1deae6a065dffa9"  # 公众号
#     gzhappSecret = "c41de1c8444ae79798ff0f1a5880295a"  # 公众号
#     appId = "wxa9ef833cef143ce1"  # 小程序
#     appSecret = "574ba86bc66b664ab42e4d60276afb7c"  # 小程序
#     if apptype == 'xcx':
#         getUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
#             appId, appSecret))
#     elif apptype == 'gzh':
#         getUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
#             gzhappId, gzhappSecret))
#     urlResp = requests.get(getUrl)
#     urlResp = urlResp.json()
#     return urlResp['access_token']
#
#
# gzhuserinfo={}
# for line in open('gzhuserinfo.json'):
#     line=json.loads(line)
#     if line['headimgurl'] not in gzhuserinfo:
#         gzhuserinfo[line['headimgurl']]=line
#     else:
#         print(line)
# print(len(gzhuserinfo))

# unionid='ofIsD1f3U4rS8_NsIdBJZ1zlvoMA'
# openid='oz7z64pL9XTkJ3F_NDHQuXc0TbDs'


# docid1='ofIsD1QnwmttBDPqL1xflN6Z6k-U'
# docid2='ofIsD1Z-dk0x44UxY-gUOvI1F7F0'
#
# doc1=es.get(index='userinfo',doc_type='userinfo',id=docid1)['_source']
# doc2=es.get(index='userinfo',doc_type='userinfo',id=docid2)['_source']
# viptime=doc1['viptime']
# doc1['viptime']=doc2['viptime']
# doc2['viptime']=viptime
# vipdengji=doc1['vipdengji']
# doc1['vipdengji']=doc2['vipdengji']
# doc2['vipdengji']=vipdengji
# print(doc1)
# print(doc2)
# es.index(index='userinfo',doc_type='userinfo',id=docid1,body=doc1)
# es.index(index='userinfo',doc_type='userinfo',id=docid2,body=doc2)

# import pymongo
# def getTime():
#     return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["zhangfen"]
# nowtime = '^' + getTime()[:10]
# docs = mydb['shouquanma'].find(
#     {'zhifuzhuangtai': 0, 'tingyong': 0, 'zhuangtai': '未激活',
#      'goumaishijian': {"$regex": nowtime}}).limit(10000)
# t=0

#
search = {"query": {"match_all": {}}}
Docs = es.search(index='userinfo', doc_type='userinfo', body=search, size=10000, scroll="5m")
t = 0
while len(Docs['hits']['hits']):
    for doc in Docs['hits']['hits']:
        t += 1
        doc = doc['_source']
        if 'unionid' in doc and doc['unionid']=='ofIsD1foZP3IJzAOOaW22vH0a_lA':
        # if 'nickName' in doc and '不忘初心' in doc['nickName']:
            # if doc['unionid']!='ofIsD1foZP3IJzAOOaW22vH0a_lA':continue
            print(doc)
            doc['viptime'] = int(time.time())
            doc['vipdengji'] = 0
            es.index(index='userinfo', doc_type='userinfo', id=doc['unionid'], body=doc)
    Docs = es.scroll(scroll_id=Docs['_scroll_id'], scroll="5m")
print(t)


# from gevent import monkey
# from gevent import pywsgi
#
# monkey.patch_all()
# import sys
# import io
# import os
# import re
# import random
# import json
# import csv
# from Crypto.Cipher import AES
# from elasticsearch import Elasticsearch
# from elasticsearch import helpers
# from flask import Flask, request
# from flask_cors import *
# import time
# from base64 import b64encode
# import base64
# import requests
# import urllib.request
# import string
# import hashlib
# import xml.etree.ElementTree as ET
# import logging
# from PIL import Image, ImageDraw, ImageFont
# # from basic import Basic
# from io import BytesIO
# import pymongo
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["zhangfen"]





# def dict_to_xml(dict_data):
#     '''
#     dict to xml
#     :param dict_data:
#     :return:
#     '''
#     xml = ["<xml>"]
#     for k, v in dict_data.items():
#         xml.append("<{0}>{1}</{0}>".format(k, v))
#     xml.append("</xml>")
#     return "".join(xml)
#
#
# url = 'https://api.mch.weixin.qq.com/secapi/pay/profitsharing'
# prepaydata = {
#     'appid': 'wx311bf0a55020cb9e',
#     'mch_id': '1596830831',
#     'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
#     'transaction_id': '4200000547202006158118473615',
#     'out_order_no': '4200000547202006158118473615' + '4200000547202006158118473615',
#     'receivers': [{'type': 'PERSONAL_OPENID', 'account': 'oM9fn5Tl5K-4CEj-hVR1FHyeyKq0',
#                    'amount': 1, 'description': '分账到个人'}]
# }
# stringA = '&'.join(["{0}={1}".format(k, prepaydata.get(k)) for k in sorted(prepaydata)])
# stringSignTemp = '{0}&key={1}'.format(stringA, 'Aa888888888888888888888888888888')
# sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
# prepaydata['sign'] = sign
#
# result=requests.post(url=url,data=prepaydata,headers={'Content-Type': 'application/xml'})
# # req = urllib.request.Request(url, dict_to_xml(prepaydata).encode('utf8'),
# #                              headers={'Content-Type': 'application/xml'})
# # result = urllib.request.urlopen(req, timeout=10).read().decode('utf8')
# # result = xml_to_dict(result)
# print(result)


# def xml_to_dict(xml_data):
#     '''
#     xml to dict
#     :param xml_data:
#     :return:
#     '''
#     xml_dict = {}
#     root = ET.fromstring(xml_data)
#     for child in root:
#         xml_dict[child.tag] = child.text
#     return xml_dict
#
# def dict_to_xml(dict_data):
#     '''
#     dict to xml
#     :param dict_data:
#     :return:
#     '''
#     xml = ["<xml>"]
#     for k, v in dict_data.items():
#         xml.append("<{0}>{1}</{0}>".format(k, v))
#     xml.append("</xml>")
#     return "".join(xml)
#
#
# url = 'https://api.mch.weixin.qq.com/pay/profitsharingaddreceiver'
# prepaydata = {
#     'appid': 'wx311bf0a55020cb9e',
#     'mch_id': '1596830831',
#     'sign_type':'HMAC-SHA256',
#     'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
#     'receiver': json.dumps({'type': 'PERSONAL_OPENID', 'account': 'oM9fn5c8gAsgS4cS1q6RTPEGU0wo',
#                    'SERVICE_PROVIDER': 'PARTNER'},ensure_ascii=False),
# }
# stringA = '&'.join(["{0}={1}".format(k, prepaydata.get(k)) for k in sorted(prepaydata)])
# stringSignTemp = '{0}&key={1}'.format(stringA, 'Aa888888888888888888888888888888')
# sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
# prepaydata['sign'] = sign
#
# # result=requests.post(url=url,data=prepaydata,headers={'Content-Type': 'application/xml'})
# req = urllib.request.Request(url, dict_to_xml(prepaydata).encode('utf8'),
#                              headers={'Content-Type': 'application/xml'})
# result = urllib.request.urlopen(req).read().decode('utf8')
# result = xml_to_dict(result)
# print(result)