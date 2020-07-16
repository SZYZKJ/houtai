from elasticsearch import Elasticsearch
from elasticsearch import helpers
import csv
import os
import time
import json
import random
import requests

datapath = '/home/ubuntu/data/lianaihuashu/data'
os.chdir(datapath)
blocklen = 100000

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
es = Elasticsearch([{"host": "182.254.227.188", "port": 9218, "timeout": 3600}])
actions = []
# es.indices.delete(index='liaomeihuashu')
# es.indices.delete(index='liaomeitaolu')
# es.indices.delete(index='tuweiqinghua')
# es.indices.delete(index='kechenglist')
# es.indices.delete(index='kecheng')
# es.indices.delete(index='sijiao')
# es.indices.delete(index='xingxiangjianshe')
# es.indices.delete(index='liaomeishizhanlist')
# es.indices.delete(index='liaomeishizhan')
# es.indices.delete(index='baikelist')
# es.indices.delete(index='baike')
# es.indices.delete(index='wendalist')
# es.indices.delete(index='wenda')
# es.indices.delete(index='xinliceshilist')
# es.indices.delete(index='xinliceshi')
# es.indices.delete(index='xinliceshiret')
# es.indices.delete(index='search')
es.indices.delete(index='biaoqing')
# es.indices.delete(index='fenxiao')
# es.indices.delete(index='userhis')

# ret_data = es.indices.create(index='liaomeihuashu', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='liaomeitaolu', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='tuweiqinghua', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='kechenglist', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='kecheng', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='sijiao', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='xingxiangjianshe', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='liaomeishizhanlist', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='liaomeishizhan', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='baikelist', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='baike', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='wendalist', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='wenda', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='xinliceshilist', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='xinliceshi', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='xinliceshiret', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='search', body=lianaizhuli_index, ignore=400)
# print(ret_data)
ret_data = es.indices.create(index='biaoqing', body=lianaizhuli_index, ignore=400)
print(ret_data)
# ret_data = es.indices.create(index='fenxiao', body=lianaizhuli_index, ignore=400)
# print(ret_data)
# ret_data = es.indices.create(index='userhis', body=lianaizhuli_index, ignore=400)
# print(ret_data)

# with open('liaomeihuashu.json', 'r') as f:
#     for line in f:
#         item = json.loads(line)
#         action = {
#             "_index": "liaomeihuashu",
#             "_type": "liaomeihuashu",
#             "_source": item
#         }
#         actions.append(action)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('liaomeitaolu.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         item['chakan'] = 0
#         action = {
#             "_index": "liaomeitaolu",
#             "_type": "liaomeitaolu",
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('tuweiqinghua.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "tuweiqinghua",
#             "_type": "tuweiqinghua",
#             "_source": item,
#             '_id': item['id']
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('kecheng.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "kecheng",
#             "_type": "kecheng",
#             '_id': item['wendangid'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('kechenglist.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "kechenglist",
#             "_type": "kechenglist",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('sijiao.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "sijiao",
#             "_type": "sijiao",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
#
# with open('xingxiangjianshe.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "xingxiangjianshe",
#             "_type": "xingxiangjianshe",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('liaomeishizhanlist.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "liaomeishizhanlist",
#             "_type": "liaomeishizhanlist",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('liaomeishizhan.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "liaomeishizhan",
#             "_type": "liaomeishizhan",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]

# with open('baikelist.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "baikelist",
#             "_type": "baikelist",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('baike.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "baike",
#             "_type": "baike",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('wendalist.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "wendalist",
#             "_type": "wendalist",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('wenda.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "wenda",
#             "_type": "wenda",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('xinliceshilist.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "xinliceshilist",
#             "_type": "xinliceshilist",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('xinliceshi.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "xinliceshi",
#             "_type": "xinliceshi",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
#
# with open('xinliceshiret.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "xinliceshiret",
#             "_type": "xinliceshiret",
#             '_id': item['id'],
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]
# #
# with open('search.json', 'r') as f:
#     for line in f:
#         item = json.loads(line.strip())
#         action = {
#             "_index": "search",
#             "_type": "search",
#             "_source": item
#         }
#         actions.append(action)
# random.shuffle(actions)
# while len(actions):
#     helpers.bulk(es, actions[:blocklen])
#     actions = actions[blocklen:]

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
    helpers.bulk(es, actions[:blocklen])
    actions = actions[blocklen:]
print('创建结束！')
