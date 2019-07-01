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
from weixin_app import handel
from weixin_app import receive
from weixin_app import reply
from msg_crypto.WXBizMsgCrypt import WXBizMsgCrypt

app = Flask(__name__)
CORS(app, supports_credentials=True)
wangzhi = 'https://www.lianaizhuli.com/'
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log/log.txt")
handler.setLevel(logging.INFO)
es = Elasticsearch([{"host": "182.254.227.188", "port": 9218}])
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * bytes(chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), encoding='utf8')
unpad = lambda s: s[0:-ord(s[-1])]
dingyuehaoappid = 'wxc1deae6a065dffa9'
dingyuehaoencodingAESKey = "UmBlx5gtFv7zravWwE9tCLjC99qPxRZQDPDdfeFCBfg"
token = 'lianailianmeng'
os.chdir('/home/ubuntu/data/lianailianmeng/data')
HD = handel.Handel()
# appid = 'wxa9ef833cef143ce1'  # 小程序
ceshiappid = 'wxbcf971f5b21cad9a'
fuwuhaoappid = 'wx2cc1bc5a412d44d2'
fuwuhaoAppSecret = '3290467fd91f3e4ae427fca28d0137c9'
dingyuhaoAppsecret = 'eed5a19fc19cbddc54e1abf363ab0eb5'
xiaochengxuAppsecret = '574ba86bc66b664ab42e4d60276afb7c'
mch_id = '1519367291'
merchant_key = 'shenzhenyuzikejiyouxiangongsi888'
key = "pangyuming920318"
iv = "abcdefabcdefabcd"


def dict_to_xml(dict_data):
    '''
    dict to xml
    :param dict_data:
    :return:
    '''
    xml = ["<xml>"]
    for k, v in dict_data.items():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)


def xml_to_dict(xml_data):
    '''
    xml to dict
    :param xml_data:
    :return:
    '''
    xml_dict = {}
    root = ET.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict


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
    return json.loads(decrypted[:-ord(decrypted[len(decrypted) - 1:])].decode('utf8'))


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
                encrypt_decrypt = WXBizMsgCrypt(token, encodingAESKey, appid)
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
                encrypt_decrypt = WXBizMsgCrypt(token, encodingAESKey, appid)
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


@app.route("/v1/shouquanhuitiao", methods=["GET", "POST"])
def shouquanhuitiao():
    print(request.args)
    return "OK"


@app.route("/v1/ceshi", methods=["GET", "POST"])
def ceshi():
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
    return None


@app.route("/v1/getKechengList", methods=["POST"])
def getKechengList():
    # try:
    #     params = json.loads(decrypt(request.stream.read()))
    #     openid = params['openid']
    # except Exception as e:
    #     logger.error(e)
    #     return json.dumps({'MSG': '警告！非法入侵！！！'})
    # adduserhis(
    #     {'openid': openid, 'time': getTime(), 'event': 'getKechengList', 'detail': 'getKechengList',
    #      'type': '0'})
    retdata = []
    search = {"query": {"match_all": {}}}
    Docs = es.search(index='kechenglist', doc_type='kechenglist', body=search, size=10000)
    Docs = Docs['hits']['hits']
    try:
        goumaidoc = es.get(index='kechenggoumai', doc_type='kechenggoumai', id=openid)['_source']
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
        # openid = params['openid']
        neirongid = params['neirongid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    # adduserhis({'openid': openid, 'time': getTime(), 'event': 'getKecheng', 'detail': neirongid,
    #             'type': '0'})
    doc = es.get(index='kecheng', doc_type='kecheng', id=neirongid)['_source']
    return encrypt(json.dumps({'MSG': 'OK', 'data': doc}))


@app.route("/v1/getOpenid", methods=["POST"])
def getOpenid():
    try:
        params = json.loads(decrypt(request.stream.read()))
        code = params['code']
        # userInfo = params['userInfo']
        # system = params['system']
        # options = params['options']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    url ='https://api.weixin.qq.com/sns/oauth2/access_token?appid='+fuwuhaoappid+'&secret='+fuwuhaoAppSecret+'&code='+code+'&grant_type=authorization_code'
    response = requests.get(url)
    response = response.json()
    print(response)
    # userInfo['openid'] = response['openid']
    # userInfo['system'] = system
    # try:
    #     doc = es.get(index='userinfo', doc_type='userinfo', id=response['openid'])
    #     newdoc = doc['_source']
    #     newdoc.update(userInfo)
    #     es.index(index='userinfo', doc_type='userinfo', id=userInfo['openid'], body=newdoc)
    #     try:
    #         escopy.index(index='userinfo', doc_type='userinfo', id=userInfo['openid'], body=newdoc, timeout="1s")
    #     except Exception as e:
    #         logger.error(e)
    # except Exception as e:
    #     logger.error(e)
    #     userInfo['addtime'] = time.strftime("%Y%m%d", time.localtime())
    #     userInfo['vipdengji'] = 0
    #     userInfo['viptime'] = int(time.time()) + viptime[0]
    #     userInfo['sijiaotime'] = 0
    #     userInfo['xiaofeicishu'] = 0
    #     userInfo['xiaofeizonge'] = 0
    #     userInfo['options'] = json.loads(options)
    #     es.index(index='userinfo', doc_type='userinfo', id=userInfo['openid'], body=userInfo)
    #     try:
    #         escopy.index(index='userinfo', doc_type='userinfo', id=userInfo['openid'], body=userInfo, timeout="1s")
    #     except Exception as e:
    #         logger.error(e)
    # # print(decryptweixin(params['encryptedData'], response['session_key'], params['iv'])['unionId'])
    # adduserhis(
    #     {'openid': response['openid'], 'time': getTime(), 'event': 'getOpenid', 'detail': 'getOpenid', 'type': '0'})
    return encrypt(json.dumps({'MSG': 'OK', 'data': {'openid': response['openid']}}))

@app.route("/v1/get_prepay_id", methods=["POST"])
def get_prepay_id():
    try:
        params = json.loads(decrypt(request.stream.read()))
        openid = params['openid']
        zhifutype = params['zhifutype']
        detail = params['detail']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    # kechengjiage = int(es.get(index='kechenglist', doc_type='kechenglist', id=kechengid)['_source']['jiage'] * 100)
    kechengjiage=1
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    prepaydata = {
        'appid': fuwuhaoappid,
        'mch_id': mch_id,
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
        'body': detail,
        'attach': json.dumps({'zhifutype': zhifutype, 'detail': detail}, ensure_ascii=False),
        'out_trade_no': str(int(time.time())) + '_' + str((random.randint(1000000, 9999999))),
        'total_fee': kechengjiage,
        'spbill_create_ip': request.remote_addr,
        'notify_url': wangzhi + "v1/paynotify",
        'trade_type': "JSAPI",
        'openid': openid,
    }
    stringA = '&'.join(["{0}={1}".format(k, prepaydata.get(k)) for k in sorted(prepaydata)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    prepaydata['sign'] = sign
    req = urllib.request.Request(url, dict_to_xml(prepaydata).encode('utf8'),
                                 headers={'Content-Type': 'application/xml'})
    result = urllib.request.urlopen(req, timeout=10).read().decode('utf8')
    result = xml_to_dict(result)
    prepay_id = result['prepay_id']
    paySign_data = {
        'appId': fuwuhaoappid,
        'timeStamp': str(int(time.time())),
        'nonceStr': result['nonce_str'],
        'package': 'prepay_id={0}'.format(prepay_id),
        'signType': 'MD5'
    }
    stringA = '&'.join(["{0}={1}".format(k, paySign_data.get(k)) for k in sorted(paySign_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    paySign_data['paySign'] = paySign
    # paySign_data.pop('appId')
    # doc = es.get(index='userinfo', doc_type='userinfo', id=openid)
    # doc = doc['_source']
    # if 'phoneNumber' not in doc:
    #     return encrypt(json.dumps({'MSG': 'nophoneNumber', 'data': paySign_data}))
    print(paySign_data)
    return encrypt(json.dumps({'MSG': 'OK', 'data': paySign_data}))

@app.route("/v1/paynotify", methods=["POST"])
def paynotify():
    zhifures = xml_to_dict(request.stream.read().decode('utf8'))
    sign = zhifures['sign']
    zhifures.pop('sign')
    stringA = '&'.join(["{0}={1}".format(k, zhifures.get(k)) for k in sorted(zhifures)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest().upper()
    if sign != paySign:
        return dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'})
    print(zhifures)
    # zhifudata = [zhifures]
    # isnew = 1
    # flag = 1
    # try:
    #     doc = es.get(index='userzhifu', doc_type='userzhifu', id=zhifures['openid'])
    #     isnew = 0
    #     for line in doc['_source']['zhifudata']:
    #         if line['transaction_id'] == zhifudata[0]['transaction_id']:
    #             flag = 0
    #     if flag:
    #         zhifudata += doc['_source']['zhifudata']
    # except Exception as e:
    #     logger.error(e)
    # if isnew or (isnew == 0 and flag == 1):
    #     es.index(index='userzhifu', doc_type='userzhifu', id=zhifures['openid'],
    #              body={'openid': zhifures['openid'], 'zhifudata': zhifudata, 'updatatime': zhifures['time_end']})
    #     try:
    #         escopy.index(index='userzhifu', doc_type='userzhifu', id=zhifures['openid'],
    #                      body={'openid': zhifures['openid'], 'zhifudata': zhifudata,
    #                            'updatatime': zhifures['time_end']}, timeout="1s")
    #     except Exception as e:
    #         logger.error(e)
    #     try:
    #         kechengid = json.loads(zhifures['attach'])['kechengid']
    #         try:
    #             goumaidoc = es.get(index='kechenggoumai', doc_type='kechenggoumai', id=zhifures['openid'])['_source']
    #             goumaidoc['data'] = json.loads(goumaidoc['data'])
    #             goumaidoc['data'][kechengid] = 1
    #         except:
    #             goumaidoc = {}
    #             goumaidoc['openid'] = zhifures['openid']
    #             goumaidoc['data'] = {}
    #             goumaidoc['data'][kechengid] = 1
    #         goumaidoc['data'] = json.dumps(goumaidoc['data'])
    #         es.index(index='kechenggoumai', doc_type='kechenggoumai', id=zhifures['openid'], body=goumaidoc)
    #         try:
    #             escopy.index(index='kechenggoumai', doc_type='kechenggoumai', id=zhifures['openid'], body=goumaidoc,
    #                          timeout="1s")
    #         except Exception as e:
    #             logger.error(e)
    #         doc = es.get(index='userinfo', doc_type='userinfo', id=zhifures['openid'])
    #         newdoc = doc['_source']
    #         newdoc['xiaofeicishu'] += 1
    #         newdoc['xiaofeizonge'] += int(zhifures['total_fee'])
    #         es.index(index='userinfo', doc_type='userinfo', id=zhifures['openid'], body=newdoc)
    #         try:
    #             escopy.index(index='userinfo', doc_type='userinfo', id=zhifures['openid'], body=newdoc, timeout="1s")
    #         except Exception as e:
    #             logger.error(e)
    #     except Exception as e:
    #         logger.error(e)
    return dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'})



@app.route("/v1/get_kechengprepay_id", methods=["POST"])
def get_kechengprepay_id():
    try:
        params = json.loads(decrypt(request.stream.read()))
        openid = params['openid']
        kechengid = params['kechengid']
        detail = params['detail']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    # kechengjiage = int(es.get(index='kechenglist', doc_type='kechenglist', id=kechengid)['_source']['jiage'] * 100)
    kechengjiage=1
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    prepaydata = {
        'appid': fuwuhaoappid,
        'mch_id': mch_id,
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
        'body': detail,
        'attach': json.dumps({'kechengid': kechengid, 'detail': detail}, ensure_ascii=False),
        'out_trade_no': str(int(time.time())) + '_' + str((random.randint(1000000, 9999999))),
        'total_fee': kechengjiage,
        'spbill_create_ip': request.remote_addr,
        'notify_url': wangzhi + "v1/kechengpaynotify",
        'trade_type': "JSAPI",
        'openid': openid,
    }
    stringA = '&'.join(["{0}={1}".format(k, prepaydata.get(k)) for k in sorted(prepaydata)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    prepaydata['sign'] = sign
    req = urllib.request.Request(url, dict_to_xml(prepaydata).encode('utf8'),
                                 headers={'Content-Type': 'application/xml'})
    result = urllib.request.urlopen(req, timeout=10).read().decode('utf8')
    result = xml_to_dict(result)
    prepay_id = result['prepay_id']
    paySign_data = {
        'appId': fuwuhaoappid,
        'timeStamp': str(int(time.time())),
        'nonceStr': result['nonce_str'],
        'package': 'prepay_id={0}'.format(prepay_id),
        'signType': 'MD5'
    }
    stringA = '&'.join(["{0}={1}".format(k, paySign_data.get(k)) for k in sorted(paySign_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    paySign_data['paySign'] = paySign
    # paySign_data.pop('appId')
    # doc = es.get(index='userinfo', doc_type='userinfo', id=openid)
    # doc = doc['_source']
    # if 'phoneNumber' not in doc:
    #     return encrypt(json.dumps({'MSG': 'nophoneNumber', 'data': paySign_data}))
    return encrypt(json.dumps({'MSG': 'OK', 'data': paySign_data}))


@app.route("/v1/kechengpaynotify", methods=["POST"])
def kechengpaynotify():
    zhifures = xml_to_dict(request.stream.read().decode('utf8'))
    sign = zhifures['sign']
    zhifures.pop('sign')
    stringA = '&'.join(["{0}={1}".format(k, zhifures.get(k)) for k in sorted(zhifures)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest().upper()
    if sign != paySign:
        return dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'})
    print(zhifures)
    # zhifudata = [zhifures]
    # isnew = 1
    # flag = 1
    # try:
    #     doc = es.get(index='userzhifu', doc_type='userzhifu', id=zhifures['openid'])
    #     isnew = 0
    #     for line in doc['_source']['zhifudata']:
    #         if line['transaction_id'] == zhifudata[0]['transaction_id']:
    #             flag = 0
    #     if flag:
    #         zhifudata += doc['_source']['zhifudata']
    # except Exception as e:
    #     logger.error(e)
    # if isnew or (isnew == 0 and flag == 1):
    #     es.index(index='userzhifu', doc_type='userzhifu', id=zhifures['openid'],
    #              body={'openid': zhifures['openid'], 'zhifudata': zhifudata, 'updatatime': zhifures['time_end']})
    #     try:
    #         escopy.index(index='userzhifu', doc_type='userzhifu', id=zhifures['openid'],
    #                      body={'openid': zhifures['openid'], 'zhifudata': zhifudata,
    #                            'updatatime': zhifures['time_end']}, timeout="1s")
    #     except Exception as e:
    #         logger.error(e)
    #     try:
    #         kechengid = json.loads(zhifures['attach'])['kechengid']
    #         try:
    #             goumaidoc = es.get(index='kechenggoumai', doc_type='kechenggoumai', id=zhifures['openid'])['_source']
    #             goumaidoc['data'] = json.loads(goumaidoc['data'])
    #             goumaidoc['data'][kechengid] = 1
    #         except:
    #             goumaidoc = {}
    #             goumaidoc['openid'] = zhifures['openid']
    #             goumaidoc['data'] = {}
    #             goumaidoc['data'][kechengid] = 1
    #         goumaidoc['data'] = json.dumps(goumaidoc['data'])
    #         es.index(index='kechenggoumai', doc_type='kechenggoumai', id=zhifures['openid'], body=goumaidoc)
    #         try:
    #             escopy.index(index='kechenggoumai', doc_type='kechenggoumai', id=zhifures['openid'], body=goumaidoc,
    #                          timeout="1s")
    #         except Exception as e:
    #             logger.error(e)
    #         doc = es.get(index='userinfo', doc_type='userinfo', id=zhifures['openid'])
    #         newdoc = doc['_source']
    #         newdoc['xiaofeicishu'] += 1
    #         newdoc['xiaofeizonge'] += int(zhifures['total_fee'])
    #         es.index(index='userinfo', doc_type='userinfo', id=zhifures['openid'], body=newdoc)
    #         try:
    #             escopy.index(index='userinfo', doc_type='userinfo', id=zhifures['openid'], body=newdoc, timeout="1s")
    #         except Exception as e:
    #             logger.error(e)
    #     except Exception as e:
    #         logger.error(e)
    return dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'})


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 13888), app)
    server.serve_forever()
