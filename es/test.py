from elasticsearch import Elasticsearch
from elasticsearch import helpers
import csv
import os
import time
import json
import random
import requests

datapath = '/home/ubuntu/data/lianailianmeng/data'
os.chdir(datapath)


es = Elasticsearch([{"host": "182.254.227.188", "port": 9218}])
# escopy = Elasticsearch([{"host": "119.29.67.239", "port": 9218}])


# openid='oz7z64liSPmlzHped8ATXf23jqyI'#
unionid='ofIsD1YLw3q_1v4d2NgX9GrS3ZEM'#庞宇明
# unionid='ofIsD1eQd-BlNZ5S0ftjwarnCUVk'#罗尼
# unionid='ofIsD1T87U3XmGr7yr-9P6pv8GUo'#周先生
# unionid='ofIsD1Xa9EqFkDLahXdiGZWH7sUo'#唔哩周周
# openid='oz7z64isIQQZ3oLczZ3hcl978dco'
# unionid='ofIsD1Xa9EqFkDLahXdiGZWH7sUo'
# es.delete(index='userinfo',doc_type='userinfo',id='ofIsD1T87U3XmGr7yr-9P6pv8GUo')
# es.delete(index='userinfo',doc_type='userinfo',id='ofIsD1Xa9EqFkDLahXdiGZWH7sUo')


doc=es.get(index='userinfo',doc_type='userinfo',id=unionid)['_source']
print(doc)

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
#
# search = {"query": {"match_all": {}}}
# Docs=es.search(index='kechenggoumai',doc_type='kechenggoumai',body=search,size=10000)['hits']['hits']
# for doc in Docs:
#     openid =doc['_id']
#     doc=es.get(index='userinfo',doc_type='userinfo',id=openid)['_source']
#     if doc['avatarUrl'] in gzhuserinfo:
#         print('aaaaaaaaaaaaaaaaaaaaaaaa')
#     else:
#         print(doc['nickName'])