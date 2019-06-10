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


name='wenzhang.json'
f=open(name)
ff=open(name+'0','w')
for line in f:
    line=json.loads(line)
    ff.write(json.dumps(line,ensure_ascii=False)+'\n')
ff.close()
