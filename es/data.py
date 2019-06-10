from elasticsearch import Elasticsearch
from elasticsearch import helpers
import csv
import os
import time
import json
import random
import requests

datapath = '/home/ubuntu/data/lianaizhuli/data'
os.chdir(datapath)
blocklen=100000

class Lianaizhuli_ES:
    es = Elasticsearch([{"host": "182.254.227.188", "port": 9218, "timeout": 3600}])

    def __init__(self):
        # self.es.indices.delete(index='huashu')
        # self.es.indices.delete(index='guanli')
        self.es.indices.delete(index='methodology')
        self.es.indices.delete(index='wenzhang')
        self.es.indices.delete(index='ganhuo')
        self.es.indices.delete(index='kecheng')
        self.es.indices.delete(index='tuweiqinghua')
        self.es.indices.delete(index='biaoqing')
        if self.es.indices.exists(index='wenzhang') is not True:
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
            # ret_huashu = self.es.indices.create(index='huashu', body=lianaizhuli_index, ignore=400)
            # print(ret_huashu)
            # ret_guanli = self.es.indices.create(index='guanli', body=lianaizhuli_index, ignore=400)
            # print(ret_guanli)
            ret_methodology = self.es.indices.create(index='methodology', body=lianaizhuli_index, ignore=400)
            print(ret_methodology)
            ret_wenzhang = self.es.indices.create(index='wenzhang', body=lianaizhuli_index, ignore=400)
            print(ret_wenzhang)
            ret_ganhuo = self.es.indices.create(index='ganhuo', body=lianaizhuli_index, ignore=400)
            print(ret_ganhuo)
            ret_kecheng = self.es.indices.create(index='kecheng', body=lianaizhuli_index, ignore=400)
            print(ret_kecheng)
            ret_tuweiqinghua = self.es.indices.create(index='tuweiqinghua', body=lianaizhuli_index, ignore=400)
            print(ret_tuweiqinghua)
            ret_biaoqing = self.es.indices.create(index='biaoqing', body=lianaizhuli_index, ignore=400)
            print(ret_biaoqing)
            # ret_userhis = self.es.indices.create(index='userhis', body=lianaizhuli_index, ignore=400)
            # print(ret_userhis)
            # ret_userinfo = self.es.indices.create(index='userinfo', body=lianaizhuli_index, ignore=400)
            # print(ret_userinfo)
            # ret_userzhifu = self.es.indices.create(index='userzhifu', body=lianaizhuli_index, ignore=400)
            # print(ret_userzhifu)
            actions = []
            # with open('huashu.csv', 'r') as f:
            #     for line in csv.reader(f):
            #         huashulist = line[1].strip().split('\n')
            #         if len(huashulist) > 1:
            #             for index in range(len(huashulist)):
            #                 huashulist[index] = huashulist[index][2:]
            #         action = {
            #             "_index": "huashu",
            #             "_type": "huashu",
            #             "_source": {'MM': line[0].strip(), 'GG': huashulist}
            #         }
            #         actions.append(action)
            # while len(actions):
            #     helpers.bulk(self.es, actions[:blocklen])
            #     actions=actions[blocklen:]
            # with open('guanli.json', 'r') as f:
            #     for line in f:
            #         item = json.loads(line.strip())
            #         action = {
            #             "_index": "guanli",
            #             "_type": "guanli",
            #             "_source": item
            #         }
            #         actions.append(action)
            # while len(actions):
            #     helpers.bulk(self.es, actions[:blocklen])
            #     actions=actions[blocklen:]
            with open('methodology.json', 'r') as f:
                for line in f:
                    item = json.loads(line.strip())
                    item['chakan'] = 0
                    action = {
                        "_index": "methodology",
                        "_type": "methodology",
                        "_source": item
                    }
                    actions.append(action)
            random.shuffle(actions)
            while len(actions):
                helpers.bulk(self.es, actions[:blocklen])
                actions = actions[blocklen:]
            with open('wenzhang.json', 'r') as f:
                for line in f:
                    item = json.loads(line.strip())
                    action = {
                        "_index": "wenzhang",
                        "_type": "wenzhang",
                        '_id': item['id'],
                        "_source": item,
                    }
                    actions.append(action)
            random.shuffle(actions)
            while len(actions):
                helpers.bulk(self.es, actions[:blocklen])
                actions = actions[blocklen:]
            with open('ganhuo.json', 'r') as f:
                for line in f:
                    item = json.loads(line.strip())
                    action = {
                        "_index": "ganhuo",
                        "_type": "ganhuo",
                        '_id': item['id'],
                        "_source": item,
                    }
                    actions.append(action)
            random.shuffle(actions)
            while len(actions):
                helpers.bulk(self.es, actions[:blocklen])
                actions = actions[blocklen:]
            with open('kecheng.json', 'r') as f:
                for line in f:
                    item = json.loads(line.strip())
                    action = {
                        "_index": "kecheng",
                        "_type": "kecheng",
                        "_source": item
                    }
                    actions.append(action)
            random.shuffle(actions)
            while len(actions):
                helpers.bulk(self.es, actions[:blocklen])
                actions = actions[blocklen:]
            with open('tuweiqinghua.json', 'r') as f:
                for line in f:
                    item = json.loads(line.strip())
                    action = {
                        "_index": "tuweiqinghua",
                        "_type": "tuweiqinghua",
                        "_source": item,
                        '_id':item['chatId']
                    }
                    actions.append(action)
            random.shuffle(actions)
            while len(actions):
                helpers.bulk(self.es, actions[:blocklen])
                actions = actions[blocklen:]
            with open('biaoqing.json', 'r') as f:
                for line in f:
                    item = json.loads(line.strip())
                    action = {
                        "_index": "biaoqing",
                        "_type": "biaoqing",
                        "_source": item
                    }
                    actions.append(action)
            while len(actions):
                print(len(actions))
                helpers.bulk(self.es, actions[:blocklen])
                actions = actions[blocklen:]
            print('创建结束！')

    def add(self):
        return None

    def delete(self):
        return None

    def updata(self):
        return None


LAES = Lianaizhuli_ES()

# es = Elasticsearch([{"host": "182.254.227.188", "port": 9218, "timeout": 3600}])
# nowtime='2019-01-18'
# body = {"query": {"match_phrase_prefix": {"time": nowtime}}}
# Docs=es.search(index='userhis',doc_type='userhis',body=body,size=1000)
# for doc in Docs['hits']['hits']:
#     print(doc['_source']['openid'])
