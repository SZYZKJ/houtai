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
from PIL import Image, ImageDraw, ImageFont
from basic import Basic
from io import BytesIO
import pymongo

datapath = '/home/ubuntu/data/lianaihuashu/data'
wangzhi = 'https://www.lianaizhuli.com'
os.chdir(datapath)
app = Flask(__name__)
app.debug = True
CORS(app, supports_credentials=True)
es = Elasticsearch([{"host": "182.254.227.188", "port": 9218}])
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["zhangfen"]
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log/zhangfen.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
key = "zhangfenzhangfen"
iv = "abcdabcdabcdabcd"
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * bytes(chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), encoding='utf8')
unpad = lambda s: s[0:-ord(s[-1])]
appids = {'wx6e2807f3bb07c07e': {'secret': 'b29938d98625ae82e4125f3cd4bf0a95', 'weixinhao': 'Love---Union',
                                 'weixinshenhe': 0, 'mch_id': '1519367291',
                                 'merchant_key': 'shenzhenyuzikejiyouxiangongsi888'},
          'wx80aa847a59c8e287': {'secret': '35fbe6b7eb3883a65ac2f9e2cd568bfc', 'weixinhao': 'QQ756782789',
                                 'weixinshenhe': 0, 'mch_id': '1519367291',
                                 'merchant_key': 'shenzhenyuzikejiyouxiangongsi888'},
          'wxc24f6a48620a38d5': {'secret': 'f76856de670c076656b7c867829c091f', 'weixinhao': 'Love---Union',
                                 'weixinshenhe': 0, 'mch_id': '1519367291',
                                 'merchant_key': 'shenzhenyuzikejiyouxiangongsi888'},
          'wx311bf0a55020cb9e': {'secret': '24231fcd562d3acc5ee2b546132c6fe9', 'weixinhao': '18756168518',
                                 'weixinshenhe': 0, 'mch_id': '1596830831',
                                 'merchant_key': 'Aa888888888888888888888888888888'},
          'wx2cc1bc5a412d44d2': {'secret': '3290467fd91f3e4ae427fca28d0137c9', 'weixinhao': 'Love---Union',
                                 'weixinshenhe': 0, 'mch_id': '1519367291',
                                 'merchant_key': 'shenzhenyuzikejiyouxiangongsi888'}}
fuwuhaoappid = 'wx2cc1bc5a412d44d2'
fuwuhaoAppSecret = '3290467fd91f3e4ae427fca28d0137c9'
vipdengji = [0, 1, 2, 3, 4]
viptime = [600, 604800, 2592000, 7776000, 31536000]
vipdengjimiaoshu = ['非会员', '周会员', '月会员', '季会员', '年会员']
total_fees = [0, 6900, 9900, 14900, 19900]
meirigeshu = 100
tuweiqinghua = []
for line in open('tuweiqinghua.json'):
    line = json.loads(line)
    tuweiqinghua.append(line['id'])
weixinpingguoshenhe = 1
liaomeishenhe = 0
if weixinpingguoshenhe == 1:
    ioswenan = '由于相关规范，小程序下IOS虚拟商品支付暂不可用。'
else:
    ioswenan = '由于相关规范，小程序下IOS虚拟商品支付暂不可用。IOS用户请到个人页咨询在线客服。'
apiqianzui = '/zhangfen/'


def adduserhis(userhis):
    mydb['userhis'].update_one({}, {'$set': userhis}, True)
    return None


@app.route(apiqianzui + "getIslianmeng", methods=["POST"])
def getIslianmeng():
    try:
        params = json.loads(decrypt(request.stream.read()))
        system = params['system']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    if system[:3].lower() == 'ios':
        return encrypt(json.dumps(
            {'MSG': 'OK', 'weixinshenhe': appids[params['nametype']]['weixinshenhe'],
             'weixinpingguoshenhe': weixinpingguoshenhe, 'liaomeishenhe': liaomeishenhe}))
    else:
        return encrypt(json.dumps(
            {'MSG': 'OK', 'weixinshenhe': appids[params['nametype']]['weixinshenhe'], 'weixinpingguoshenhe': 0,
             'liaomeishenhe': liaomeishenhe}))


@app.route(apiqianzui + "getShouyekuai", methods=["POST"])
def getShouyekuai():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    return encrypt(json.dumps({'MSG': 'OK', 'lunbotu': [
        {'title': '和友商对比', 'adurl': wangzhi + '/shouye/lunbotu/WechatIMG43.jpeg',
         'type': 'html', 'url': 'https://mp.weixin.qq.com/s/xR2iH6bHkY9OUvRVYHWv9w'},
    ],
                               'tubiao': [{'title': '土味情话', 'image': wangzhi + '/shouye/tubiao/tuweiqinghua.png',
                                           'page': 'tuweiqinghualist'},
                                          {'title': '幽默话题', 'image': wangzhi + '/shouye/tubiao/liaomeitaolu.png',
                                           'page': 'liaomeitaolulist'},
                                          {'title': '情感百科', 'image': wangzhi + '/shouye/tubiao/qingganbaike.png',
                                           'page': 'qingganbaike'},
                                          {'title': '心理测试', 'image': wangzhi + '/shouye/tubiao/xinliceshi.png',
                                           'page': 'xinliceshilist'}, ],
                               'searchicon': wangzhi + '/shouye/search.png',
                               'miaoshu': '①女生回了一句话 ②你恐惧回复不好 ③复制粘贴在这里试试？',
                               'tuijian': ['我有男朋友了', '你真自恋', '我睡觉了', '表白', '哈哈'],
                               }))


@app.route(apiqianzui + "getShouyeman", methods=["POST"])
def getShouyeman():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    kecheng = {'image': wangzhi + '/shouye/wenzi/kecheng.png', 'data': []}
    xingxiangjianshe = {'image': wangzhi + '/shouye/wenzi/xingxiangjianshe.png', 'data': []}
    qingganbaike = {'image': wangzhi + '/shouye/wenzi/qingganbaike.png', 'data': []}
    liaomeishizhan = {'image': wangzhi + '/shouye/wenzi/liaotianshizhan.png', 'data': []}
    xinliceshi = {'image': wangzhi + '/shouye/wenzi/xinliceshi.png', 'data': []}
    search = {"query": {"match_all": {}}}
    Docs = es.search(index='kechenglist', doc_type='kechenglist', body=search, size=3)['hits']['hits']
    try:
        goumaidoc = mydb['kechenggoumai'].find_one({'_id': unionid + params['nametype']})
        goumaidoc['data'] = json.loads(goumaidoc['data'])
    except:
        goumaidoc = {}
        goumaidoc['data'] = {}
    for u, doc in enumerate(Docs):
        doc = doc['_source']
        doc['newimage'] = wangzhi + '/shouye/images/kecheng' + str(u + 1) + '.png'
        if doc['id'] in goumaidoc['data']:
            doc['yigoumai'] = 1
        else:
            doc['yigoumai'] = 0
        kecheng['data'].append(doc)
    Docs = es.search(index='xingxiangjianshe', doc_type='xingxiangjianshe', body=search, size=4)['hits']['hits']
    for u, doc in enumerate(Docs):
        doc = doc['_source']
        doc['newimage'] = wangzhi + '/shouye/images/xingxiangjianshe' + str(u + 1) + '.png'
        xingxiangjianshe['data'].append(doc)
    Docs = es.search(index='baikelist', doc_type='baikelist', body=search, size=3)['hits']['hits']
    for u, doc in enumerate(Docs):
        doc = doc['_source']
        doc['newimage'] = doc['image']
        qingganbaike['data'].append(doc)
    Docs = es.search(index='liaomeishizhanlist', doc_type='liaomeishizhanlist', body=search, size=4)['hits']['hits']
    for u, doc in enumerate(Docs):
        doc = doc['_source']
        doc['newimage'] = doc['image']
        liaomeishizhan['data'].append(doc)
    Docs = es.search(index='xinliceshilist', doc_type='xinliceshilist', body=search, size=4)['hits']['hits']
    for u, doc in enumerate(Docs):
        doc = doc['_source']
        doc['newimage'] = wangzhi + '/shouye/images/xinliceshi' + str(u + 1) + '.png'
        xinliceshi['data'].append(doc)
    return encrypt(json.dumps({'MSG': 'OK',
                               'gengduotext': '更多',
                               'gengduoicon': wangzhi + '/shouye/gengduo.png',
                               'kecheng': kecheng,
                               'xingxiangjianshe': xingxiangjianshe,
                               'qingganbaike': qingganbaike,
                               'liaomeishizhan': liaomeishizhan,
                               'xinliceshi': xinliceshi,
                               }))


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


def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def check_user(unionid):
    doc = mydb['userinfo'].find_one({'_id': unionid})
    if doc['tingyong'] == 1:
        return 0
    if doc['viptime'] > int(time.time()):
        return 1
    elif doc['vipdengji'] > 0:
        doc['vipdengji'] = 0
        mydb['userinfo'].update_one({'_id', unionid}, {'$set': doc}, True)
    return 0


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
    retdata = json.loads(decrypted[:-ord(decrypted[len(decrypted) - 1:])].decode('utf8'))
    return retdata


def addKeyword(params):
    unionid = params['unionid']
    inputValue = params['query']
    retdata = []
    try:
        doc = mydb['userkeywordhislist'].find_one({'_id': unionid})
        retdata = doc['data']
    except Exception as e:
        None
    if len(retdata) == 0 or inputValue != retdata[0]:
        flag = 1
        for index, value in enumerate(retdata):
            if inputValue == value:
                flag = 0
                retdata = [inputValue] + retdata[:index] + \
                          retdata[
                          index + 1:]
        if flag:
            retdata = [inputValue] + retdata
            retdata = retdata[:12]
    mydb['userkeywordhislist'].update_one({'_id': unionid}, {"$set": {'data': retdata}}, True)


@app.route(apiqianzui + "getUnionid", methods=["POST"])
def getUnionid():
    try:
        params = json.loads(decrypt(request.stream.read()))
        js_code = params['js_code']
        userinfo = params['userinfo']
        system = params['system']
        options = params['options']
        nametype = params['nametype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    secret = appids[params['nametype']]['secret']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + params[
        'nametype'] + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = requests.get(url)
    response = response.json()
    userinfo['system'] = system
    openid = ''
    if 'openid' in response:
        openid = response['openid']
    elif 'openId' in response:
        openid = response['openId']
    userinfo['openid'] = openid
    unionid = openid
    userinfo['unionid'] = unionid
    try:
        uniondoc = mydb['userinfo'].find_one({'_id': unionid + nametype})
        uniondoc.update(userinfo)
        userinfo = uniondoc
    except:
        None
    if 'addtime' not in userinfo:
        userinfo['addtime'] = getTime()
        userinfo['vipdengji'] = 0
        userinfo['viptime'] = int(time.time()) + viptime[0]
        userinfo['xiaofeicishu'] = 0
        userinfo['xiaofeizonge'] = 0
        userinfo['tingyong'] = 0
    if 'options' not in userinfo:
        userinfo['options'] = options
    userinfo['apptype'] = params['apptype']
    userinfo['nametype'] = params['nametype']
    mydb['userinfo'].update_one({'_id': unionid + nametype}, {'$set': userinfo}, True)
    adduserhis({'time': getTime(), 'event': 'getUnionid', 'detail': params})
    return encrypt(json.dumps({'MSG': 'OK', 'data': {'unionid': unionid}}))


def getopenid_and_access_token(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + fuwuhaoappid + '&secret=' + fuwuhaoAppSecret + '&code=' + code + '&grant_type=authorization_code'
    response = requests.get(url)
    response = response.json()
    return response


def openid_unionid(openid, access_token):
    unionidurl = 'https://api.weixin.qq.com/sns/userinfo?access_token=' + access_token + '&openid=' + openid + '&lang=zh_CN'
    response = requests.get(unionidurl)
    response = response.json()
    return response


@app.route(apiqianzui + "getFwhnionid", methods=["POST"])
def getFwhnionid():
    try:
        params = json.loads(decrypt(request.stream.read()))
        code = params['code']
        apptype = params['apptype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    response = getopenid_and_access_token(code)
    resdata = openid_unionid(response['openid'], response['access_token'])
    unionid = resdata['unionid']
    resdata['fwhid'] = resdata['openid']
    resdata.pop('openid')
    try:
        userinfodoc = mydb['userinfo'].find_one({'_id': unionid + fuwuhaoappid})
        userinfodoc.update(resdata)
        resdata = userinfodoc
    except:
        resdata['addtime'] = getTime()
        resdata['vipdengji'] = 0
        resdata['viptime'] = int(time.time()) + viptime[0]
        resdata['xiaofeicishu'] = 0
        resdata['xiaofeizonge'] = 0
        resdata['tingyong'] = 0
    resdata['apptype'] = apptype
    resdata['nametype'] = fuwuhaoappid
    mydb['userinfo'].update_one({'_id': unionid + fuwuhaoappid}, {'$set': resdata}, True)
    return encrypt(json.dumps({'MSG': 'OK', 'data': {'unionid': unionid}}))


@app.route(apiqianzui + "checkUnionid", methods=["POST"])
def checkUnionid():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        userinfo = params['userinfo']
        nametype = params['nametype']
        system = params['system']
    except Exception as e:
        logger.error(e)
        return encrypt(json.dumps({'MSG': 'NO'}))
    try:
        unionid_token = mydb['unionid_token']
        unionid_token.delete_one({'_id': unionid})
    except:
        None
    try:
        newdoc = mydb['userinfo'].find_one({'_id': unionid + nametype})
        newdoc.update(userinfo)
        newdoc['system'] = system
        mydb['userinfo'].update_one({'_id': unionid + nametype}, {'$set': newdoc}, True)
        if 'unionid' in newdoc and 'openid' in newdoc:
            return encrypt(json.dumps({'MSG': 'YES'}))
        else:
            return encrypt(json.dumps({'MSG': 'NO'}))
    except Exception as e:
        logger.error(e)
        return encrypt(json.dumps({'MSG': 'NO'}))


@app.route(apiqianzui + "searchLiaomeihuashu", methods=["POST"])
def searchLiaomeihuashu():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        query = params['query']
        scroll = params['scroll']
        nametype = params['nametype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    check_user_res = check_user(unionid + nametype)
    if check_user_res == 0:
        return encrypt(json.dumps({'MSG': 'LIMIT'}))
    addKeyword(params)
    adduserhis({'time': getTime(), 'event': 'searchLiaomeihuashu', 'detail': params})
    retdata = []
    search = {'query': {'match': {'chat_name': query}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='liaomeihuashu', doc_type='liaomeihuashu', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='liaomeihuashu', doc_type='liaomeihuashu', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "searchBiaoqing", methods=["POST"])
def searchBiaoqing():
    try:
        params = json.loads(decrypt(request.stream.read()))
        query = params['query']
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    addKeyword(params)
    adduserhis({'time': getTime(), 'event': 'searchBiaoqing', 'detail': params})
    retdata = []
    search = {'query': {'match': {'imgExplain': query}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='biaoqing', doc_type='biaoqing', body=search, size=15, scroll="5m")

    else:
        Docs = es.search(index='biaoqing', doc_type='biaoqing', body=search, size=15, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source']['url'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "searchBaike", methods=["POST"])
def searchBaike():
    try:
        params = json.loads(decrypt(request.stream.read()))
        query = params['query']
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    addKeyword(params)
    adduserhis({'time': getTime(), 'event': 'searchBaike', 'detail': params})
    retdata = []
    search = {'query': {'match': {'title': query}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='search', doc_type='search', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='search', doc_type='search', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getLiaomeitaoluList", methods=["POST"])
def getLiaomeitaoluList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        cid = params['cid']
        scroll = params['scroll']
        nametype = params['nametype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    check_user_res = check_user(unionid + nametype)
    if check_user_res == 0 and scroll != '':
        return encrypt(json.dumps({'MSG': 'LIMIT'}))
    adduserhis({'time': getTime(), 'event': 'getLiaomeitaoluList', 'detail': params})
    retdata = []
    search = {'query': {'bool': {'filter': {"term": {'cid': cid}}}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='liaomeitaolu', doc_type='liaomeitaolu', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='liaomeitaolu', doc_type='liaomeitaolu', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getHiswordList", methods=["POST"])
def getHiswordList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    try:
        doc = mydb['userkeywordhislist'].find_one({'_id': unionid})
        retdata = doc['data']
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata}))


@app.route(apiqianzui + "clearHiswords", methods=["POST"])
def clearHiswords():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    mydb['userkeywordhislist'].update_one({'_id': unionid}, {"$set": {'data': []}}, True)
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "getRecommend", methods=["POST"])
def getRecommend():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    hotWords = ['自恋', '厉害', '睡觉', '生气', '干嘛', '烦', '哈哈', '好吧', '介绍', '丑', '表白', '呵呵', '开场白', '赞美', '拉升关系', '高价值展示',
                '幽默搞笑', '冷读', '推拉', '角色扮演', '框架', '打压', '进挪', '背景植入']
    return encrypt(json.dumps({'MSG': 'OK', 'data': {'hotWordsList': hotWords}}))


@app.route(apiqianzui + "getHelpkeywords", methods=["POST"])
def getHelpkeywords():
    try:
        params = json.loads(decrypt(request.stream.read()))
        query = params['query']
        nowtab = params['nowtab'],
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    nowtab = int(nowtab[0])
    if nowtab == 0:
        search = {'query': {'match': {'chat_name': query}}}
        Docs = es.search(index='liaomeihuashu', doc_type='liaomeihuashu', body=search, size=20, scroll="5m")
        Docs = Docs['hits']['hits']
        for doc in Docs:
            retdata.append(doc['_source']['chat_name'].strip())
    elif nowtab == 1:
        search = {'query': {'match': {'imgExplain': query}}}
        Docs = es.search(index='biaoqing', doc_type='biaoqing', body=search, size=20, scroll="5m")
        Docs = Docs['hits']['hits']
        for doc in Docs:
            retdata.append(doc['_source']['imgExplain'])
    else:
        search = {'query': {'match': {'title': query}}}
        Docs = es.search(index='search', doc_type='search', body=search, size=20, scroll="5m")
        Docs = Docs['hits']['hits']
        for doc in Docs:
            retdata.append(doc['_source']['title'])
    nowi = 0
    for i in range(1, len(retdata)):
        if retdata[nowi] != retdata[i]:
            nowi += 1
            retdata[nowi] = retdata[i]
    retdata = retdata[:10]
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata}))


@app.route(apiqianzui + "getXingxiangjiansheList", methods=["POST"])
def getXingxiangjiansheList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    search = {"query": {"match_all": {}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='xingxiangjianshe', doc_type='xingxiangjianshe', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='xingxiangjianshe', doc_type='xingxiangjianshe', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getXingxiangjianshe", methods=["POST"])
def getXingxiangjianshe():
    try:
        params = json.loads(decrypt(request.stream.read()))
        xingxiangjiansheid = params['xingxiangjiansheid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getXingxiangjianshe', 'detail': params})
    doc = es.get(index='xingxiangjianshe', doc_type='xingxiangjianshe', id=xingxiangjiansheid)['_source']
    doc['count'] += 1
    es.index(index='xingxiangjianshe', doc_type='xingxiangjianshe', id=xingxiangjiansheid, body=doc)
    return encrypt(json.dumps({'MSG': 'OK', 'data': doc}))


@app.route(apiqianzui + "getLiaomeishizhanList", methods=["POST"])
def getLiaomeishizhanList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    search = {"query": {"match_all": {}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='liaomeishizhanlist', doc_type='liaomeishizhanlist', body=search, size=10,
                             scroll="5m")

    else:
        Docs = es.search(index='liaomeishizhanlist', doc_type='liaomeishizhanlist', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getLiaomeishizhan", methods=["POST"])
def getLiaomeishizhan():
    try:
        params = json.loads(decrypt(request.stream.read()))
        liaomeishizhanid = params['liaomeishizhanid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getLiaomeishizhan', 'detail': params})
    doc = es.get(index='liaomeishizhanlist', doc_type='liaomeishizhanlist', id=liaomeishizhanid)['_source']
    doc['count'] += 1
    es.index(index='liaomeishizhanlist', doc_type='liaomeishizhanlist', id=liaomeishizhanid, body=doc)
    doc = es.get(index='liaomeishizhan', doc_type='liaomeishizhan', id=liaomeishizhanid)['_source']
    return encrypt(json.dumps({'MSG': 'OK', 'data': doc}))


@app.route(apiqianzui + "getKechengList", methods=["POST"])
def getKechengList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getKechengList', 'detail': params})
    retdata = []
    search = {"query": {"match_all": {}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='kechenglist', doc_type='kechenglist', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='kechenglist', doc_type='kechenglist', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    try:
        goumaidoc = mydb['kechenggoumai'].find_one({'_id': unionid + params['nametype']})
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
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getKecheng", methods=["POST"])
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
    adduserhis({'time': getTime(), 'event': 'getKecheng', 'detail': params})
    if kefenxiang == '0':
        try:
            goumaidoc = mydb['kechenggoumai'].find_one({'_id': unionid + params['nametype']})
            goumaidoc['data'] = json.loads(goumaidoc['data'])
            if kechengid in goumaidoc['data']:
                kefenxiang = '1'
        except:
            None
    if kefenxiang == '1':
        doc = es.get(index='kecheng', doc_type='kecheng', id=neirongid)['_source']
        return encrypt(json.dumps({'MSG': 'YES', 'data': doc}))
    return encrypt(json.dumps({'MSG': 'NO'}))


@app.route(apiqianzui + "searchWenzhangList", methods=["POST"])
def searchWenzhangList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        scroll = params['scroll']
        query = params['query']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    search = {'query': {'match': {'title': query}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='wenzhang', doc_type='wenzhang', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='wenzhang', doc_type='wenzhang', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getTuweiqinghuaList", methods=["POST"])
def getTuweiqinghuaList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    search = {"query": {"match_all": {}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='tuweiqinghua', doc_type='tuweiqinghua', body=search, size=20, scroll="5m")

    else:
        Docs = es.search(index='tuweiqinghua', doc_type='tuweiqinghua', body=search, size=20, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getTuweiqinghua", methods=["POST"])
def getTuweiqinghua():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getTuweiqinghua', 'detail': params})
    tuweiqinghuaid = tuweiqinghua[random.randint(0, len(tuweiqinghua) - 1)]
    doc = es.get(index='tuweiqinghua', doc_type='tuweiqinghua', id=tuweiqinghuaid)
    return encrypt(json.dumps({'MSG': 'OK', 'data': doc['_source']}))


@app.route(apiqianzui + "setJilu", methods=["POST"])
def setJilu():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'setJilu', 'detail': params})
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "getQingganbaike", methods=["POST"])
def getQingganbaike():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    return encrypt(json.dumps({'MSG': 'OK',
                               'rumenjieduan': wangzhi + '/qingganbaike/rumenjieduan.png',
                               'jinjiejieduan': wangzhi + '/qingganbaike/jinjiejieduan.png',
                               'wenda': [{'title': '单身期', 'image': wangzhi + '/qingganbaike/danshenqi.png',
                                          'list': [{'category_name': '聊天搭讪', 'category_id': 6},
                                                   {'category_name': '相亲', 'category_id': 7},
                                                   {'category_name': '社交软件', 'category_id': 8},
                                                   {'category_name': '线下交友', 'category_id': 9},
                                                   {'category_name': '暗恋', 'category_id': 10},
                                                   {'category_name': '形象改造', 'category_id': 11},
                                                   {'category_name': '心态建设', 'category_id': 12},
                                                   {'category_name': '了解女性', 'category_id': 13}, ]},
                                         {'title': '追求期', 'image': wangzhi + '/qingganbaike/zhuiqiuqi.png',
                                          'list': [{'category_name': '吸引女生', 'category_id': 14},
                                                   {'category_name': '聊天技巧', 'category_id': 15},
                                                   {'category_name': '约会', 'category_id': 16},
                                                   {'category_name': '表白', 'category_id': 17}, ]},
                                         {'title': '恋爱期', 'image': wangzhi + '/qingganbaike/lianaiqi.png',
                                          'list': [{'category_name': '异地恋', 'category_id': 18},
                                                   {'category_name': '出轨', 'category_id': 19},
                                                   {'category_name': '长期相处', 'category_id': 20},
                                                   {'category_name': '冷战吵架', 'category_id': 21}, ]},
                                         {'title': '失恋期', 'image': wangzhi + '/qingganbaike/shilianqi.png',
                                          'list': [{'category_name': '挽回复合', 'category_id': 22},
                                                   {'category_name': '重建吸引', 'category_id': 23},
                                                   {'category_name': '挽回沟通', 'category_id': 24},
                                                   {'category_name': '真假分手', 'category_id': 25},
                                                   {'category_name': '走出失恋', 'category_id': 26}, ]},
                                         {'title': '婚姻期', 'image': wangzhi + '/qingganbaike/hunyinqi.png',
                                          'list': [{'category_name': '挽救婚姻', 'category_id': 27},
                                                   {'category_name': '婚外情', 'category_id': 28}, ]}, ],
                               'rumen': [
                                   {'title': '怎么让你的话撩动屏幕后面的她', 'image': wangzhi + '/qingganbaike/wangshangliaomei.png',
                                    'category_name': '网上撩妹', 'category_id': 10},
                                   {'title': '聊天宝典，随机随处可用', 'image': wangzhi + '/qingganbaike/xianxialiaotian.png',
                                    'category_name': '线下聊天', 'category_id': 3},
                                   {'title': '邀约话术，让女生迫不及待的跟你约会', 'image': wangzhi + '/qingganbaike/yaoqingyuehui.png',
                                    'category_name': '邀请约会', 'category_id': 16},
                                   {'title': '搭讪话题，搭讪技巧，让你快速破冰', 'image': wangzhi + '/qingganbaike/yixingdashan.png',
                                    'category_name': '异性搭讪', 'category_id': 13},
                                   {'title': '狙击真命女神，让她对你念念不忘', 'image': wangzhi + '/qingganbaike/jujizhenming.png',
                                    'category_name': '狙击真命', 'category_id': 9},
                                   {'title': '避免表白雷区，表白无压力', 'image': wangzhi + '/qingganbaike/wanmeibiaobai.png',
                                    'category_name': '完美表白', 'category_id': 11}, ],
                               'jinjie': [
                                   {'title': '把控节奏，推进关系，让她离不开你', 'image': wangzhi + '/qingganbaike/quedingguanxi.png',
                                    'category_name': '确定关系', 'category_id': 8},
                                   {'title': '美满而幸福的婚姻是靠经营出来的', 'image': wangzhi + '/qingganbaike/hunyinjingying.png',
                                    'category_name': '婚姻经营', 'category_id': 7},
                                   {'title': '找到情感问题的关键', 'image': wangzhi + '/qingganbaike/fenshouwanhui.png',
                                    'category_name': '分手挽回', 'category_id': 4},
                                   {'title': '升温情感，毁约交往更顺畅', 'image': wangzhi + '/qingganbaike/guanxipobing.png',
                                    'category_name': '关系破冰', 'category_id': 6},
                                   {'title': '相亲小技巧，告别失败阴影', 'image': wangzhi + '/qingganbaike/xiangqinjiqiao.png',
                                    'category_name': '相亲技巧', 'category_id': 14},
                                   {'title': '形象决定气质，改变从现在开始', 'image': wangzhi + '/qingganbaike/xingxiangtisheng.png',
                                    'category_name': '形象提升', 'category_id': 12},
                                   {'title': '有爱，距离不是问题', 'image': wangzhi + '/qingganbaike/yidilian.png',
                                    'category_name': '异地恋', 'category_id': 15}, ], }))


@app.route(apiqianzui + "getQingganbaikeList", methods=["POST"])
def getQingganbaikeList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        category_id = params['category_id']
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    search = {'query': {'bool': {'filter': {"term": {'category_id': category_id}}}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='baikelist', doc_type='baikelist', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='baikelist', doc_type='baikelist', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        doc = doc['_source']
        retdata.append(doc)
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getBaike", methods=["POST"])
def getBaike():
    try:
        params = json.loads(decrypt(request.stream.read()))
        baikeid = params['baikeid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getBaike', 'detail': params})
    doc = es.get(index='baike', doc_type='baike', id=baikeid)['_source']
    listdoc = es.get(index='baikelist', doc_type='baikelist', id=baikeid)['_source']
    listdoc['count'] += 1
    es.index(index='baikelist', doc_type='baikelist', id=baikeid, body=listdoc)
    return encrypt(json.dumps({'MSG': 'OK', 'data': doc}))


@app.route(apiqianzui + "getWendaList", methods=["POST"])
def getWendaList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        category_id = params['category_id']
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    search = {'query': {'bool': {'filter': {"term": {'category_id': category_id}}}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='wendalist', doc_type='wendalist', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='wendalist', doc_type='wendalist', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        doc = doc['_source']
        retdata.append(doc)
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getWenda", methods=["POST"])
def getWenda():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        wendaid = params['wendaid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getWenda', 'detail': params})
    doc = es.get(index='wenda', doc_type='wenda', id=wendaid)['_source']
    listdoc = es.get(index='wendalist', doc_type='wendalist', id=wendaid)['_source']
    listdoc['count'] += 1
    es.index(index='wendalist', doc_type='wendalist', id=wendaid, body=listdoc)
    return encrypt(json.dumps({'MSG': 'OK', 'data': doc}))


@app.route(apiqianzui + "getXinliceshiList", methods=["POST"])
def getXinliceshiList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        category_id = params['category_id']
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    search = {'query': {'bool': {'filter': {"term": {'category_id': category_id}}}}}
    if scroll:
        try:
            Docs = es.scroll(scroll_id=scroll, scroll="5m")
        except:
            Docs = es.search(index='xinliceshilist', doc_type='xinliceshilist', body=search, size=10, scroll="5m")

    else:
        Docs = es.search(index='xinliceshilist', doc_type='xinliceshilist', body=search, size=10, scroll="5m")
    scroll = Docs['_scroll_id']
    Docs = Docs['hits']['hits']
    for doc in Docs:
        doc = doc['_source']
        retdata.append(doc)
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata, 'scroll': scroll}))


@app.route(apiqianzui + "getXinliceshi", methods=["POST"])
def getXinliceshi():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        ceshiid = int(params['ceshiid'])
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getXinliceshi', 'detail': params})
    doc = es.get(index='xinliceshi', doc_type='xinliceshi', id=ceshiid)['_source']
    doc['questions'] = json.loads(doc['questions'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': doc}))


@app.route(apiqianzui + "getCeshidaan", methods=["POST"])
def getCeshidaan():
    try:
        params = json.loads(decrypt(request.stream.read()))
        ceshiid = int(params['ceshiid'])
        ceshitype = params['ceshitype']
        score = int(params['score'])
        optionId = str(params['optionId'])
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getCeshidaan', 'detail': params})
    doc = es.get(index='xinliceshiret', doc_type='xinliceshiret', id=ceshiid)['_source']
    doc['data'] = json.loads(doc['data'])
    retdata = {}
    if ceshitype == 'jump':
        if optionId in doc['data']:
            retdata = doc['data'][optionId]
        else:
            randomindex = random.randint(0, len(doc['data'] - 1))
            t = 0
            for randomret in doc['data']:
                if t == randomindex:
                    retdata = doc['data'][randomret]
                t += 1
    else:
        minscore = doc['min']
        maxscore = doc['max']
        jiange = (maxscore - minscore) / len(doc['data'])
        if jiange != 0:
            index = int((score - minscore) // jiange)
        if index >= 0 and index < len(doc['data']):
            retdata = doc['data'][index]
        else:
            randomindex = random.randint(0, len(doc['data']) - 1)
            retdata = doc['data'][randomindex]
    newdoc = es.get(index='xinliceshilist', doc_type='xinliceshilist', id=ceshiid)['_source']
    newdoc['count'] += 1
    es.index(index='xinliceshilist', doc_type='xinliceshilist', id=ceshiid, body=newdoc)
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata}))


@app.route(apiqianzui + "getvipdengji", methods=["POST"])
def getvipdengji():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    doc = mydb['userinfo'].find_one({'_id': unionid + params['nametype']})
    viptimestr = ''
    if doc['viptime'] > time.time():
        viptimestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(doc['viptime']))
    else:
        viptimestr = '已到期'
    return encrypt(json.dumps(
        {'MSG': 'OK', 'vipdengji': doc['vipdengji'], 'vipdengjimiaoshu': vipdengjimiaoshu[doc['vipdengji']],
         'viptime': viptimestr, 'wenhouyu': 'HI，欢迎您~'}))


@app.route(apiqianzui + "getweixinhao", methods=["POST"])
def getweixinhao():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    weixinhao = appids[params['nametype']]['weixinhao']
    ifkefu = 0
    ifweixin = 1
    ifxiaochengxu = 0
    return encrypt(json.dumps(
        {'MSG': 'OK', 'weixinhao': weixinhao, 'ifkefu': ifkefu, 'ifweixin': ifweixin, 'ifxiaochengxu': ifxiaochengxu}))


@app.route(apiqianzui + "setDianzanshoucangshu", methods=["POST"])
def setDianzanshoucangshu():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        doctype = params['doctype']
        docid = params['docid']
        dianzanshu = params['dianzanshu']
        shoucangshu = params['shoucangshu']
        dianzan = params['dianzan']
        shoucang = params['shoucang']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'setDianzanshoucangshu', 'detail': params})
    doc = es.get(index=doctype, doc_type=doctype, id=docid)['_source']
    doc['dianzan'] = dianzanshu
    doc['shoucangshu'] = shoucangshu
    es.index(index=doctype, doc_type=doctype, id=docid, body=doc)
    wendang = {}
    wendang['doctype'] = doctype
    wendang['docid'] = docid
    wendang['dianzan'] = dianzan
    wendang['shoucang'] = shoucang
    wendang['title'] = doc['title']
    wendang['image'] = doc['image']
    try:
        newdoc = mydb['dianzanshoucang'].find_one({'_id': unionid + params['nametype']})
        flag = 1
        for u, newwendang in enumerate(newdoc['data']):
            if newwendang['docid'] == docid and newwendang['doctype'] == doctype:
                newdoc['data'][u] = wendang
                flag = 0
                break
        if flag: newdoc['data'].append(wendang)
        mydb['dianzanshoucang'].update_one({'_id': unionid + params['nametype']}, {'$set': newdoc}, True)
    except:
        newdoc = {'data': [wendang]}
        mydb['dianzanshoucang'].update_one({'_id': unionid + params['nametype']}, {'$set': newdoc}, True)
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "getDianzanshoucangList", methods=["POST"])
def getDianzanshoucangList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    retdata = []
    try:
        doc = mydb['dianzanshoucang'].find_one({'_id': unionid + params['nametype']})
        retdata = doc['data']
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata}))


@app.route(apiqianzui + "getDianzanshoucang", methods=["POST"])
def getDianzanshoucang():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        doctype = params['doctype']
        docid = params['docid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    dianzan = 0
    shoucang = 0
    try:
        doc = mydb['dianzanshoucang'].find_one({'_id': unionid + params['nametype']})
        for newdoc in doc['data']:
            if newdoc['docid'] == docid and newdoc['doctype'] == doctype:
                dianzan = newdoc['dianzan']
                shoucang = newdoc['shoucang']
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK', 'dianzan': dianzan, 'shoucang': shoucang}))


@app.route(apiqianzui + "setDianzanshoucang", methods=["POST"])
def setDianzanshoucang():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        DianzanshoucangList = params['DianzanshoucangList']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    mydb['dianzanshoucang'].dpdate_one({'_id': unionid + params['nametype']}, {'$set': {'data': DianzanshoucangList}},
                                       True)
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "getIoswenan", methods=["POST"])
def getIoswenan():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    return encrypt(json.dumps({'MSG': 'OK', 'data': ioswenan}))


@app.route(apiqianzui + "get_jiage", methods=["POST"])
def get_jiage():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'get_jiage', 'params': params})
    jiage = {'jiage': total_fees[4] * 0.005, 'miaoshu': '年授权码'}
    return encrypt(json.dumps(
        {'MSG': 'OK', 'jiage': jiage}))


@app.route(apiqianzui + "get_prepay_id", methods=["POST"])
def get_prepay_id():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        zhifutype = int(params['zhifutype'])
        apptype = params['apptype']
        nametype = params['nametype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    trade_type = 'JSAPI'
    zhifubili = 1.0
    profit_sharing = 'Y'
    if apptype == 'fwh':
        nowappid = fuwuhaoappid
        zhifubili = 0.5
        profit_sharing = 'N'
        openid = mydb['userinfo'].find_one({'_id': unionid + nowappid})['fwhid']
    if apptype == 'weixin':
        nowappid = nametype
        openid = mydb['userinfo'].find_one({'_id': unionid + nametype})['openid']
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    prepaydata = {
        'appid': nowappid,
        'mch_id': appids[params['nametype']]['mch_id'],
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
        'device_info': nametype,
        'body': vipdengjimiaoshu[zhifutype],
        'attach': json.dumps({'zhifutype': zhifutype, 'detail': vipdengjimiaoshu[zhifutype], 'unionid': unionid},
                             ensure_ascii=False),
        'out_trade_no': str(int(time.time())) + '_' + str((random.randint(1000000, 9999999))),
        'total_fee': int(total_fees[zhifutype] * zhifubili),
        'spbill_create_ip': request.remote_addr,
        'notify_url': wangzhi + apiqianzui + "paynotify",
        'trade_type': trade_type,
        'openid': openid,
        'profit_sharing': profit_sharing,
    }
    stringA = '&'.join(["{0}={1}".format(k, prepaydata.get(k)) for k in sorted(prepaydata)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    prepaydata['sign'] = sign
    req = urllib.request.Request(url, dict_to_xml(prepaydata).encode('utf8'),
                                 headers={'Content-Type': 'application/xml'})
    result = urllib.request.urlopen(req, timeout=10).read().decode('utf8')
    result = xml_to_dict(result)
    prepay_id = result['prepay_id']
    if apptype == 'weixin' or apptype == 'fwh':
        paySign_data = {
            'appId': nowappid,
            'timeStamp': str(int(time.time())),
            'nonceStr': result['nonce_str'],
            'package': 'prepay_id={0}'.format(prepay_id),
            'signType': 'MD5'
        }
    else:
        paySign_data = {
            'appid': nowappid,
            'partnerid': appids[params['nametype']]['mch_id'],
            'prepayid': prepay_id,
            'package': 'Sign=WXPay',
            'noncestr': result['nonce_str'],
            'timestamp': str(int(time.time())),
        }
    stringA = '&'.join(["{0}={1}".format(k, paySign_data.get(k)) for k in sorted(paySign_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    if apptype == 'weixin' or apptype == 'fwh':
        paySign_data['paySign'] = paySign
    else:
        paySign_data['sign'] = paySign
    return encrypt(json.dumps({'MSG': 'OK', 'data': paySign_data}))


def fenzhang(req):
    # result = urllib.request.urlopen(req, timeout=10).read().decode('utf8')
    # result = xml_to_dict(result)
    return None


@app.route(apiqianzui + "paynotify", methods=["POST"])
def paynotify():
    zhifures = xml_to_dict(request.stream.read().decode('utf8'))
    sign = zhifures['sign']
    zhifures.pop('sign')
    unionid = json.loads(zhifures['attach'])['unionid']
    nowappid = zhifures['device_info']
    params = mydb['userinfo'].find_one({'_id': unionid + nowappid})
    stringA = '&'.join(["{0}={1}".format(k, zhifures.get(k)) for k in sorted(zhifures)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest().upper()
    if sign != paySign:
        return dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'})
    zhifudata = [zhifures]
    zhifutype = int(json.loads(zhifures['attach'])['zhifutype'])
    isnew = 1
    flag = 1
    try:
        doc = mydb['userzhifu'].find_one({'_id': unionid + nowappid})
        isnew = 0
        for line in doc['zhifudata']:
            if line['transaction_id'] == zhifudata[0]['transaction_id']:
                flag = 0
        if flag:
            zhifudata += doc['zhifudata']
    except Exception as e:
        logger.error(e)
    zhifures['total_fee'] = int(zhifures['total_fee'])
    if isnew or (isnew == 0 and flag == 1):
        mydb['userzhifu'].update_one({'_id': unionid + nowappid}, {
            '$set': {'unionid': unionid, 'zhifudata': zhifudata, 'updatatime': zhifures['time_end']}}, True)
        userdoc = mydb['userinfo'].find_one({'_id': unionid + nowappid})
        try:
            if userdoc['vipdengji'] < zhifutype:
                userdoc['vipdengji'] = zhifutype
            if userdoc['viptime'] < int(time.time()):
                userdoc['viptime'] = int(time.time()) + viptime[zhifutype]
            else:
                userdoc['viptime'] += viptime[zhifutype]
            userdoc['xiaofeicishu'] += 1
            userdoc['xiaofeizonge'] += zhifures['total_fee']
            mydb['userinfo'].update_one({'_id': unionid + nowappid}, {'$set': userdoc}, True)
        except Exception as e:
            logger.error(e)
    if nowappid == 'wx2cc1bc5a412d44d2':
        shouquanma = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        while mydb['shouquanma'].find_one({'_id': shouquanma}):
            shouquanma = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        nowtime = getTime()
        mydb['shouquanma'].update_one({'_id': shouquanma}, {
            '$set': {'shouquanma': shouquanma, 'goumaiunionid': unionid, 'zhuangtai': '未激活',
                     'jiage': total_fees[1] * 0.5,
                     'viptime': viptime[4], 'vipdengji': 4, 'zhifuzhuangtai': 1, 'goumaishijian': nowtime,
                     'jiesuanshijian': nowtime, 'jihuoshijian': '-', 'jihuoopenid': '-', 'jihuorenyuan': '-'}}, True)
    if nowappid == 'wx311bf0a55020cb9e':
        url = 'https://api.mch.weixin.qq.com/secapi/pay/profitsharing'
        prepaydata = {
            'appid': nowappid,
            'mch_id': appids[params['nametype']]['mch_id'],
            'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
            'transaction_id': zhifures['transaction_id'],
            'out_order_no': zhifures['transaction_id'] + zhifures['transaction_id'],
            'receivers': [{'type': 'PERSONAL_OPENID', 'account': 'oM9fn5Tl5K-4CEj-hVR1FHyeyKq0',
                           'amount': int(zhifures['total_fee'] * 0.2), 'description': '分账到个人'}]
        }
        stringA = '&'.join(["{0}={1}".format(k, prepaydata.get(k)) for k in sorted(prepaydata)])
        stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
        sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
        prepaydata['sign'] = sign
        req = urllib.request.Request(url, dict_to_xml(prepaydata).encode('utf8'),
                                     headers={'Content-Type': 'application/xml'})
        fenzhang(req)
    return dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'})


@app.route(apiqianzui + "jieqing_prepay_id", methods=["POST"])
def jieqing_prepay_id():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        apptype = params['apptype']
        nametype = params['nametype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    nowappid = fuwuhaoappid
    trade_type = 'JSAPI'
    openid = mydb['userinfo'].find_one({'_id': unionid + nowappid})['fwhid']
    docs = mydb['shouquanma'].find(
        {'goumaiunionid': params['unionid'], 'zhifuzhuangtai': 0, 'tingyong': 0, 'zhuangtai': '已激活'}).limit(10000)
    yuekashu = 0
    zhongshenkashu = 0
    yuekazonge = 0
    zhongshenkazonge = 0
    for doc in docs:
        if doc['vipdengji'] == 1:
            zhongshenkashu += 1
            zhongshenkazonge += doc['jiage']
        if doc['vipdengji'] == 2:
            yuekashu += 1
            yuekazonge += doc['jiage']
    jieqingzonge = zhongshenkazonge + yuekazonge
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    prepaydata = {
        'appid': nowappid,
        'mch_id': appids[params['nametype']]['mch_id'],
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
        'device_info': nametype,
        'body': getTime(),
        'attach': json.dumps({'yuekashu': yuekashu, 'zhongshenkashu': zhongshenkashu, 'unionid': unionid},
                             ensure_ascii=False),
        'out_trade_no': str(int(time.time())) + '_' + str((random.randint(1000000, 9999999))),
        'total_fee': jieqingzonge,
        'spbill_create_ip': request.remote_addr,
        'notify_url': wangzhi + apiqianzui + "jieqing_paynotify",
        'trade_type': trade_type,
        'openid': openid,
    }
    stringA = '&'.join(["{0}={1}".format(k, prepaydata.get(k)) for k in sorted(prepaydata)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    prepaydata['sign'] = sign
    req = urllib.request.Request(url, dict_to_xml(prepaydata).encode('utf8'),
                                 headers={'Content-Type': 'application/xml'})
    result = urllib.request.urlopen(req, timeout=10).read().decode('utf8')
    result = xml_to_dict(result)
    prepay_id = result['prepay_id']
    if apptype == 'weixin' or apptype == 'fwh':
        paySign_data = {
            'appId': nowappid,
            'timeStamp': str(int(time.time())),
            'nonceStr': result['nonce_str'],
            'package': 'prepay_id={0}'.format(prepay_id),
            'signType': 'MD5'
        }
    else:
        paySign_data = {
            'appid': nowappid,
            'partnerid': appids[params['nametype']]['mch_id'],
            'prepayid': prepay_id,
            'package': 'Sign=WXPay',
            'noncestr': result['nonce_str'],
            'timestamp': str(int(time.time())),
        }
    stringA = '&'.join(["{0}={1}".format(k, paySign_data.get(k)) for k in sorted(paySign_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    if apptype == 'weixin' or apptype == 'fwh':
        paySign_data['paySign'] = paySign
    else:
        paySign_data['sign'] = paySign
    return encrypt(json.dumps({'MSG': 'OK', 'data': paySign_data}))


@app.route(apiqianzui + "jieqing_paynotify", methods=["POST"])
def jieqing_paynotify():
    zhifures = xml_to_dict(request.stream.read().decode('utf8'))
    sign = zhifures['sign']
    zhifures.pop('sign')
    unionid = json.loads(zhifures['attach'])['unionid']
    nowappid = zhifures['device_info']
    params = mydb['userinfo'].find_one({'_id': unionid + nowappid})
    stringA = '&'.join(["{0}={1}".format(k, zhifures.get(k)) for k in sorted(zhifures)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest().upper()
    if sign != paySign:
        return dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'})
    zhifudata = [zhifures]
    isnew = 1
    flag = 1
    try:
        doc = mydb['userzhifu'].find_one({'_id': unionid + nowappid})
        isnew = 0
        for line in doc['zhifudata']:
            if line['transaction_id'] == zhifudata[0]['transaction_id']:
                flag = 0
        if flag:
            zhifudata += doc['zhifudata']
    except Exception as e:
        logger.error(e)
    if isnew or (isnew == 0 and flag == 1):
        mydb['userzhifu'].update_one({'_id': unionid + nowappid}, {
            '$set': {'unionid': unionid, 'zhifudata': zhifudata, 'updatatime': zhifures['time_end']}}, True)
        userdoc = mydb['userinfo'].find_one({'_id': unionid + nowappid})
        zhifures['total_fee'] = int(zhifures['total_fee'])
        try:
            userdoc['xiaofeicishu'] += 1
            userdoc['xiaofeizonge'] += zhifures['total_fee']
            mydb['userinfo'].update_one({'_id': unionid + nowappid}, {'$set': userdoc}, True)
        except Exception as e:
            logger.error(e)
    try:
        yuekashu = json.loads(zhifures['attach'])['yuekashu']
        zhongshenkashu = json.loads(zhifures['attach'])['zhongshenkashu']
        docs = mydb['shouquanma'].find(
            {'goumaiunionid': unionid, 'zhifuzhuangtai': 0, 'vipdengji': 2, 'tingyong': 0, 'zhuangtai': '已激活'}).limit(
            yuekashu)
        nowtime = getTime()
        for doc in docs:
            doc['zhifuzhuangtai'] = 1
            doc['jiesuanshijian'] = nowtime
            mydb['shouquanma'].update_one({'_id': doc['shouquanma']}, {'$set': doc}, True)
        docs = mydb['shouquanma'].find(
            {'goumaiunionid': unionid, 'zhifuzhuangtai': 0, 'vipdengji': 1, 'tingyong': 0, 'zhuangtai': '已激活'}).limit(
            zhongshenkashu)
        for doc in docs:
            doc['zhifuzhuangtai'] = 1
            doc['jiesuanshijian'] = nowtime
            mydb['shouquanma'].update_one({'_id': doc['shouquanma']}, {'$set': doc}, True)
    except:
        None
    return dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'})


@app.route(apiqianzui + 'jihuo', methods=['POST'])
def jihuo():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    shouquanma = params['shouquanma'].strip()
    shouquanmadoc = mydb['shouquanma'].find_one({'_id': shouquanma})
    if shouquanmadoc == None or shouquanmadoc['zhuangtai'] == '已激活':
        return encrypt(json.dumps({'MSG': 'NO'}, ensure_ascii=False))
    jihuoopenid = params['unionid']
    nametype = params['nametype']
    shouquanmadoc['zhuangtai'] = '已激活'
    shouquanmadoc['jihuoshijian'] = getTime()
    shouquanmadoc['jihuoopenid'] = jihuoopenid
    shouquanmadoc['appid'] = nametype
    userdoc = mydb['userinfo'].find_one({'_id': jihuoopenid + nametype})
    if userdoc['vipdengji'] == 1 or (userdoc['vipdengji'] == 2 and shouquanmadoc['vipdengji'] == 2):
        return encrypt(json.dumps({'MSG': 'NO'}, ensure_ascii=False))
    userdoc['vipdengji'] = shouquanmadoc['vipdengji']
    if userdoc['viptime'] < int(time.time()):
        userdoc['viptime'] = int(time.time()) + shouquanmadoc['viptime']
    else:
        userdoc['viptime'] += shouquanmadoc['viptime']
    userdoc['tingyong'] = 0
    mydb['userinfo'].update_one({'_id': jihuoopenid + nametype}, {'$set': userdoc}, True)
    shouquanmadoc['jihuorenyuan'] = userdoc['nickName']
    mydb['shouquanma'].update_one({'_id': shouquanma}, {'$set': shouquanmadoc}, True)
    return encrypt(json.dumps({'MSG': 'OK'}, ensure_ascii=False))


@app.route(apiqianzui + 'get_shouquanmalist', methods=['POST'])
def get_shouquanmalist():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    shouquanmalist = []
    jihuoshu = 0
    try:
        Docs = mydb['shouquanma'].find({'goumaiunionid': params['unionid']}).limit(10000)
        for doc in Docs:
            shouquanmalist.append(doc)
            if doc['zhuangtai'] == '已激活':
                jihuoshu += 1
    except:
        None
    return encrypt(
        json.dumps({'MSG': 'NO', 'shouquanmalist': shouquanmalist, 'jihuoshu': jihuoshu}, ensure_ascii=False))


@app.route(apiqianzui + 'get_weifukuan', methods=['POST'])
def get_weifukuan():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    docs = mydb['shouquanma'].find(
        {'goumaiunionid': params['unionid'], 'zhifuzhuangtai': 0, 'tingyong': 0, 'zhuangtai': '已激活'}).limit(10000)
    yuekashu = 0
    zhongshenkashu = 0
    yuekazonge = 0
    zhongshenkazonge = 0
    for doc in docs:
        if doc['vipdengji'] == 1:
            zhongshenkashu += 1
            zhongshenkazonge += doc['jiage']
        if doc['vipdengji'] == 2:
            yuekashu += 1
            yuekazonge += doc['jiage']
    zhongshenkazonge *= 0.01
    yuekazonge *= 0.01
    zonge = zhongshenkazonge + yuekazonge
    return encrypt(
        json.dumps({'MSG': 'OK', 'weifukuan': {'miaoshu0': '月卡未付个数', 'jiage0': yuekazonge, 'yuekashu': yuekashu,
                                               'miaoshu1': '终身卡未付个数', 'jiage1': zhongshenkazonge,
                                               'zhongshenkashu': zhongshenkashu, 'zonge': zonge}},
                   ensure_ascii=False))


@app.route(apiqianzui + 'tingyongshouquanma', methods=['POST'])
def tingyongshouquanma():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    for line in params['tingshouquanma'].split('\n'):
        try:
            doc = mydb['shouquanma'].find_one({'_id': line})
            doc['tingyong'] = 1
            mydb['shouquanma'].update_one({'_id': doc['shouquanma']}, {'$set': doc}, True)
            jihuoopenid = doc['jihuoopenid']
            p = '^' + jihuoopenid
            userdoc = mydb['userinfo'].find_one({'_id': {"$regex": p}, })
            userdoc['tingyong'] = 1
            mydb['userinfo'].update_one({'_id': userdoc['_id']}, {'$set': userdoc}, True)
        except:
            None
    return encrypt(
        json.dumps({'MSG': 'OK'}, ensure_ascii=False))


@app.route(apiqianzui + 'qiyongshouquanma', methods=['POST'])
def qiyongshouquanma():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    for line in params['qishouquanma'].split('\n'):
        try:
            doc = mydb['shouquanma'].find_one({'_id': line})
            doc['tingyong'] = 0
            mydb['shouquanma'].update_one({'_id': doc['shouquanma']}, {'$set': doc}, True)
            jihuoopenid = doc['jihuoopenid']
            p = '^' + jihuoopenid
            userdoc = mydb['userinfo'].find_one({'_id': {"$regex": p}, })
            userdoc['tingyong'] = 0
            mydb['userinfo'].update_one({'_id': userdoc['_id']}, {'$set': userdoc}, True)
        except:
            None
    return encrypt(
        json.dumps({'MSG': 'OK'}, ensure_ascii=False))


@app.route(apiqianzui + 'get_yueshouquanma', methods=['POST'])
def get_yueshouquanma():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    docs = mydb['shouquanma'].find(
        {'goumaiunionid': params['unionid'], 'zhifuzhuangtai': 0, 'tingyong': 0, 'zhuangtai': '已激活'}).limit(10000)
    for doc in docs:
        return encrypt(
            json.dumps({'MSG': 'NO'}, ensure_ascii=False))
    yueshouquanma = ''
    numshouquanma = 0
    nowtime = '^' + getTime()[:10]
    docs = mydb['shouquanma'].find(
        {'goumaiunionid': params['unionid'], 'zhifuzhuangtai': 0, 'tingyong': 0, 'zhuangtai': '未激活', 'vipdengji': 2,
         'goumaishijian': {"$regex": nowtime}}).limit(10000)
    for doc in docs:
        numshouquanma += 1
        yueshouquanma += doc['shouquanma'] + '\n'
    nowtime = getTime()
    for i in range(meirigeshu - numshouquanma):
        try:
            shouquanma = 'yue_' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
            while mydb['shouquanma'].find_one({'_id': shouquanma}):
                shouquanma = 'yue_' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
            yueshouquanma += shouquanma + '\n'
            mydb['shouquanma'].update_one({'_id': shouquanma}, {
                '$set': {'shouquanma': shouquanma, 'goumaiunionid': params['unionid'], 'zhuangtai': '未激活',
                         'jiage': total_fees[2], 'tingyong': 0,
                         'viptime': viptime[2], 'vipdengji': 2, 'zhifuzhuangtai': 0, 'goumaishijian': nowtime,
                         'jiesuanshijian': '-', 'jihuoshijian': '-', 'jihuoopenid': '-', 'jihuorenyuan': '-'}},
                                          True)
        except:
            None
    return encrypt(
        json.dumps({'MSG': 'OK', 'yueshouquanma': yueshouquanma}, ensure_ascii=False))


@app.route(apiqianzui + 'get_zhongshenshouquanma', methods=['POST'])
def get_zhongshenshouquanma():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    docs = mydb['shouquanma'].find(
        {'goumaiunionid': params['unionid'], 'zhifuzhuangtai': 0, 'tingyong': 0, 'zhuangtai': '已激活'}).limit(10000)
    for doc in docs:
        return encrypt(
            json.dumps({'MSG': 'NO'}, ensure_ascii=False))
    zhongshenshouquanma = ''
    numshouquanma = 0
    nowtime = '^' + getTime()[:10]
    docs = mydb['shouquanma'].find(
        {'goumaiunionid': params['unionid'], 'zhifuzhuangtai': 0, 'tingyong': 0, 'zhuangtai': '未激活', 'vipdengji': 1,
         'goumaishijian': {"$regex": nowtime}}).limit(10000)
    for doc in docs:
        numshouquanma += 1
        zhongshenshouquanma += doc['shouquanma'] + '\n'
    nowtime = getTime()
    for i in range(meirigeshu - numshouquanma):
        try:
            shouquanma = 'zhongshen_' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
            while mydb['shouquanma'].find_one({'_id': shouquanma}):
                shouquanma = 'zhongshen_' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
            zhongshenshouquanma += shouquanma + '\n'
            mydb['shouquanma'].update_one({'_id': shouquanma}, {
                '$set': {'shouquanma': shouquanma, 'goumaiunionid': params['unionid'], 'zhuangtai': '未激活',
                         'jiage': total_fees[2], 'tingyong': 0,
                         'viptime': viptime[1], 'vipdengji': 1, 'zhifuzhuangtai': 0, 'goumaishijian': nowtime,
                         'jiesuanshijian': '-', 'jihuoshijian': '-', 'jihuoopenid': '-', 'jihuorenyuan': '-'}},
                                          True)
        except:
            None
    return encrypt(
        json.dumps({'MSG': 'OK', 'zhongshenshouquanma': zhongshenshouquanma}, ensure_ascii=False))


@app.route(apiqianzui + "get_kechengprepay_id", methods=["POST"])
def get_kechengprepay_id():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        kechengid = params['kechengid']
        detail = params['detail']
        nametype = params['nametype']
        apptype = params['apptype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    if apptype == 'weixin':
        nowappid = nametype
        trade_type = 'JSAPI'
        openid = mydb['userinfo'].find_one({'_id': unionid + nametype})['openid']
    elif apptype == 'fwh':
        nowappid = fuwuhaoappid
        trade_type = 'JSAPI'
        openid = mydb['userinfo'].find_one({'_id': unionid + nametype})['openid']['fwhid']
    else:
        nametype = params['nametype']
        nowappid = apps[nametype]['appid']
        trade_type = 'APP'
        openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['yingyongid']
    kechengjiage = int(es.get(index='kechenglist', doc_type='kechenglist', id=kechengid)['_source']['jiage'] * 100)
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    prepaydata = {
        'appid': nowappid,
        'mch_id': appids[params['nametype']]['mch_id'],
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
        'device_info': nametype,
        'body': detail,
        'attach': json.dumps({'kechengid': kechengid, 'detail': '课程', 'unionid': unionid}, ensure_ascii=False),
        'out_trade_no': str(int(time.time())) + '_' + str((random.randint(1000000, 9999999))),
        'total_fee': kechengjiage,
        'spbill_create_ip': request.remote_addr,
        'notify_url': wangzhi + apiqianzui + "kechengpaynotify",
        'trade_type': trade_type,
        'openid': openid,
        'profit_sharing': 'Y',
    }
    stringA = '&'.join(["{0}={1}".format(k, prepaydata.get(k)) for k in sorted(prepaydata)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    prepaydata['sign'] = sign
    req = urllib.request.Request(url, dict_to_xml(prepaydata).encode('utf8'),
                                 headers={'Content-Type': 'application/xml'})
    result = urllib.request.urlopen(req, timeout=10).read().decode('utf8')
    result = xml_to_dict(result)
    prepay_id = result['prepay_id']
    if apptype == 'weixin' or apptype == 'fwh':
        paySign_data = {
            'appId': nowappid,
            'timeStamp': str(int(time.time())),
            'nonceStr': result['nonce_str'],
            'package': 'prepay_id={0}'.format(prepay_id),
            'signType': 'MD5'
        }
    else:
        paySign_data = {
            'appid': nowappid,
            'partnerid': appids[params['nametype']]['mch_id'],
            'prepayid': prepay_id,
            'package': 'Sign=WXPay',
            'noncestr': result['nonce_str'],
            'timestamp': str(int(time.time())),
        }
    stringA = '&'.join(["{0}={1}".format(k, paySign_data.get(k)) for k in sorted(paySign_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    if apptype == 'weixin' or apptype == 'fwh':
        paySign_data['paySign'] = paySign
    else:
        paySign_data['sign'] = paySign
    return encrypt(json.dumps({'MSG': 'OK', 'data': paySign_data}))


@app.route(apiqianzui + "kechengpaynotify", methods=["POST"])
def kechengpaynotify():
    zhifures = xml_to_dict(request.stream.read().decode('utf8'))
    sign = zhifures['sign']
    zhifures.pop('sign')
    unionid = json.loads(zhifures['attach'])['unionid']
    nowappid = zhifures['device_info']
    params = mydb['userinfo'].find_one({'_id': unionid + nowappid})
    stringA = '&'.join(["{0}={1}".format(k, zhifures.get(k)) for k in sorted(zhifures)])
    stringSignTemp = '{0}&key={1}'.format(stringA, appids[params['nametype']]['merchant_key'])
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest().upper()
    if sign != paySign:
        return dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'})
    zhifudata = [zhifures]
    isnew = 1
    flag = 1
    try:
        doc = mydb['userzhifu'].find_one({'_id': unionid + params['nametype']})
        isnew = 0
        for line in doc['zhifudata']:
            if line['transaction_id'] == zhifudata[0]['transaction_id']:
                flag = 0
        if flag:
            zhifudata += doc['_source']['zhifudata']
    except Exception as e:
        logger.error(e)
    if isnew or (isnew == 0 and flag == 1):
        mydb['userzhifu'].update_one({'_id': unionid + nowappid}, {
            '$set': {'unionid': unionid, 'zhifudata': zhifudata, 'updatatime': zhifures['time_end']}}, True)
        userdoc = mydb['userinfo'].find_one({'_id': unionid + nowappid})
        zhifures['total_fee'] = int(zhifures['total_fee'])
        try:
            userdoc['xiaofeicishu'] += 1
            userdoc['xiaofeizonge'] += zhifures['total_fee']
            mydb['userinfo'].update_one({'_id': unionid + nowappid}, {'$set': userdoc}, True)
        except Exception as e:
            logger.error(e)
        try:
            kechengid = json.loads(zhifures['attach'])['kechengid']
            try:
                goumaidoc = mydb['kechenggoumai'].find_one({'_id': unionid + nowappid})
                goumaidoc['data'] = json.loads(goumaidoc['data'])
                goumaidoc['data'][kechengid] = 1
            except:
                goumaidoc = {}
                goumaidoc['unionid'] = unionid
                goumaidoc['data'] = {}
                goumaidoc['data'][kechengid] = 1
            goumaidoc['data'] = json.dumps(goumaidoc['data'], ensure_ascii=False)
            mydb['kechenggoumai'].update_one({'_id': unionid + nowappid}, {'$set': goumaidoc}, True)
        except Exception as e:
            logger.error(e)
    return dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'})


@app.route(apiqianzui + "getJiagelist", methods=["POST"])
def getJiagelist():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    contentlist = ['1、20万+条撩妹话术可供搜索', '2、上万+条撩妹套路可供参考', '3、百万+张逗趣表情可供搜索', '4、丰富的聊天实战案例', '5、丰富的展示面案例', '6、丰富的恋爱百科知识',
                   '7、丰富的土味情话', '8、丰富的心理测试', '9、500人答疑群']
    jiagelist = [{'jiage': total_fees[0], 'miaoshu': vipdengjimiaoshu[0], 'contentlist': contentlist},
                 {'jiage': total_fees[1], 'miaoshu': vipdengjimiaoshu[1], 'contentlist': contentlist},
                 {'jiage': total_fees[2], 'miaoshu': vipdengjimiaoshu[2], 'contentlist': contentlist},
                 {'jiage': total_fees[3], 'miaoshu': vipdengjimiaoshu[3], 'contentlist': contentlist},
                 {'jiage': total_fees[4], 'miaoshu': vipdengjimiaoshu[4], 'contentlist': contentlist}, ]
    return encrypt(json.dumps({'MSG': 'OK', 'jiagelist': jiagelist}))


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 14888), app)
    server.serve_forever()
