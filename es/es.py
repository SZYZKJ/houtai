from elasticsearch import Elasticsearch
from elasticsearch import helpers
import csv
import os
import time
from random import randint
from requests import post

datapath = '/home/ubuntu/data/lianaihuashu/data'
os.chdir(datapath)
tulinkey = [
    '1dea0cd4b44a4613b19d0a02442624a8',
    '2948b84b2f904816874708150395e68f',
    '4519cc99a42448cdac866f419998149f',
    '717a53a9d4cd49b49a85fe44c3828e5c',
    '3134aa17d10345048dc355311a794326',
    'b511ba9870994994b4fb778ffcbb734b',
    'e756e4c656a343c9b51ccce278344885',
    'adcd8ca4d9cf45ec9853273cc14c9c17',
    '4bb221b38e984b09854980c1a69304d0',
]
es = Elasticsearch([{"host": "182.254.227.188", "port": 9218, "timeout": 3600}])


def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class Lianailianmeng_ES:
    emoji = {'\ue412': ["喜极而泣，😂这个是最新的撩汉表情", "怎么了呀，跟我说说看", "原谅我放荡不羁的笑声"],
             '\ue40e': ["一双天使的眼睛被你用坏了", "你这是在糟蹋我们的革命友谊", "这小眼神，秒杀了多少像我一样的帅哥"],
             '\ue409': ['突然好嫌弃你（打压）']}

    def search(self, params):
        newquery = params['query']
        returnlist = []
        search = {'query': {'match': {'chat_name': newquery}}}
        Docs = es.search(index='liaomeihuashu', doc_type='liaomeihuashu', body=search, size=10)
        Docs = Docs['hits']['hits']
        key = tulinkey[0]
        tulinkey.append(tulinkey[0])
        tulinkey.pop(0)
        resp = post("http://www.tuling123.com/openapi/api",
                    data={"key": key, "info": newquery})
        resp = resp.json()
        if resp['code'] == 100000:
            returnlist.append({'MM': params['query'], 'GG': resp['text']})
        for doc in Docs:
            returnlist.append(doc['_source'])
        if len(Docs) == 0:
            for emo in self.emoji:
                if emo in newquery:
                    returnlist.append({'MM': emo, 'GG': self.emoji[emo]})
            query = newquery
            query = query.replace('+', '\+')
            query = query.replace('-', '\-')
            query = query.replace('=', '\=')
            query = query.replace('&', '\&')
            query = query.replace('|', '\|')
            query = query.replace('>', '\>')
            query = query.replace('<', '\<')
            query = query.replace('!', '\!')
            query = query.replace('(', '\(')
            query = query.replace(')', '\)')
            query = query.replace('/', '\/')
            query = query.replace(':', '\:')
            query = query.replace('*', '\*')
            query = query.replace('~', '\~')
            query = query.replace('[', '\[')
            query = query.replace(']', '\]')
            query = query.replace('^', '\^')
            query = query.replace('{', '\{')
            query = query.replace('}', '\}')
            query = query.replace('?', '\?')
            query = query.replace(' ', '\ ')
            query = query.replace('"', '\"')
            search = {'query': {'query_string': {"query": query}}}
            Docs = es.search(index='liaomeihuashu', doc_type='liaomeihuashu', body=search, size=10)
            Docs = Docs['hits']['hits']
            for doc in Docs:
                returnlist.append(doc['_source'])
        newresponse = ''
        for line in returnlist:
            if 'MM' in line:
                newresponse += 'MM:'
                newresponse += line['MM']
                newresponse += 'GG:'
                newresponse += line['GG']
                newresponse += '\n'
            else:
                for newline in line['chat_content']:
                    if newline['ans_sex'] == 1:
                        newresponse += 'GG:'
                    else:
                        newresponse += 'MM:'
                    newresponse += newline['content'] + '\n'
                newresponse += '\n'
                if len(newresponse) > 300:
                    break
        return newresponse
