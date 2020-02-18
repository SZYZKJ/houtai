import sys
import io
import os
import random
import json
import csv
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch([{"host": "182.254.227.188", "port": 9218, "timeout": 3600}])
datapath = '/home/ubuntu/data/lianaihuashu/data'
os.chdir(datapath)
unionidlist = {}
nowtime = time.strftime("%Y%m%d", time.localtime())
search = {"query": {"match_phrase_prefix": {"updatatime": nowtime}}}
Docs = es.search(index='userzhifu', doc_type='userzhifu', body=search, size=10000)
userlist = []
for doc in Docs['hits']['hits']:
    try:
        if doc['_source']['updatatime'][:8] == nowtime:
            userlist.append(doc['_source']['unionid'])
            unionidlist[doc['_source']['unionid']] = doc['_source']['updatatime']
    except:
        None
for unionid in userlist:
    doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
    print(doc)