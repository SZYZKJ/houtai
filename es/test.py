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
escopy = Elasticsearch([{"host": "119.29.67.239", "port": 9218}])


openid='oz7z64liSPmlzHped8ATXf23jqyI'
unionid='ofIsD1YLw3q_1v4d2NgX9GrS3ZEM'


es.delete(index='userinfo',doc_type='userinfo',id=unionid)