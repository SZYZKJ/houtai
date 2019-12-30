from gevent import monkey
from gevent import pywsgi

monkey.patch_all()
import sys
import io
import os
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
from urllib import parse
import string
import hashlib
from WXBizMsgCrypt import WXBizMsgCrypt
from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
sockets = Sockets(app)
CORS(app, supports_credentials=True)
es = Elasticsearch([{"host": "182.254.227.188", "port": 9218, "timeout": 3600}])
histype = {'searchLiaomeihuashu': 0, 'searchBiaoqing': 0, 'searchBaike': 0, 'getLiaomeitaoluList': 0,
           'getXingxiangjianshe': 0, 'getLiaomeishizhan': 0, 'getKecheng': 0, 'getTuweiqinghua': 0, 'getBaike': 0,
           'getWenda': 0, 'getCeshidaan': 0, 'setDianzanshoucang': 0, 'setJilu': 0, }
key = "pangyuming920318"
iv = "abcdefabcdefabcd"
appid = 'wxa9ef833cef143ce1'
token = 'lianailianmeng'
secret = '574ba86bc66b664ab42e4d60276afb7c'
EncodingAESKey = "zo84lZOejrVKHTyoe5D18QNHCWothe0FovOxIubrnKj"
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * bytes(chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), encoding='utf8')
unpad = lambda s: s[0:-ord(s[-1])]
datapath = '/home/ubuntu/data/lianailianmeng/data'
os.chdir(datapath)

hisdata = {}
newhisdata = {}
f = open('shujuzhongxin.json')
for line in f:
    hisdata = json.loads(line)
    newhisdata = json.loads(line)
f.close()

constws = {}
sendws = {}
MsgId = {}
access_tokentime = []


def getaccess_token():
    global access_tokentime
    access_token = ''
    if len(access_tokentime) == 0 or access_tokentime[1] < int(time.time()):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret
        response = requests.get(url)
        response = response.json()
        access_token = response['access_token']
        access_tokentime = []
        access_tokentime.append(access_token)
        access_tokentime.append(int(time.time() + 3600))
    else:
        access_token = access_tokentime[0]
    return access_token


def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def encrypt(encrypting):
    encrypting = bytes(encrypting, encoding='utf8')
    aes = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(aes.encrypt(pad(encrypting)))


def decrypt(encrypted):
    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(bytes.fromhex(str(encrypted)[2:-1])).decode('utf8')
    return unpad(decrypted)


def decryptweixin(encrypted, weixinkey, weixiniv):
    encrypted = base64.b64decode(encrypted)
    weixinkey = base64.b64decode(weixinkey)
    weixiniv = base64.b64decode(weixiniv)
    aes = AES.new(weixinkey, AES.MODE_CBC, weixiniv)
    decrypted = aes.decrypt(encrypted)
    return json.loads(decrypted[:-ord(decrypted[len(decrypted) - 1:])])


@app.route("/test/xiaFashuruzhuangtai", methods=["POST"])
def xiaFashuruzhuangtai():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        command = params['command']
    except Exception as e:
        print(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    access_token = getaccess_token()
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/typing?access_token=' + access_token
    openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['openid']
    values = {
        "touser": openid,
        "command": command
    }
    data = json.dumps(values).encode('utf8')
    reponse = urllib.request.Request(url=url, data=data, method='POST')
    html = urllib.request.urlopen(reponse).read().decode('utf-8')
    return encrypt(html)


def faSongwenhouyu(unionid):
    textvalue = "您好，我是恋爱联盟客服薇薇，很高兴为您服务。"
    access_token = getaccess_token()
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + access_token
    openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['openid']
    values = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": textvalue
        }
    }
    data = json.dumps(values, ensure_ascii=False).encode('utf8')
    reponse = urllib.request.Request(url=url, data=data, method='POST')
    html = urllib.request.urlopen(reponse).read().decode('utf-8')
    html = json.loads(html)
    content = {
        "Content": textvalue,
        "ToUserName": "gh_95cc82b21cba",
        "person": 1,
        "MsgType": "text",
        "MsgId": int(str(int(time.time())) + str(random.randint(100000000, 999999999))),
        "FromUserName": openid,
        "CreateTime": int(time.time())
    }
    if html['errcode'] == 0:
        try:
            doc = es.get(index='kefu', doc_type='kefu', id=unionid)
            doc = doc['_source']
            doc['datalist'].append(content)
            doc['updatatime'] = getTime()
            doc['unread'] += 1
            doc['zuijin'] = textvalue
            es.index(index='kefu', doc_type='kefu', id=unionid, body=doc)
        except Exception as e:
            doc = {}
            doc['unionid'] = unionid
            doc['updatatime'] = getTime()
            user = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
            doc['avatarUrl'] = user['avatarUrl']
            doc['nickName'] = user['nickName']
            doc['datalist'] = [content]
            doc['unread'] = 1
            doc['zuijin'] = textvalue
            es.index(index='kefu', doc_type='kefu', id=unionid, body=doc)
        getKefuList('')


@app.route("/test/faSongtext", methods=["POST"])
def faSongtext():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        textvalue = params['textvalue']
    except Exception as e:
        print(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    access_token = getaccess_token()
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + access_token
    openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['openid']
    values = {
        "touser": openid,
        "msgtype": "text",
        "text": {
            "content": textvalue
        }
    }
    data = json.dumps(values, ensure_ascii=False).encode('utf8')
    reponse = urllib.request.Request(url=url, data=data, method='POST')
    html = urllib.request.urlopen(reponse).read().decode('utf-8')
    html = json.loads(html)
    content = {
        "Content": textvalue,
        "ToUserName": "gh_95cc82b21cba",
        "person": 1,
        "MsgType": "text",
        "MsgId": int(str(int(time.time())) + str(random.randint(100000000, 999999999))),
        "FromUserName": openid,
        "CreateTime": int(time.time())
    }
    if html['errcode'] == 0:
        try:
            doc = es.get(index='kefu', doc_type='kefu', id=unionid)
            doc = doc['_source']
            doc['datalist'].append(content)
            doc['updatatime'] = getTime()
            doc['unread'] = 0
            doc['zuijin'] = textvalue
            es.index(index='kefu', doc_type='kefu', id=unionid, body=doc)
        except Exception as e:
            doc = {}
            doc['unionid'] = unionid
            doc['updatatime'] = getTime()
            user = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
            doc['avatarUrl'] = user['avatarUrl']
            doc['nickName'] = user['nickName']
            doc['datalist'] = [content]
            doc['unread'] = 0
            doc['zuijin'] = textvalue
            es.index(index='kefu', doc_type='kefu', id=unionid, body=doc)
        getKefuList(unionid)
    return encrypt(json.dumps(html))


@app.route("/test/upUnread", methods=["POST"])
def upUnread():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        print(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    doc = es.get(index='kefu', doc_type='kefu', id=unionid)
    doc = doc['_source']
    doc['unread'] = 0
    es.index(index='kefu', doc_type='kefu', id=unionid, body=doc)
    getKefuList('')
    return encrypt(json.dumps({'MSG': 'OK'}))


@sockets.route('/test/getKefuList', methods=['POST'])
def getKefuList(ws):
    global constws, sendws
    if type(ws) == type(""):
        time.sleep(1)
        if ws != '':
            doc = es.get(index='kefu', doc_type='kefu', id=ws)['_source']
            newconstws = constws.copy()
            for newws in newconstws:
                if constws[newws] == ws:
                    try:
                        sendws[newws].send(
                            encrypt(json.dumps({'MSG': 0, 'unionid': ws, 'data': doc})).decode('utf8'))
                    except Exception as e:
                        print(e)
                        constws.pop(newws)
                        sendws.pop(newws)
        nowtime = time.strftime("%Y-%m", time.localtime())
        body = {"query": {"match_phrase_prefix": {"updatatime": nowtime}}}
        Docs = es.search(index='kefu', doc_type='kefu', body=body, size=10000)
        Docs = Docs['hits']['hits']
        retdata = []
        for doc in Docs:
            doc['_source']['updatatime'] = doc['_source']['updatatime'][5:16]
            retdata.append(doc['_source'])
        newconstws = constws.copy()
        try:
            for newws in newconstws:
                if not sendws[newws].closed:
                    if constws[newws] == '':
                        try:
                            sendws[newws].send(
                                encrypt(json.dumps({'MSG': 1, 'unionid': '', 'data': retdata})).decode('utf8'))
                        except Exception as e:
                            print(e)
                            constws.pop(newws)
                            sendws.pop(newws)
                else:
                    constws.pop(newws)
                    sendws.pop(newws)
        except Exception as e:
            print(e)
    while type(ws) != type(""):
        if ws.closed:
            break
        time.sleep(1)
        try:
            a = ws.receive()
            print(a)
            if a:
                params = json.loads(decrypt(a.encode('utf8')))
                unionid = params['unionid']
                constws[str(ws)] = unionid
                sendws[str(ws)] = ws
                if unionid == '':
                    nowtime = time.strftime("%Y-%m", time.localtime())
                    body = {"query": {"match_phrase_prefix": {"updatatime": nowtime}}}
                    Docs = es.search(index='kefu', doc_type='kefu', body=body, size=10000)
                    Docs = Docs['hits']['hits']
                    retdata = []
                    for doc in Docs:
                        doc['_source']['updatatime'] = doc['_source']['updatatime'][5:16]
                        retdata.append(doc['_source'])
                    ws.send(encrypt(json.dumps({'MSG': 1, 'unionid': '', 'data': retdata})).decode('utf8'))
                else:
                    ws.send(encrypt(json.dumps({'MSG': 2})).decode('utf8'))
        except Exception as e:
            print(e)


@app.route("/test/kefutuisong", methods=["GET", "POST"])
def kefutuisong():
    global MsgId
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
    else:
        aaaa = json.loads(request.stream.read().decode('utf8'))
        timestamp = request.values.get('timestamp')
        nonce = request.values.get('nonce')
        msg_signature = request.values.get('msg_signature')
        encrypt_decrypt = WXBizMsgCrypt(token, EncodingAESKey, appid)
        (ret, content) = encrypt_decrypt.DecryptMsg(aaaa['Encrypt'], msg_signature, timestamp, nonce)
        content = json.loads(content.decode('utf8'))
        if 'MsgId' in content:
            if content['MsgId'] in MsgId:
                return "SUCCESS"
            if len(MsgId) >= 9999:
                MsgId = {}
            MsgId[content['MsgId']] = 0
        content['person'] = 0
        if content['MsgType'] != 'event':
            search = {'query': {'match': {'openid': content['FromUserName']}}}
            unionid = \
            es.search(index='userinfo', doc_type='userinfo', body=search, size=1)['hits']['hits'][0]['_source'][
                'unionid']
            try:
                doc = es.get(index='kefu', doc_type='kefu', id=unionid)
                doc = doc['_source']
                doc['datalist'].append(content)
                doc['updatatime'] = getTime()
                doc['unread'] += 1
                if content['MsgType'] == 'image':
                    doc['zuijin'] = '[图片]'
                else:
                    doc['zuijin'] = content['Content']
                es.index(index='kefu', doc_type='kefu', id=unionid, body=doc)
            except Exception as e:

                doc = {}
                doc['unionid'] = unionid
                doc['updatatime'] = getTime()
                user = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
                doc['unionid'] = user['unionid']
                doc['avatarUrl'] = user['avatarUrl']
                doc['nickName'] = user['nickName']
                doc['datalist'] = [content]
                doc['unread'] = 1
                if content['MsgType'] == 'image':
                    doc['zuijin'] = '[图片]'
                else:
                    doc['zuijin'] = content['Content']
                es.index(index='kefu', doc_type='kefu', id=unionid, body=doc)
            getKefuList(unionid)
        elif content['Event'] == 'user_enter_tempsession':
            if (content['FromUserName'] + str(content['CreateTime'])) in MsgId:
                return "SUCCESS"
            if len(MsgId) >= 9999:
                MsgId = {}
            MsgId[content['FromUserName'] + str(content['CreateTime'])] = 0
            faSongwenhouyu(unionid)
        return "SUCCESS"


@app.route("/test/getChengGong", methods=["POST"])
def getChengGong():
    try:
        params = json.loads(decrypt(request.stream.read()))
        yidingchenggong = params['yidingchenggong']
    except Exception as e:
        print(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    global hisdata, newhisdata
    jintian = time.strftime("%Y-%m-%d", time.localtime())
    nowtime = time.strftime("%Y%m%d", time.localtime())
    hisdatajintian = hisdata['jintian'][:4] + hisdata['jintian'][5:7] + hisdata['jintian'][8:10]
    if (jintian != hisdata['jintian']):
        searchtian = {"query": {"match_phrase_prefix": {"addtime": hisdata['jintian']}}}
        Docs = es.search(index='userinfo', doc_type='userinfo', body=searchtian, size=1000, scroll="1m")
        scroll = Docs['_scroll_id']
        jintianyonghushu = len(Docs['hits']['hits'])
        jintianfufeiyonghushu = 0
        jintianfufeicishu = 0
        jintianfufeizonge = 0
        while 1:
            try:
                Docs = es.scroll(scroll_id=scroll, scroll="1m")
                if (len(Docs['hits']['hits']) == 0):
                    break
                scroll = Docs['_scroll_id']
                jintianyonghushu += len(Docs['hits']['hits'])
            except:
                break
        searchtian = {"query": {"match_phrase_prefix": {"updatatime": hisdatajintian}}}
        Docs = es.search(index='userzhifu', doc_type='userzhifu', body=searchtian, size=1000, scroll="1m")
        scroll = Docs['_scroll_id']
        for doc in Docs['hits']['hits']:
            doc = doc['_source']
            if (len(doc['zhifudata']) == 1): jintianfufeiyonghushu += 1
            for zhifudata in doc['zhifudata']:
                if hisdatajintian == zhifudata['time_end'][:8]:
                    jintianfufeicishu += 1
                    jintianfufeizonge += int(int(zhifudata['total_fee']) * 0.01)
        while 1:
            try:
                Docs = es.scroll(scroll_id=scroll, scroll="1m")
                if (len(Docs['hits']['hits']) == 0):
                    break
                scroll = Docs['_scroll_id']
                for doc in Docs['hits']['hits']:
                    doc = doc['_source']
                    if (len(doc['zhifudata']) == 1): jintianfufeiyonghushu += 1
                    for zhifudata in doc['zhifudata']:
                        if hisdatajintian == zhifudata['time_end'][:8]:
                            jintianfufeicishu += 1
                            jintianfufeizonge += int(int(zhifudata['total_fee']) * 0.01)
            except:
                break
        newhisdata['zuotianyonghushu'] = jintianyonghushu
        newhisdata['zuotianfufeicishu'] = jintianfufeicishu
        newhisdata['zuotianfufeizonge'] = jintianfufeizonge
        if (jintian[:7] != hisdata['jintian'][:7]):
            newhisdata['dangyueyonghushu'] = 0
            newhisdata['dangyuefufeicishu'] = 0
            newhisdata['dangyuefufeizonge'] = 0
        else:
            newhisdata['dangyueyonghushu'] = hisdata['dangyueyonghushu'] + jintianyonghushu
            newhisdata['dangyuefufeicishu'] = hisdata['dangyuefufeicishu'] + jintianfufeicishu
            newhisdata['dangyuefufeizonge'] = hisdata['dangyuefufeizonge'] + jintianfufeizonge
        newhisdata['zongyonghushu'] = hisdata['zongyonghushu'] + jintianyonghushu
        newhisdata['zongfufeiyonghushu'] = hisdata['zongfufeiyonghushu'] + jintianfufeiyonghushu
        newhisdata['zongfufeicishu'] = hisdata['zongfufeicishu'] + jintianfufeicishu
        newhisdata['zongfufeie'] = hisdata['zongfufeie'] + jintianfufeizonge
        newhisdata['jintian'] = jintian
        f = open('shujuzhongxin.json', 'w')
        f.write(json.dumps(newhisdata) + '\n')
        f.close()
        hisdata = newhisdata.copy()
    searchtian = {"query": {"match_phrase_prefix": {"addtime": jintian}}}
    Docs = es.search(index='userinfo', doc_type='userinfo', body=searchtian, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    jintianyonghushu = len(Docs['hits']['hits'])
    jintianfufeiyonghushu = 0
    jintianfufeicishu = 0
    jintianfufeizonge = 0
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            jintianyonghushu += len(Docs['hits']['hits'])
        except:
            break
    searchtian = {"query": {"match_phrase_prefix": {"updatatime": nowtime}}}
    Docs = es.search(index='userzhifu', doc_type='userzhifu', body=searchtian, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    for doc in Docs['hits']['hits']:
        doc = doc['_source']
        if (len(doc['zhifudata']) == 1): jintianfufeiyonghushu += 1
        for zhifudata in doc['zhifudata']:
            if nowtime == zhifudata['time_end'][:8]:
                jintianfufeicishu += 1
                jintianfufeizonge += int(int(zhifudata['total_fee']) * 0.01)
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            for doc in Docs['hits']['hits']:
                doc = doc['_source']
                if (len(doc['zhifudata']) == 1): jintianfufeiyonghushu += 1
                for zhifudata in doc['zhifudata']:
                    if nowtime == zhifudata['time_end'][:8]:
                        jintianfufeicishu += 1
                        jintianfufeizonge += int(int(zhifudata['total_fee']) * 0.01)
        except:
            break
    newhisdata = hisdata.copy()
    newhisdata['zongyonghushu'] = hisdata['zongyonghushu'] + jintianyonghushu
    newhisdata['zongfufeiyonghushu'] = hisdata['zongfufeiyonghushu'] + jintianfufeiyonghushu
    newhisdata['zongfufeicishu'] = hisdata['zongfufeicishu'] + jintianfufeicishu
    newhisdata['zongfufeie'] = hisdata['zongfufeie'] + jintianfufeizonge
    newhisdata['jintianyonghushu'] = jintianyonghushu
    newhisdata['jintianfufeicishu'] = jintianfufeicishu
    newhisdata['jintianfufeizonge'] = jintianfufeizonge
    newhisdata['dangyueyonghushu'] = hisdata['dangyueyonghushu'] + jintianyonghushu
    newhisdata['dangyuefufeicishu'] = hisdata['dangyuefufeicishu'] + jintianfufeicishu
    newhisdata['dangyuefufeizonge'] = hisdata['dangyuefufeizonge'] + jintianfufeizonge
    body = {"query": {"bool": {"filter": [{"term": {"vipdengji": 1}}, ]}}}
    Docs = es.search(index='userinfo', doc_type='userinfo', body=body, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    newhisdata['xianyuehuiyuan'] = len(Docs['hits']['hits'])
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            newhisdata['xianyuehuiyuan'] += len(Docs['hits']['hits'])
        except:
            break
    body = {"query": {"bool": {"filter": [{"term": {"vipdengji": 2}}, ]}}}
    Docs = es.search(index='userinfo', doc_type='userinfo', body=body, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    newhisdata['xiannianhuiyuan'] = len(Docs['hits']['hits'])
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            newhisdata['xiannianhuiyuan'] += len(Docs['hits']['hits'])
        except:
            break
    body = {"query": {"bool": {"filter": [{"term": {"vipdengji": 3}}, ]}}}
    Docs = es.search(index='userinfo', doc_type='userinfo', body=body, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    newhisdata['xiansijiaoyigeyue'] = len(Docs['hits']['hits'])
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            newhisdata['xiansijiaoyigeyue'] += len(Docs['hits']['hits'])
        except:
            break
    body = {"query": {"bool": {"filter": [{"term": {"vipdengji": 4}}, ]}}}
    Docs = es.search(index='userinfo', doc_type='userinfo', body=body, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    newhisdata['xiansijiaosangeyue'] = len(Docs['hits']['hits'])
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            newhisdata['xiansijiaosangeyue'] += len(Docs['hits']['hits'])
        except:
            break
    body = {"query": {"bool": {"filter": [{"term": {"vipdengji": 5}}, ]}}}
    Docs = es.search(index='userinfo', doc_type='userinfo', body=body, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    newhisdata['xiansijiaoyinian'] = len(Docs['hits']['hits'])
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            newhisdata['xiansijiaoyinian'] += len(Docs['hits']['hits'])
        except:
            break
    body = {"query": {"bool": {"filter": [{"term": {"vipdengji": 6}}, ]}}}
    Docs = es.search(index='userinfo', doc_type='userinfo', body=body, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    newhisdata['xianlianmenghuiyuan'] = len(Docs['hits']['hits'])
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            newhisdata['xianlianmenghuiyuan'] += len(Docs['hits']['hits'])
        except:
            break

    return encrypt(json.dumps({'MSG': 'OK', 'data': newhisdata}))


@app.route("/test/getXiangqing", methods=["POST"])
def getXiangqing():
    try:
        params = json.loads(decrypt(request.stream.read()))
        yidingchenggong = params['yidingchenggong']
    except Exception as e:
        print(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    nowtime = time.strftime("%Y-%m-%d", time.localtime())
    body = {"query": {"match_phrase_prefix": {"time": nowtime}}}
    retdata = {'all': {'renshu': {}, 'cishu': 0, 'name': '总计', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'searchLiaomeihuashu': {'renshu': {}, 'cishu': 0, 'name': '话术搜索', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'searchBiaoqing': {'renshu': {}, 'cishu': 0, 'name': '表情搜索', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'searchBaike': {'renshu': {}, 'cishu': 0, 'name': '百科搜索', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'getLiaomeitaoluList': {'renshu': {}, 'cishu': 0, 'name': '撩妹套路', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'getXingxiangjianshe': {'renshu': {}, 'cishu': 0, 'name': '形象建设', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'getLiaomeishizhan': {'renshu': {}, 'cishu': 0, 'name': '撩妹实战', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'getKecheng': {'renshu': {}, 'cishu': 0, 'name': '课程阅读', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'getTuweiqinghua': {'renshu': {}, 'cishu': 0, 'name': '土味情话', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'getBaike': {'renshu': {}, 'cishu': 0, 'name': '百科阅读', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'getWenda': {'renshu': {}, 'cishu': 0, 'name': '问答阅读', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'getCeshidaan': {'renshu': {}, 'cishu': 0, 'name': '心理测试', 'renshuzhanbi': 0, 'cishuzhanbi': 0},
               'setDianzanshoucang': {'renshu': {}, 'cishu': 0, 'name': '点赞收藏', 'renshuzhanbi': 0, 'cishuzhanbi': 0}, }
    wenti = []
    Docs = es.search(index='userhis', doc_type='userhis', body=body, size=1000, scroll="1m")
    scroll = Docs['_scroll_id']
    allDocs = []
    allDocs += Docs['hits']['hits']
    while 1:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="1m")
            if (len(Docs['hits']['hits']) == 0):
                break
            scroll = Docs['_scroll_id']
            allDocs += Docs['hits']['hits']
        except:
            break
    for line in allDocs:
        line = line['_source']
        if line['event'] in histype:
            try:
                if line['event'] == 'setJilu':
                    if line['jilutype'] == 'huashu':
                        wenti.insert(0, {'wenti': line['detail'], 'daan': line['jilucontent']})
                else:
                    retdata['all']['renshu'][line['unionid']] = 0
                    retdata['all']['cishu'] += 1
                    retdata[line['event']]['renshu'][line['unionid']] = 0
                    retdata[line['event']]['cishu'] += 1
            except:
                None
    for line in retdata:
        retdata[line]['renshu'] = len(retdata[line]['renshu'])
    renshu = max(retdata['all']['renshu'], 1)
    cishu = max(retdata['all']['cishu'], 1)
    for line in retdata:
        retdata[line]['renshuzhanbi'] = int(retdata[line]['renshu'] / renshu * 1000) / 1000
        retdata[line]['cishuzhanbi'] = int(retdata[line]['cishu'] / cishu * 1000) / 1000
    newdata = []
    for line in retdata:
        newdata.append(retdata[line])
    newdata = sorted(newdata, key=lambda x: x['cishu'], reverse=True)
    return encrypt(json.dumps({'MSG': 'OK', 'data': newdata, 'wenti': wenti}))



@app.route("/test/getZhifulist", methods=["POST"])
def getZhifulist():
    try:
        params = json.loads(decrypt(request.stream.read()))
        yidingchenggong = params['yidingchenggong']
    except Exception as e:
        print(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
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
    retlist = []
    for unionid in userlist:
        doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
        purePhoneNumber = ''
        if 'purePhoneNumber' in doc:
            purePhoneNumber = doc['purePhoneNumber']
        nickName = ''
        if 'nickName' in doc:
            nickName = doc['nickName']
        elif 'nickname' in doc:
            nickName = doc['nickname']
        yingyongid = ''
        if 'yingyongid' in doc:
            yingyongid = doc['yingyongid']
        retlist.append([nickName,
                        doc['addtime'], str(doc['xiaofeicishu']), str(doc['xiaofeizonge']), doc['province'], doc[
                            'city'], unionidlist[unionid][:4] + '-' + unionidlist[unionid][4:6] + '-' + unionidlist[
                                                                                                            unionid][
                                                                                                        6:8] + ' ' +
                        unionidlist[unionid][8:10] + ':' + unionidlist[unionid][10:12] + ':' + unionidlist[unionid][
                                                                                               12:14], purePhoneNumber,
                        yingyongid])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retlist}))


if __name__ == "__main__":
    # server = pywsgi.WSGIServer(('127.0.0.1', 16888), app)
    # server.serve_forever()
    http_serve = WSGIServer(("127.0.0.1", 16888), app, handler_class=WebSocketHandler)
    http_serve.serve_forever()
