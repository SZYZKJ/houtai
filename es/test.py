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


openid='oz7z64liSPmlzHped8ATXf23jqyI'
unionid='ofIsD1YLw3q_1v4d2NgX9GrS3ZEM'
# openid='oz7z64isIQQZ3oLczZ3hcl978dco'
# unionid='ofIsD1Xa9EqFkDLahXdiGZWH7sUo'

es.delete(index='userinfo',doc_type='userinfo',id=unionid)


# search = {"query": {"match_all": {}}}
# Docs=es.search(index='userinfo',doc_type='userinfo',body=search,size=10000)['hits']['hits']
# for doc in Docs:
#     doc=doc['_source']
#     if 'unionid' in doc:
#         try:
#             es.delete(index='userinfo',doc_type='userinfo',id=doc['unionid'])
#         except:
#             doc.pop('unionid')
#             es.index(index='userinfo',doc_type='userinfo',body=doc,id=doc['openid'])

# try:
#     es.delete(index='userinfo', doc_type='userinfo', id=openid)
# except:
#     None
# try:
#     es.delete(index='userinfo', doc_type='userinfo', id=unionid)
# except:
#     None
# try:
#     es.delete(index='kechenggoumai', doc_type='kechenggoumai', id=openid)
# except:
#     None
# try:
#     es.delete(index='kechenggoumai', doc_type='kechenggoumai', id=unionid)
# except:
#     None
# try:
#     es.delete(index='dianzanshoucang', doc_type='dianzanshoucang', id=openid)
# except:
#     None
# try:
#     es.delete(index='dianzanshoucang', doc_type='dianzanshoucang', id=unionid)
# except:
#     None
# doc=es.get(index='userinfo',doc_type='userinfo',id=unionid)['_source']
# es.index(index='userinfo',doc_type='userinfo',id=openid,body=doc)