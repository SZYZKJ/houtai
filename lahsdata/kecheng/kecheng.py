#!/usr/bin/python
import csv
from flask import Flask
from flask import request
import json
import time
import random
from flask_cors import *
import os

datapath = '/home/ubuntu/data/lianailianmeng/data/opendata/kecheng/'
os.chdir(datapath)

app = Flask(__name__)
app.debug = True
CORS(app, supports_credentials=True)

kechengdict = {}
f = open('kecheng.json')
for line in f:
    line = json.loads(line)
    kechengdict[line['wendangid']] = line
f.close()


@app.route('/api/fasonggonggao', methods=['POST'])
def fasonggonggao():
    wendang = json.loads(str(request.stream.read(), encoding='utf8'))
    wendangid = wendang['wendangid']
    kechengdict[wendangid] = wendang
    f = open('kecheng.json', 'w')
    for newwendangid in kechengdict:
        f.write(json.dumps(kechengdict[newwendangid], ensure_ascii=False) + '\n')
    f.close()
    return json.dumps({'MSG': 'YES'}, ensure_ascii=False)


@app.route('/api/getfawenhao', methods=['POST'])
def getfawenhao():
    wendangid = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return json.dumps({'wendangid': wendangid}, ensure_ascii=False)


@app.route('/api/baocunimage', methods=['POST'])
def baocunimage():
    wendangid = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = wendangid + '.jpg'
    f = open(datapath + filename, 'wb')
    imagedata = request.stream.read()
    f.write(imagedata)
    f.close()
    url = 'https://www.lianaizhuli.com/kecheng/' + filename
    return json.dumps({'url': url}, ensure_ascii=False)


@app.route('/api/getgonggaoguanli', methods=['POST'])
def getgonggaoguanli():
    dataTable = []
    for wendangid in kechengdict:
        dataTable.append(kechengdict[wendangid])
    return json.dumps({'dataTable': dataTable}, ensure_ascii=False)


@app.route('/api/deletegonggao', methods=['POST'])
def deletegonggao():
    params = json.loads(str(request.stream.read(), encoding='utf8'))
    wendangid = params['wendangid']
    if wendangid in kechengdict:
        kechengdict.pop(wendangid)
        f = open('kecheng.json', 'w')
        for newwendangid in kechengdict:
            f.write(json.dumps(kechengdict[newwendangid], ensure_ascii=False) + '\n')
        f.close()
    dataTable = []
    for wendangid in kechengdict:
        dataTable.append(kechengdict[wendangid])
    return json.dumps({'dataTable': dataTable}, ensure_ascii=False)


@app.route('/api/getgonggao', methods=['POST'])
def getgonggao():
    params = json.loads(str(request.stream.read(), encoding='utf8'))
    wendangid = params['wendangid']
    if wendangid in kechengdict:
        return json.dumps({'data': kechengdict[wendangid]}, ensure_ascii=False)

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=6888, debug=True)
