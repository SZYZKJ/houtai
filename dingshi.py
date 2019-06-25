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
blocklen=10000

ip="182.254.227.188"
# ip="119.29.67.239"
es = Elasticsearch([{"host": ip, "port": 9218, "timeout": 3600}])
gengxin=['tuweiqinghua','liaomeitaolu','xingxiangjianshe','liaomeishizhanlist','baikelist','wendalist','xinliceshilist']
gengxindianzanshooucang=['liaomeishizhan','baike','wenda','xinliceshi']
gengxinhaokan=['kechenglist','sijiao']
search = {"query": {"match_all": {}}}
lianaizhuli_index = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1,
                },
                "properties": {
                    "title": {
                        "type": "text",
                        "fields": {
                            "cn": {
                                "type": "text",
                                "analyzer": "ik_smart"
                            },
                            "en": {
                                "type": "text",
                                "analyzer": "english"
                            }
                        }
                    }
                }
            }
def solve():
    for docname in gengxin:
        try:
            actions = []
            Docs=es.search(index=docname,doc_type=docname,body=search,size=10000)['hits']['hits']
            for doc in Docs:
                xinzeng = random.randint(10, 100)
                doc['_source']['count'] += xinzeng
                action = {
                    "_index": docname,
                    "_type": docname,
                    '_id': doc['_id'],
                    "_source": doc['_source'],
                }
                actions.append(action)
            es.indices.delete(index=docname)
            es.indices.create(index=docname, body=lianaizhuli_index, ignore=400)
            random.shuffle(actions)
            while len(actions):
                helpers.bulk(es, actions[:blocklen])
                actions = actions[blocklen:]
        except:
            print(docname)
    for docname in gengxindianzanshooucang:
        try:
            actions = []
            Docs=es.search(index=docname,doc_type=docname,body=search,size=10000)['hits']['hits']
            for doc in Docs:
                xinzeng=random.randint(0,10)
                doc['_source']['dianzan']+=xinzeng
                xinzeng = random.randint(0, 10)
                doc['_source']['shoucang'] += xinzeng
                action = {
                    "_index": docname,
                    "_type": docname,
                    '_id': doc['_id'],
                    "_source": doc['_source'],
                }
                actions.append(action)
            es.indices.delete(index=docname)
            es.indices.create(index=docname, body=lianaizhuli_index, ignore=400)
            random.shuffle(actions)
            while len(actions):
                helpers.bulk(es, actions[:blocklen])
                actions = actions[blocklen:]
        except:
            print(docname)
    for docname in gengxinhaokan:
        try:
            actions = []
            Docs=es.search(index=docname,doc_type=docname,body=search,size=10000)['hits']['hits']
            for doc in Docs:
                xinzeng=random.randint(0,10)
                doc['_source']['count']+=xinzeng
                action = {
                    "_index": docname,
                    "_type": docname,
                    '_id': doc['_id'],
                    "_source": doc['_source'],
                }
                actions.append(action)
            es.indices.delete(index=docname)
            es.indices.create(index=docname, body=lianaizhuli_index, ignore=400)
            random.shuffle(actions)
            while len(actions):
                helpers.bulk(es, actions[:blocklen])
                actions = actions[blocklen:]
        except:
            print(docname)


def dingshi():
    nowtime=time.strftime("%H", time.localtime())
    if nowtime=='04':
        solve()
        print('更新完成')
        time.sleep(79200)
    else:
        time.sleep(3600)
    dingshi()
dingshi()