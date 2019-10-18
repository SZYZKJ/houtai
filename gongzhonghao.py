from gevent import monkey
from gevent import pywsgi

monkey.patch_all()
import sys
import io
import os
import re
import random
import json
import csv
from Crypto.Cipher import AES
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from flask import Flask, request
from flask_cors import *
import time
from base64 import b64encode
import base64
import requests
import urllib.request
import string
import hashlib
import xml.etree.ElementTree as ET
import logging
from basic import Basic
from weixin_app import handel
from weixin_app import receive
from weixin_app import reply
from msg_crypto.WXBizMsgCrypt import WXBizMsgCrypt

app = Flask(__name__)
CORS(app, supports_credentials=True)
wangzhi = 'http://www.lianaizhuli.com/'
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log/log.txt")
handler.setLevel(logging.INFO)
es = Elasticsearch([{"host": "182.254.227.188", "port": 9218}])
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
dingyuehaoappid = 'wxc1deae6a065dffa9'
encodingAESKey = "UmBlx5gtFv7zravWwE9tCLjC99qPxRZQDPDdfeFCBfg"
token = 'lianailianmeng'
os.chdir('/home/ubuntu/data/lianailianmeng/data')
HD = handel.Handel()


@app.route("/v1/api/contribute", methods=["GET", "POST"])
def contribute():
    try:
        data = json.loads(str(request.stream.read(), encoding='utf8'))['params']
        if 'images' in data:
            data.pop('images')
        f = open('feedback/contribute.json', 'a+')
        f.write(json.dumps(data) + '\n')
        f.close()
    except Exception as e:
        print(e)
    result = {'result': 'ok'}
    return json.dumps(result)


@app.route("/v1/api/feedback", methods=["GET", "POST"])
def feedback():
    try:
        data = json.loads(str(request.stream.read(), encoding='utf8'))['params']
        if 'images' in data:
            data.pop('images')
        f = open('feedback/feedback.json', 'a+')
        f.write(json.dumps(data) + '\n')
        f.close()
    except Exception as e:
        print(e)
    result = {'result': 'ok'}
    return json.dumps(result)


@app.route("/v1/api/addimage", methods=["GET", "POST"])
def addimage():
    try:
        recdata = request.stream.read()
        uuid = re.compile(b'name="uuid"\r\n\r\n.*?\r\n')
        image_id = re.compile(b'name="image_id"\r\n\r\n.*?\r\n')
        dataname = re.compile(b'filename=".*?"')
        uuid = str(uuid.search(recdata).group()).split('\\r\\n')[-2]
        dataname = str(dataname.search(recdata).group()).split('"')[-2]
        t = 0
        l, r = 0, 0
        for i in range(len(recdata)):
            if recdata[i:i + 2] == b'\r\n':
                t += 1
                if t == 28:
                    l = i + 2
                    break
        i = len(recdata) - 4
        while (i > 0):
            i -= 1
            if recdata[i:i + 2] == b'\r\n':
                r = i
                break
        f = open('./feedback/images/' + uuid + '_' + dataname, 'wb')
        f.write(recdata[l:r])
        f.close()
    except Exception as e:
        print(e)
    result = {'result': 'ok'}
    return json.dumps(result)


@app.route("/v1/api/delimage", methods=["GET", "POST"])
def deletePic():
    result = {'result': 'ok'}
    return json.dumps(result)


@app.route("/", methods=["GET", "POST"])
def index():
    return "ok"


@app.route("/v1/lianailianmeng", methods=["GET", "POST"])
def lianailianmeng():
    if request.method == "GET":
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        data = [token, timestamp, nonce]
        data.sort()
        newstring = data[0] + data[1] + data[2]
        sha1 = hashlib.sha1()
        sha1.update(newstring.encode())
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return echostr
    elif request.method == 'POST':
        rec_xml = request.stream.read()
        if request.values.get('encrypt_type'):
            encrypt_type = request.values.get('encrypt_type')
            if encrypt_type == 'aes':
                timestamp = request.values.get('timestamp')
                nonce = request.values.get('nonce')
                msg_signature = request.values.get('msg_signature')
                encrypt_decrypt = WXBizMsgCrypt(token, encodingAESKey, dingyuehaoappid)
                (ret, decrypt_xml) = encrypt_decrypt.DecryptMsg(rec_xml, msg_signature, timestamp, nonce)
                recMsg = receive.parse_xml(decrypt_xml)
                gzhid=recMsg.FromUserName
                accessToken = Basic().get_access_token('gzh')
                unionidurl='https://api.weixin.qq.com/cgi-bin/user/info?access_token='+accessToken+'&openid='+gzhid+'&lang=zh_CN'
                response = requests.get(unionidurl)
                gzhuserinfo=response.json()
                gzhuserinfo['gzhid']=gzhid
                gzhuserinfo.pop('openid')
                unionid=gzhuserinfo['unionid']
                resdata=gzhuserinfo
                try:
                    userinfodoc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
                    userinfodoc.update(gzhuserinfo)
                    resdata = userinfodoc
                except:
                    resdata['addtime'] = getTime()
                    resdata['vipdengji'] = 0
                    resdata['viptime'] = int(time.time()) + viptime[0]
                    resdata['sijiaotime'] = 0
                    resdata['xiaofeicishu'] = 0
                    resdata['xiaofeizonge'] = 0
                es.index(index='userinfo', doc_type='userinfo', id=unionid, body=resdata)
                repMsg = HD.handel_msg(recMsg)
                xml = repMsg.send()
                (ret, encrypt_xml) = encrypt_decrypt.EncryptMsg(xml, nonce)
                return encrypt_xml
        else:
            recMsg = receive.parse_xml(rec_xml)
            repMsg = handel.handel_msg(recMsg)
            rep_xml = repMsg.send()
            return rep_xml


@app.route("/v1/yuzikeji", methods=["GET", "POST"])
def yuzikeji():
    if request.method == "GET":
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        data = [token, timestamp, nonce]
        data.sort()
        newstring = data[0] + data[1] + data[2]
        sha1 = hashlib.sha1()
        sha1.update(newstring.encode())
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return echostr
    elif request.method == 'POST':
        rec_xml = request.stream.read()
        if request.values.get('encrypt_type'):
            encrypt_type = request.values.get('encrypt_type')
            if encrypt_type == 'aes':
                timestamp = request.values.get('timestamp')
                nonce = request.values.get('nonce')
                msg_signature = request.values.get('msg_signature')
                encrypt_decrypt = WXBizMsgCrypt(token, encodingAESKey, fuwuhaoappid)
                (ret, decrypt_xml) = encrypt_decrypt.DecryptMsg(rec_xml, msg_signature, timestamp, nonce)
                recMsg = receive.parse_xml(decrypt_xml)
                repMsg = HD.handel_msg(recMsg)
                xml = repMsg.send()
                (ret, encrypt_xml) = encrypt_decrypt.EncryptMsg(xml, nonce)
                return encrypt_xml
        else:
            recMsg = receive.parse_xml(rec_xml)
            repMsg = handel.handel_msg(recMsg)
            rep_xml = repMsg.send()
            return rep_xml


@app.route("/v1/getKechengList", methods=["POST"])
def getKechengList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis(
        {'unionid': unionid, 'time': getTime(), 'event': 'getKechengList', 'detail': 'getKechengList',
         'type': '1'})
    retdata = []
    search = {"query": {"match_all": {}}}
    Docs = es.search(index='kechenglist', doc_type='kechenglist', body=search, size=10000)
    Docs = Docs['hits']['hits']
    try:
        goumaidoc = es.get(index='kechenggoumai', doc_type='kechenggoumai', id=unionid)['_source']
        goumaidoc['data'] = json.loads(goumaidoc['data'])
    except:
        goumaidoc = {}
        goumaidoc['data'] = {}
    for doc in Docs:
        doc = doc['_source']
        if doc['id'] in goumaidoc['data']:
            doc['yigoumai'] = 1
        else:
            doc['yigoumai'] = 0
        retdata.append(doc)
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata}))


@app.route("/v1/getKecheng", methods=["POST"])
def getKecheng():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        kechengid = params['kechengid']
        neirongid = params['neirongid']
        kefenxiang = params['kefenxiang']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'unionid': unionid, 'time': getTime(), 'event': 'getKecheng', 'detail': neirongid,
                'type': '1'})
    if kefenxiang == '0':
        try:
            goumaidoc = es.get(index='kechenggoumai', doc_type='kechenggoumai', id=unionid)['_source']
            goumaidoc['data'] = json.loads(goumaidoc['data'])
            if kechengid in goumaidoc['data']:
                kefenxiang = '1'
        except:
            None
    if kefenxiang == '1':
        doc = es.get(index='kecheng', doc_type='kecheng', id=neirongid)['_source']
        return encrypt(json.dumps({'MSG': 'YES', 'data': doc}))
    return encrypt(json.dumps({'MSG': 'NO'}))


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 13888), app)
    server.serve_forever()
