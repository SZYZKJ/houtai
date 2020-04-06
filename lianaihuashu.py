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
mydb = myclient["lianaihuashu"]
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log/log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
xiaochengxus = {'lianaihuashuai': {'appid': 'wxa9ef833cef143ce1', 'secret': '574ba86bc66b664ab42e4d60276afb7c'},
                'lianaihuashu': {'appid': 'wx37ef7f5da5362166', 'secret': 'd0e1cce029a3eec467ce439a3b4cb750'},
                'lianaishenqi': {'appid': 'wx162c6dee9b3f10f4', 'secret': 'ced8850a46d89b0156b8f083d6111aaf'},
                'liaotianhuashu': {'appid': 'wx81e1a4ccc8385f3a', 'secret': 'be67438b9553c084c6e10041b69a8d8d'},
                'liaotianshenqi': {'appid': 'wx37351e7c4754d5fd', 'secret': '25a70835c7e02b7a7aff8be37a72e1d6'},
                'tuodanhuashu': {'appid': 'wxfd8bc693434e910f', 'secret': '72e3a71fc433defaa6acb485b4ed51bb'}}
fuwuhaoappid = 'wx2cc1bc5a412d44d2'
fuwuhaoAppSecret = '3290467fd91f3e4ae427fca28d0137c9'
apps = {'lianaituodanhuashu': {'appid': 'wx492758c5b72a2e3f', 'secret': '89be1eaaf1cc9b5fc744488f2e404491'},
        'lianaihuashu': {'appid': 'wxa3fd03bd67991724', 'secret': '9603dcb14f0728e3cc2df4ad5ac51100'},
        'tuodanhuashu': {'appid': 'wxe8d85652ce34761a', 'secret': 'bb5da1ed0b7663bf815eb14cb28ba814'},
        'liaotianhuashu': {'appid': 'wx95d8198056366e70', 'secret': 'b1d31434470fe63a07a6355b49c2bd95'},
        'lianaishenqi': {'appid': 'wxf826c7c4ef8113c3', 'secret': 'a699107b8e5ad3081bdc6540dbe243bb'},
        'liaotianshenqi': {'appid': 'wx8d09d578e92e9eca', 'secret': '48bd1b8daba333f1a799701e549e15aa'}}
mch_id = '1519367291'
merchant_key = 'shenzhenyuzikejiyouxiangongsi888'
key = "szyzkjpangyuming"
iv = "abcde920318abcde"
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * bytes(chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), encoding='utf8')
unpad = lambda s: s[0:-ord(s[-1])]
tixianunionid = {}
tixianunionid_time = {}
vipdengji = [0, 1, 2, 3, 4, 5, 6]
viptime = [86400, 3153600000, 3153600000, 3153600000, 3153600000, 3153600000, 3153600000]
sijiaotime = [0, 0, 2592000, 15552000, 7776000, 31536000, 3153600000]
total_fees = [0, 19900, 199900, 49900, 99900, 299900, 499900]
# viptime = [0, 60, 60, 60, 60, 60, 60]
# sijiaotime = [0, 60, 60, 60, 60, 60, 60]
# total_fees = [0, 19900, 199900, 1, 99900, 299900, 499900]
tuweiqinghua = []
for line in open('tuweiqinghua.json'):
    line = json.loads(line)
    tuweiqinghua.append(line['id'])
tiyancishu = 3
pingguoshenhe = 1
baidushenhe = 1
tengxunshenhe = 0
weixinshenhe = 1
weixinpingguoshenhe = 1
if weixinshenhe == 1:
    ioswenan = '由于相关规范，小程序下IOS虚拟商品支付暂不可用。'
else:
    ioswenan = '由于相关规范，小程序下IOS虚拟商品支付暂不可用。IOS用户请到个人页咨询在线客服。'
istuiguang = 0
nowversion = '1.1.1'
apiqianzui = '/xcx/'


def adduserhis(userhis):
    es.index(index='userhis', doc_type='userhis', body=userhis)
    return None


@app.route(apiqianzui + "getIslianmeng", methods=["POST"])
def getIslianmeng():
    try:
        params = json.loads(decrypt(request.stream.read()))
        system = params['system']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    nowbaidushenhe = 0
    if params['apptype'] == 'baidu':
        nowbaidushenhe = baidushenhe
    if system[:3].lower() == 'ios':
        return encrypt(json.dumps(
            {'MSG': 'OK', 'istuiguang': istuiguang, 'weixinshenhe': weixinshenhe,
             'weixinpingguoshenhe': weixinpingguoshenhe, 'pingguoshenhe': pingguoshenhe, 'tengxunshenhe': 0,
             'baidushenhe': nowbaidushenhe}))
    else:
        return encrypt(json.dumps(
            {'MSG': 'OK', 'istuiguang': istuiguang, 'weixinshenhe': weixinshenhe, 'weixinpingguoshenhe': 0,
             'pingguoshenhe': 0,
             'tengxunshenhe': tengxunshenhe, 'baidushenhe': nowbaidushenhe, 'appleshenhe': 1}))


@app.route(apiqianzui + "jianChagengxin", methods=["POST"])
def jianChagengxin():
    try:
        params = json.loads(decrypt(request.stream.read()))
        version = params['version']
        apptype = params['apptype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    nametype = 'lianaituodanhuashu'
    if 'nametype' in params:
        nametype = params['nametype']
    gengxintype = 0
    msgtype = 0
    msgtext = ''
    openurl = wangzhi
    if version < nowversion:
        gengxintype = 1  # 更新
        # gengxintype = 2  # 打开网页
    gengxinurl = wangzhi + '/app/' + apptype + '_' + nametype + '.wgt'
    return encrypt(json.dumps({'MSG': 'YES',
                               'data': {'gengxintype': gengxintype, 'gengxinurl': gengxinurl, 'openurl': openurl,
                                        'msgtype': msgtype, 'msgtext': msgtext}}))


@app.route(apiqianzui + "checkVersion", methods=["POST"])
def checkVersion():
    oldversion = request.form['version']
    andoridupdatetype = 0
    iosupdatetype = 0
    if oldversion < nowversion:
        andoridupdatetype = 1
        iosupdatetype = 1
    andoridxiaourl = 'https://www.lianaizhuli.com/app_lianaituodanhuashu.wgt'
    andoriddaurl = 'http://www.lianaizhuli.com/'
    andoridurl = 'https://www.lianaizhuli.com/app.apk'
    iosxiaourl = 'https://www.lianaizhuli.com/app_lianaituodanhuashu.wgt'
    iosdaurl = 'http://www.lianaizhuli.com/'
    androidmagtype = 0
    androidmsg = ''
    iosmsgtype = 0
    isomsg = ''
    return json.dumps({'MSG': 'YES',
                       'data': {'andoridupdatetype': andoridupdatetype, 'andoridxiaourl': andoridxiaourl,
                                'andoriddaurl': andoriddaurl, 'andoridurl': andoridurl, 'iosupdatetype': iosupdatetype,
                                'iosxiaourl': iosxiaourl,
                                'iosdaurl': iosdaurl, 'androidmagtype': androidmagtype, 'androidmsg': androidmsg,
                                'iosmsgtype': iosmsgtype, 'isomsg': isomsg, 'version': nowversion}})


@app.route(apiqianzui + "getShouyekuai", methods=["POST"])
def getShouyekuai():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    return encrypt(json.dumps({'MSG': 'OK', 'lunbotu': [
        # {'title': '分销', 'adurl': wangzhi + '/fenxiao/fenxiaobanner.png',
        #  'type': 'html', 'url': 'https://mp.weixin.qq.com/s/7tNvqTjx1TaS_LnK8JXEPg'},
        # {'title': '小程序使用介绍', 'adurl': 'https://www.lianaizhuli.com/shouye/shiyongjieshaobanner.jpg',
        #  'type': 'ganhuo', 'url': 'cloud://lianaihuashu-086596.6c69-lianaihuashu-086596/shouye/shiyongjieshao.mp4',
        #  'duration': '04:04', 'direction': '0'},
        # {'title': '恋爱联盟招聘',
        #  'adurl': 'https://www.lianaizhuli.com/shouye/zhaopinbanner.jpg',
        #  'type': 'image', 'url': 'cloud://lianaihuashu-086596.6c69-lianaihuashu-086596/shouye/zhaopin1.jpg'},
        {'title': '和友商对比', 'adurl': wangzhi + '/shouye/lunbotu/WechatIMG43.jpeg',
         'type': 'html', 'url': 'https://mp.weixin.qq.com/s/xR2iH6bHkY9OUvRVYHWv9w'},
        {'title': '分手挽回', 'adurl': wangzhi + '/shouye/lunbotu/fenshouwanhui.png',
         'type': 'path', 'url': '/pages/sijiao',
         'data': {"url": "https://www.lianaizhuli.com/sijiao/1999.png", "title": "恋爱联盟分手挽回私教(送小程序终身会员)",
                  "id": "yusd3ntvgRLCNFpxKw", "image": "https://www.lianaizhuli.com/shouye/images/sijiao4.png",
                  "count": 7532}},
    ],
                               'tubiao': [{'title': '土味情话', 'image': wangzhi + '/shouye/tubiao/tuweiqinghua.png',
                                           'page': 'tuweiqinghualist'},
                                          {'title': '聊天实战', 'image': wangzhi + '/shouye/tubiao/liaomeitaolu.png',
                                           'page': 'liaomeishizhanlist'},
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
    sijiao = {'image': wangzhi + '/shouye/wenzi/sijiao.png', 'data': []}
    xinliceshi = {'image': wangzhi + '/shouye/wenzi/xinliceshi.png', 'data': []}
    search = {"query": {"match_all": {}}}
    Docs = es.search(index='kechenglist', doc_type='kechenglist', body=search, size=3)['hits']['hits']
    try:
        goumaidoc = es.get(index='kechenggoumai', doc_type='kechenggoumai', id=unionid)['_source']
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
        # doc['newimage'] = wangzhi + '/shouye/images/qingganbaike' + str(u + 1) + '.png'
        qingganbaike['data'].append(doc)
    Docs = es.search(index='liaomeishizhanlist', doc_type='liaomeishizhanlist', body=search, size=4)['hits']['hits']
    for u, doc in enumerate(Docs):
        doc = doc['_source']
        doc['newimage'] = doc['image']
        # doc['newimage'] = wangzhi + '/shouye/images/liaomeishizhan' + str(u + 1) + '.png'
        liaomeishizhan['data'].append(doc)
    Docs = es.search(index='sijiao', doc_type='sijiao', body=search, size=3)['hits']['hits']
    for u, doc in enumerate(Docs):
        doc = doc['_source']
        doc['newimage'] = doc['image']
        sijiao['data'].append(doc)
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
                               'sijiao': sijiao,
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
    doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
    doc = doc['_source']
    if doc['viptime'] > int(time.time()):
        return 1
    elif doc['vipdengji'] > 0:
        doc['vipdengji'] = 0
        es.index(index='userinfo', doc_type='userinfo', id=unionid, body=doc)
    if doc['tiyancishu'] > 0:
        doc['tiyancishu'] -= 1
        es.index(index='userinfo', doc_type='userinfo', id=unionid, body=doc)
        return 1
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
    except:
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
        encryptedData = params['encryptedData']
        jiemiiv = params['jiemiiv']
        system = params['system']
        options = params['options']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    apptype = 'app'
    if 'apptype' in params:
        apptype = params['apptype']
    nametype = 'lianaihuashuai'
    if 'nametype' in params:
        nametype = params['nametype']
    appid = xiaochengxus[nametype]['appid']
    secret = xiaochengxus[nametype]['secret']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = requests.get(url)
    response = response.json()
    userinfo['system'] = system
    openid = ''
    unionid = ''
    if 'openid' in response:
        openid = response['openid']
    elif 'openId' in response:
        openid = response['openId']
    if 'unionid' in response:
        unionid = response['unionid']
    elif 'unionId' in response:
        unionid = response['unionId']
    else:
        try:
            session_key = response['session_key']
            jiemidata = decryptweixin(encryptedData, session_key, jiemiiv)
            if 'unionId' in jiemidata:
                unionid = jiemidata['unionId']
            elif 'unionid' in jiemidata:
                unionid = jiemidata['unionid']
        except Exception as e:
            logger.error(e)
            unionid = openid
    try:
        if options['scene'] == 1129:
            return encrypt(json.dumps({'MSG': 'OK', 'data': {'unionid': unionid}}))
    except:
        logger.error(json.dumps(options, ensure_ascii=False))
        None
    userinfo['openid'] = openid
    if openid != unionid:
        userinfo['unionid'] = unionid
    # if 'query' in options and 'scene' in options['query']:
    #     shangji = options['query']['scene']
    #     try:
    #         newfenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
    #     except:
    #         shangshangji = ''
    #         try:
    #             newfenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=shangji)['_source']
    #             shangshangji = newfenxiao['shangji']
    #             newfenxiao['yijiyonghu'].insert(0,
    #                                             {'unionid': unionid, 'nickName': userinfo['nickName'],
    #                                              'avatarUrl': userinfo['avatarUrl'],
    #                                              'time': getTime()})
    #             es.index(index='fenxiao', doc_type='fenxiao', id=shangji, body=newfenxiao)
    #             if shangshangji != '':
    #                 try:
    #                     newfenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=shangshangji)['_source']
    #                     newfenxiao['erjiyonghu'].insert(0,
    #                                                     {'unionid': unionid, 'nickName': userinfo['nickName'],
    #                                                      'avatarUrl': userinfo['avatarUrl'],
    #                                                      'time': getTime()})
    #                     es.index(index='fenxiao', doc_type='fenxiao', id=shangshangji, body=newfenxiao)
    #                 except:
    #                     None
    #         except:
    #             None
    #         fenxiao = {'zongshouyi': 0.00, 'dingdan': [], 'ketixian': 0.00, 'yitixian': 0.00,
    #                    'yijiyonghu': [], 'erjiyonghu': [], 'tixianjilu': [], 'shangji': shangji,
    #                    'shangshangji': shangshangji}
    #         es.index(index='fenxiao', doc_type='fenxiao', id=unionid, body=fenxiao)
    try:
        uniondoc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
        uniondoc.update(userinfo)
        userinfo = uniondoc
    except:
        None
    if 'addtime' not in userinfo:
        userinfo['addtime'] = getTime()
        userinfo['vipdengji'] = 0
        userinfo['viptime'] = int(time.time()) + viptime[0]
        userinfo['tiyancishu'] = 0
        userinfo['sijiaotime'] = 0
        userinfo['xiaofeicishu'] = 0
        userinfo['xiaofeizonge'] = 0
        userinfo['apptype'] = apptype
        userinfo['nametype'] = nametype
    if 'options' not in userinfo:
        userinfo['options'] = options
    es.index(index='userinfo', doc_type='userinfo', id=unionid, body=userinfo)
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
        userinfodoc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
        userinfodoc.update(resdata)
        resdata = userinfodoc
    except:
        resdata['addtime'] = getTime()
        resdata['vipdengji'] = 0
        resdata['viptime'] = int(time.time()) + viptime[0]
        resdata['tiyancishu'] = 0
        resdata['sijiaotime'] = 0
        resdata['xiaofeicishu'] = 0
        resdata['xiaofeizonge'] = 0
        resdata['apptype'] = apptype
        resdata['nametype'] = 'fuwuhao'
    es.index(index='userinfo', doc_type='userinfo', id=unionid, body=resdata)
    return encrypt(json.dumps({'MSG': 'OK', 'data': {'unionid': unionid}}))


@app.route(apiqianzui + "getAppunionid", methods=["POST"])
def getAppunionid():
    try:
        params = json.loads(decrypt(request.stream.read()))
        code = params['code']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    apptype = 'app'
    if 'apptype' in params:
        apptype = params['apptype']
    nametype = 'lianaituodanhuashu'
    if 'nametype' in params:
        nametype = params['nametype']
    appappid = apps[nametype]['appid']
    appsecret = apps[nametype]['secret']
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + appappid + '&secret=' + appsecret + '&code=' + code + '&grant_type=authorization_code'
    response = requests.get(url)
    response = response.json()
    unionid = response['unionid']
    yingyongid = response['openid']
    url = 'https://api.weixin.qq.com/sns/userinfo?access_token=' + response['access_token'] + '&openid=' + yingyongid
    response = requests.get(url)
    userinfo = json.loads(bytes(response.text, encoding='ISO-8859-1').decode('utf8'))
    userinfo['yingyongid'] = yingyongid
    userinfo.pop('openid')
    try:
        opendoc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
        opendoc.update(userinfo)
        opendoc['apptype'] = apptype
        es.index(index='userinfo', doc_type='userinfo', id=unionid, body=opendoc)
    except:
        if 'addtime' not in userinfo:
            userinfo['addtime'] = getTime()
            userinfo['vipdengji'] = 0
            userinfo['viptime'] = int(time.time()) + viptime[0]
            userinfo['tiyancishu'] = 0
            userinfo['sijiaotime'] = 0
            userinfo['xiaofeicishu'] = 0
            userinfo['xiaofeizonge'] = 0
            userinfo['apptype'] = apptype
            userinfo['nametype'] = nametype
            es.index(index='userinfo', doc_type='userinfo', id=unionid, body=userinfo)
    unionid_token = mydb['unionid_token']
    token = str(int(time.time()))
    try:
        unionid_token.remove({'_id': unionid})
    except:
        None
    unionid_token.update_one({'_id': unionid}, {"$set": {'_id': unionid, 'unionid': unionid, 'token': token}}, True)
    return encrypt(json.dumps({'MSG': 'OK', 'data': {'unionid': unionid, 'token': token, 'userinfo': userinfo}}))


@app.route(apiqianzui + "checkUnionid", methods=["POST"])
def checkUnionid():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        userinfo = params['userinfo']
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
        doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
        newdoc = doc['_source']
        newdoc.update(userinfo)
        newdoc['system'] = system
        es.index(index='userinfo', doc_type='userinfo', id=unionid, body=newdoc)
        if 'unionid' in newdoc and 'openid' in newdoc:
            return encrypt(json.dumps({'MSG': 'YES'}))
        else:
            return encrypt(json.dumps({'MSG': 'NO'}))
    except:
        return encrypt(json.dumps({'MSG': 'NO'}))


@app.route(apiqianzui + "checkAppunionid", methods=["POST"])
def checkAppunionid():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        token = params['token']
    except Exception as e:
        logger.error(e)
        return encrypt(json.dumps({'MSG': 'NO'}))
    if len(unionid) == 0 or len(token) == 0:
        return encrypt(json.dumps({'MSG': 'NO'}))
    unionid_token = mydb['unionid_token']
    try:
        results = unionid_token.find_one({'_id': unionid})
        if results['token'] == token:
            return encrypt(json.dumps({'MSG': 'YES'}))
    except:
        return encrypt(json.dumps({'MSG': 'NO'}))
    return encrypt(json.dumps({'MSG': 'NO'}))


@app.route(apiqianzui + "getTiyancishu", methods=["POST"])
def getTiyancishu():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return encrypt(json.dumps({'MSG': 'NO'}))
    doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
    return encrypt(json.dumps(
        {'MSG': 'OK', 'tiyancishu': doc['tiyancishu'], 'sousuocishu': tiyancishu, 'vipdengji': doc['vipdengji'],
         'wenhouyu': 'HI，欢迎您~'}))


@app.route(apiqianzui + "addTiyancishu", methods=["POST"])
def addTiyancishu():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return encrypt(json.dumps({'MSG': 'NO'}))
    adduserhis({'time': getTime(), 'event': 'addTiyancishu', 'detail': params})
    try:
        doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
        doc['tiyancishu'] += tiyancishu
        es.index(index='userinfo', doc_type='userinfo', id=unionid, body=doc)
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "searchLiaomeihuashu", methods=["POST"])
def searchLiaomeihuashu():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        query = params['query']
        scroll = params['scroll']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    check_user_res = check_user(unionid)
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
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    check_user_res = check_user(unionid)
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
    adduserhis({'time': getTime(), 'event': 'getXingxiangjiansheList', 'detail': params})
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
        logger.error(json.dumps(params, ensure_ascii=False))
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
    adduserhis({'time': getTime(), 'event': 'getLiaomeishizhanList', 'detail': params})
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
        logger.error(json.dumps(params, ensure_ascii=False))
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getLiaomeishizhan', 'detail': params})
    doc = es.get(index='liaomeishizhanlist', doc_type='liaomeishizhanlist', id=liaomeishizhanid)['_source']
    doc['count'] += 1
    es.index(index='liaomeishizhanlist', doc_type='liaomeishizhanlist', id=liaomeishizhanid, body=doc)
    doc = es.get(index='liaomeishizhan', doc_type='liaomeishizhan', id=liaomeishizhanid)['_source']
    return encrypt(json.dumps({'MSG': 'OK', 'data': doc}))


@app.route(apiqianzui + "getSijiaoList", methods=["POST"])
def getSijiaoList():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getSijiaoList', 'detail': params})
    retdata = []
    search = {"query": {"match_all": {}}}
    Docs = es.search(index='sijiao', doc_type='sijiao', body=search, size=10000)
    Docs = Docs['hits']['hits']
    for doc in Docs:
        retdata.append(doc['_source'])
    return encrypt(json.dumps({'MSG': 'OK', 'data': retdata}))


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


@app.route(apiqianzui + "searchWenzhangList", methods=["POST"])
def searchWenzhangList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        scroll = params['scroll']
        query = params['query']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'searchWenzhangList', 'detail': params})
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
    adduserhis({'time': getTime(), 'event': 'getTuweiqinghuaList', 'detail': params})
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


@app.route(apiqianzui + "getPhoneNumber", methods=["POST"])
def getPhoneNumber():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        js_code = params['jsCode']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    nametype = 'lianaihuashuai'
    if 'nametype' in params:
        nametype = params['nametype']
    appid = xiaochengxus[nametype]['appid']
    secret = xiaochengxus[nametype]['secret']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = requests.get(url)
    response = response.json()
    userphone = decryptweixin(params['encryptedData'], response['session_key'], params['iv'])
    userphone.pop('watermark')
    doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
    userphone.update(doc['_source'])
    es.index(index='userinfo', doc_type='userinfo', id=unionid, body=userphone)
    return encrypt(json.dumps({'MSG': 'OK', 'data': {'unionid': response['unionid']}}))


@app.route(apiqianzui + "getTequan", methods=["POST"])
def getTequan():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
    return encrypt(json.dumps({'MSG': 'OK', 'vipdengji': doc['_source']['vipdengji'],
                               'viptime': time.strftime("%Y-%m-%d %H:%M:%S",
                                                        time.localtime(doc['_source']['viptime']))}))


@app.route(apiqianzui + "getJifen", methods=["POST"])
def getJifen():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
    return encrypt(json.dumps({'MSG': 'OK', 'data': {'vipdengji': doc['_source']['vipdengji'],
                                                     'jifen': int(doc['_source']['xiaofeizonge'] * 0.01),
                                                     'wenhouyu': 'HI，欢迎您~'}}))


@app.route(apiqianzui + "getDingdan", methods=["POST"])
def getDingdan():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    try:
        doc = es.get(index='userzhifu', doc_type='userzhifu', id=unionid)
        retdata = doc['_source']['zhifudata']
        for i in range(len(retdata)):
            retdata[i]['attach'] = json.loads(retdata[i]['attach'])
            if 'openid' in retdata[i]['attach']:
                retdata[i]['attach'].pop('openid')
            if 'unionid' in retdata[i]['attach']:
                retdata[i]['attach'].pop('unionid')
            retdata[i]['time_end'] = retdata[i]['time_end'][:4] + '-' + retdata[i]['time_end'][4:6] + '-' + retdata[i][
                                                                                                                'time_end'][
                                                                                                            6:8] + ' ' + \
                                     retdata[i]['time_end'][8:10] + ':' + retdata[i]['time_end'][10:12] + ':' + \
                                     retdata[i]['time_end'][-2:]
        return encrypt(json.dumps({'MSG': 'OK', 'data': retdata}))
    except:
        return encrypt(json.dumps({'MSG': 'OK', 'data': []}))


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
    adduserhis({'time': getTime(), 'event': 'getQingganbaike', 'detail': params})
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
    adduserhis({'time': getTime(), 'event': 'getQingganbaikeList', 'detail': params})
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
        logger.error(json.dumps(params, ensure_ascii=False))
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
    adduserhis({'time': getTime(), 'event': 'getWendaList', 'detail': params})
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
        wendaid = params['wendaid']
    except Exception as e:
        logger.error(json.dumps(params, ensure_ascii=False))
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
    adduserhis({'time': getTime(), 'event': 'getXinliceshiList', 'detail': params})
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
        ceshiid = int(params['ceshiid'])
    except Exception as e:
        logger.error(json.dumps(params, ensure_ascii=False))
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
        newdoc = es.get(index='dianzanshoucang', doc_type='dianzanshoucang', id=unionid)['_source']
        flag = 1
        for u, newwendang in enumerate(newdoc['data']):
            if newwendang['docid'] == docid and newwendang['doctype'] == doctype:
                newdoc['data'][u] = wendang
                flag = 0
                break
        if flag: newdoc['data'].append(wendang)
        es.index(index='dianzanshoucang', doc_type='dianzanshoucang', id=unionid,
                 body=newdoc)
    except:
        newdoc = [wendang]
        es.index(index='dianzanshoucang', doc_type='dianzanshoucang', id=unionid,
                 body={'data': newdoc})
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "getDianzanshoucangList", methods=["POST"])
def getDianzanshoucangList():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getDianzanshoucangList', 'detail': params})
    retdata = []
    try:
        doc = es.get(index='dianzanshoucang', doc_type='dianzanshoucang', id=unionid)['_source']
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
    adduserhis({'time': getTime(), 'event': 'getDianzanshoucang', 'detail': params})
    dianzan = 0
    shoucang = 0
    try:
        doc = es.get(index='dianzanshoucang', doc_type='dianzanshoucang', id=unionid)['_source']
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
    adduserhis({'time': getTime(), 'event': 'setDianzanshoucang', 'detail': params})
    es.index(index='dianzanshoucang', doc_type='dianzanshoucang', id=unionid, body={'data': DianzanshoucangList})
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "getIoswenan", methods=["POST"])
def getIoswenan():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    return encrypt(json.dumps({'MSG': 'OK', 'data': ioswenan}))


@app.route(apiqianzui + "getJiagelist", methods=["POST"])
def getJiagelist():
    try:
        params = json.loads(decrypt(request.stream.read()))
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    jiagelist = [{'jiage': total_fees[0], 'miaoshu': '非会员'},
                 {'jiage': total_fees[1], 'miaoshu': '终身会员'},
                 {'jiage': total_fees[2], 'miaoshu': '分手挽回(送终身会员)'},
                 {'jiage': total_fees[3], 'miaoshu': '私教1个月(送终身会员)'},
                 {'jiage': total_fees[4], 'miaoshu': '私教3个月(送终身会员)'},
                 {'jiage': total_fees[5], 'miaoshu': '私教1年(送终身会员)'},
                 {'jiage': total_fees[6], 'miaoshu': '私教终身(送终身会员)'}]
    return encrypt(json.dumps({'MSG': 'OK', 'jiagelist': jiagelist}))


@app.route(apiqianzui + "getFenxiao", methods=["POST"])
def getFenxiao():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    adduserhis({'time': getTime(), 'event': 'getFenxiao', 'detail': params})
    if len(unionid) < 10: return json.dumps({'MSG': '警告！非法入侵！！！'})
    try:
        fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
    except:
        fenxiao = {'zongshouyi': 0.00, 'dingdan': [], 'ketixian': 0.00, 'yitixian': 0.00,
                   'yijiyonghu': [], 'erjiyonghu': [], 'tixianjilu': [], 'shangji': '', 'shangshangji': ''}
        es.index(index='fenxiao', doc_type='fenxiao', id=unionid, body=fenxiao)
    jintian = time.strftime("%Y-%m-%d", time.localtime())
    fenxiao['banner'] = 'https://www.lianaizhuli.com/fenxiao/fenxiaobanner.png'
    fenxiao['xiangqing'] = 'https://www.lianaizhuli.com/fenxiao/fenxiaoguize.png'
    fenxiao['wenan'] = '①女生回了一句话 ②你恐惧回复不好 ③复制粘贴在这里试试？'
    fenxiao['tixiantixing'] = '提现金额大于1.00元，不超过200.00元，将以微信红包形式发给你的微信，在深圳宇子科技公众号消息里面，提现成功后请及时领取以免逾期，每天可提现10次。'
    fenxiao['haibaoming'] = '1'
    if len(fenxiao['yijiyonghu']) >= 30:
        fenxiao['jibie'] = '超级推广员'
        fenxiao['yijibili'] = '40%'
        fenxiao['erjibili'] = '10%',
    elif len(fenxiao['yijiyonghu']) >= 10:
        fenxiao['jibie'] = '高级推广员'
        fenxiao['yijibili'] = '30%'
        fenxiao['erjibili'] = '8%',
    elif len(fenxiao['yijiyonghu']) >= 3:
        fenxiao['jibie'] = '中级推广员'
        fenxiao['yijibili'] = '20%'
        fenxiao['erjibili'] = '6%',
    else:
        fenxiao['jibie'] = '初级推广员'
        fenxiao['yijibili'] = '10%'
        fenxiao['erjibili'] = '4%',
    fenxiao['zongshouyi'] = str(round(fenxiao['zongshouyi'], 2))
    fenxiao['ketixian'] = str(round(fenxiao['ketixian'], 2))
    fenxiao['yitixian'] = str(round(fenxiao['yitixian'], 2))
    fenxiao['yijiyonghu'] = len(fenxiao['yijiyonghu'])
    fenxiao['erjiyonghu'] = len(fenxiao['erjiyonghu'])
    fenxiao['jintianshouyi'] = 0.00
    fenxiao['jintiandingdan'] = 0
    for dingdan in fenxiao['dingdan']:
        if dingdan['time'][:10] == jintian:
            fenxiao['jintianshouyi'] += dingdan['shouyi']
            fenxiao['jintiandingdan'] += 1
    fenxiao['jintianshouyi'] = str(round(fenxiao['jintianshouyi'], 2))
    return encrypt(json.dumps({'MSG': 'OK', 'data': fenxiao}))


def shengchengtupian(haibaoming, yonghuming, unionid):
    yonghuming = yonghuming[:10]
    newwidth = 500
    haibao = Image.open('/home/ubuntu/data/lianaihuashu/data/opendata/fenxiao/' + haibaoming + '.png')
    haibaow, haibaoh = haibao.size
    haibao = haibao.resize((newwidth, int(haibaoh / haibaow * newwidth)), Image.BILINEAR)
    haibaoh = int(haibaoh / haibaow * newwidth)
    imgtou = Image.new('RGBA', (newwidth, 100), 'white')
    draw = ImageDraw.Draw(imgtou)  # 生成绘制对象draw
    big = 20
    typeface = ImageFont.truetype('simkai.ttf', big)
    text1 = "Hi，我是" + yonghuming
    text2 = "推荐您这款超级棒的产品"
    text3 = "（长按识别底部小程序码，助您快速脱单）"
    draw.text(((newwidth - len(text1) * big) / 2, 10), text1, fill='#ff7e00', font=typeface)
    draw.text(((newwidth - len(text2) * big) / 2, 20 + big), text2, fill='#ff7e00', font=typeface)
    draw.text(((newwidth - len(text3) * big) / 2, 30 + 2 * big), text3, fill='#1861ce', font=typeface)
    xcxmk = Image.new('RGBA', (newwidth, 200), 'white')
    accessToken = Basic().get_access_token('xcx')
    postUrl = "https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=%s" % accessToken
    postJson = {"scene": unionid, 'width': 280}
    response = requests.post(postUrl, data=json.dumps(postJson))
    xcxm = Image.open(BytesIO(response.content))
    xcxm = xcxm.resize((100, 100), Image.BILINEAR)
    xcxmk.paste(xcxm, (200, 50))
    newimg = Image.new(haibao.mode, (newwidth, haibaoh + 300))
    newimg.paste(imgtou, (0, 0))
    newimg.paste(haibao, (0, 100))
    newimg.paste(xcxmk, (0, 100 + haibaoh))
    output_buffer = BytesIO()
    newimg.save(output_buffer, format='png')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str


@app.route(apiqianzui + "getHaibaobase64", methods=["POST"])
def getHaibaobase64():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        imgname = params['imgname']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    userinfodoc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
    haibao = str(shengchengtupian(imgname, userinfodoc['nickName'], unionid), encoding='utf8')
    return encrypt(json.dumps({'MSG': 'OK', 'data': haibao}))


@app.route(apiqianzui + "getHaibao", methods=["POST"])
def getHaibao():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        imgname = params['imgname']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    userinfodoc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
    yonghuming = userinfodoc['nickName'][:10]
    newwidth = 500
    haibao = Image.open('/home/ubuntu/data/lianaihuashu/data/opendata/fenxiao/' + imgname + '.png')
    haibaow, haibaoh = haibao.size
    haibao = haibao.resize((newwidth, int(haibaoh / haibaow * newwidth)), Image.BILINEAR)
    haibaoh = int(haibaoh / haibaow * newwidth)
    imgtou = Image.new('RGBA', (newwidth, 100), 'white')
    draw = ImageDraw.Draw(imgtou)  # 生成绘制对象draw
    big = 20
    typeface = ImageFont.truetype('simkai.ttf', big)
    text1 = "Hi，我是" + yonghuming
    text2 = "推荐您这款超级棒的产品"
    text3 = "（长按识别底部小程序码，助您快速脱单）"
    draw.text(((newwidth - len(text1) * big) / 2, 10), text1, fill='#ff7e00', font=typeface)
    draw.text(((newwidth - len(text2) * big) / 2, 20 + big), text2, fill='#ff7e00', font=typeface)
    draw.text(((newwidth - len(text3) * big) / 2, 30 + 2 * big), text3, fill='#1861ce', font=typeface)
    xcxmk = Image.new('RGBA', (newwidth, 200), 'white')
    accessToken = Basic().get_access_token('xcx')
    postUrl = "https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=%s" % accessToken
    postJson = {"scene": unionid, 'width': 280}
    response = requests.post(postUrl, data=json.dumps(postJson))
    xcxm = Image.open(BytesIO(response.content))
    xcxm = xcxm.resize((100, 100), Image.BILINEAR)
    xcxmk.paste(xcxm, (200, 50))
    newimg = Image.new(haibao.mode, (newwidth, haibaoh + 300))
    newimg.paste(imgtou, (0, 0))
    newimg.paste(haibao, (0, 100))
    newimg.paste(xcxmk, (0, 100 + haibaoh))
    newimg.save('/home/ubuntu/data/lianaihuashu/data/opendata/fenxiao/' + unionid + imgname + '.png')
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "deleteHaibao", methods=["POST"])
def deleteHaibao():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        imgname = params['imgname']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    try:
        os.remove('/home/ubuntu/data/lianaihuashu/data/opendata/fenxiao/' + unionid + imgname + '.png')
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK'}))


@app.route(apiqianzui + "getFenxiaodingdan", methods=["POST"])
def getFenxiaodingdan():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    dingdan = []
    try:
        fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
        dingdan = fenxiao['dingdan']
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK', 'data': dingdan}))


@app.route(apiqianzui + "getYijiyonghu", methods=["POST"])
def getYijiyonghu():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    yijiyonghu = []
    try:
        fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
        yijiyonghu = fenxiao['yijiyonghu']
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK', 'data': yijiyonghu}))


@app.route(apiqianzui + "getFenxiaoyonghu", methods=["POST"])
def getFenxiaoyonghu():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    fenxiaoyonghu = []
    try:
        fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
        fenxiaoyonghu = fenxiao['yijiyonghu'] + fenxiao['erjiyonghu']
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK', 'data': fenxiaoyonghu}))


@app.route(apiqianzui + "getTixianjilu", methods=["POST"])
def getTixianjilu():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    tixianjilu = []
    try:
        fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
        tixianjilu = fenxiao['tixianjilu']
    except:
        None
    return encrypt(json.dumps({'MSG': 'OK', 'data': tixianjilu}))


def chaxundingdan(dingdanhao, appid):
    chaxunurl = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/gethbinfo'
    chaxundict = {
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
        'mch_billno': dingdanhao,
        'mch_id': mch_id,
        'appid': appid,
        'bill_type': 'MCHT',
    }
    stringA = '&'.join(["{0}={1}".format(k, chaxundict.get(k)) for k in sorted(chaxundict)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    chaxundict['sign'] = sign
    ssh_keys_path = '/home/ubuntu/data/lianaihuashu/data'
    weixinapiclient_cert = os.path.join(ssh_keys_path, "apiclient_cert.pem")
    weixinapiclient_key = os.path.join(ssh_keys_path, "apiclient_key.pem")
    result = requests.post(chaxunurl, data=dict_to_xml(chaxundict).encode('utf8'),
                           headers={'Content-Type': 'application/xml'},
                           cert=(weixinapiclient_cert, weixinapiclient_key), verify=True)
    result = xml_to_dict(result.content)
    return result


@app.route(apiqianzui + "tiXian", methods=["POST"])
def tiXian():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        tixianjine = params['tixianjine']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})

    if unionid in tixianunionid:
        return encrypt(json.dumps({'MSG': 'FREQ_LIMIT'}))
    else:
        if unionid in tixianunionid_time and int(time.time()) - tixianunionid_time[unionid] <= 10:
            return encrypt(json.dumps({'MSG': 'FREQ_LIMIT'}))
        tixianunionid_time[unionid] = int(time.time())
    tixianunionid[unionid] = int(time.time())
    try:
        userdoc = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']
        try:
            tixianjine = int(float(tixianjine.strip()) * 100)
            ketixian = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']['ketixian']
            if tixianjine < 100 or tixianjine > 20000 or tixianjine > ketixian * 100:
                tixianunionid.pop(unionid)
                return encrypt(json.dumps({'MSG': 'NO'}))
        except:
            tixianunionid.pop(unionid)
            return encrypt(json.dumps({'MSG': 'NO'}))
        try:
            fwhid = userdoc['fwhid']
        except Exception as e:
            tixianunionid.pop(unionid)
            return encrypt(json.dumps({'MSG': 'NOFWHID'}))
        tixianurl = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
        dingdanhao = str(int(time.time())) + ''.join(random.sample(string.ascii_letters + string.digits, 18))
        tixiandict = {
            'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
            'mch_billno': dingdanhao,
            'mch_id': mch_id,
            'wxappid': 'wx2cc1bc5a412d44d2',
            'send_name': '恋爱话术',
            're_openid': fwhid,
            'total_amount': tixianjine,
            'total_num': 1,
            'wishing': '祝您生活愉快，天天开心！',
            'client_ip': '182.254.227.188',
            'act_name': '推广佣金',
            'remark': '走向人生巅峰',
            'scene_id': 'PRODUCT_5',
        }
        stringA = '&'.join(["{0}={1}".format(k, tixiandict.get(k)) for k in sorted(tixiandict)])
        stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
        sign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
        tixiandict['sign'] = sign
        ssh_keys_path = '/home/ubuntu/data/lianaihuashu/data'
        weixinapiclient_cert = os.path.join(ssh_keys_path, "apiclient_cert.pem")
        weixinapiclient_key = os.path.join(ssh_keys_path, "apiclient_key.pem")
        result = requests.post(tixianurl, data=dict_to_xml(tixiandict).encode('utf8'),
                               headers={'Content-Type': 'application/xml'},
                               cert=(weixinapiclient_cert, weixinapiclient_key), verify=True)
        result = xml_to_dict(result.content)
        if result['return_code'] == 'SUCCESS':
            if result['err_code'] == 'NO_AUTH' or result['err_code'] == 'ILLEGAL_APPID' or result[
                'err_code'] == 'MONEY_LIMIT' or \
                    result['err_code'] == 'SEND_FAILED' or result['err_code'] == 'FATAL_ERROR' or result[
                'err_code'] == 'CA_ERROR' or result[
                'err_code'] == 'SIGN_ERROR' or result['err_code'] == 'XML_ERROR' or result[
                'err_code'] == 'FREQ_LIMIT' or \
                    result[
                        'err_code'] == 'API_METHOD_CLOSED' or \
                    result['err_code'] == 'NOTENOUGH' or result['err_code'] == 'OPENID_ERROR' or result[
                'err_code'] == 'MSGAPPID_ERROR' or result['err_code'] == 'ACCEPTMODE_ERROR' or result[
                'err_code'] == 'PARAM_ERROR' or \
                    result['err_code'] == 'SENDAMOUNT_LIMIT':
                tixianunionid.pop(unionid)
                return encrypt(json.dumps({'MSG': 'ERROR'}))
            if result['err_code'] == 'SENDNUM_LIMIT':
                tixianunionid.pop(unionid)
                return encrypt(json.dumps({'MSG': 'SENDNUM_LIMIT'}))
            if result['err_code'] == 'RCVDAMOUNT_LIMIT':
                tixianunionid.pop(unionid)
                return encrypt(json.dumps({'MSG': 'RCVDAMOUNT_LIMIT'}))
            if result['err_code'] == 'SUCCESS':
                fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
                fenxiao['tixianjilu'].insert(0, {'tixianjine': tixianjine, 'time': getTime()})
                fenxiao['ketixian'] -= tixianjine * 0.01
                es.index(index='fenxiao', doc_type='fenxiao', id=unionid, body=fenxiao)
                adduserhis({'time': getTime(), 'event': 'tiXian', 'detail': params})
                tixianunionid.pop(unionid)
                return encrypt(json.dumps({'MSG': 'YES', 'data': str(round(tixianjine * 0.01, 2))}))
            if result['result_code'] == 'FAIL' or result['err_code'] == 'SYSTEMERROR' or result[
                'err_code'] == 'PROCESSING':
                appid = lianailianmengappid
                if 'nametype' in params:
                    if params['nametype'] == 'lianaihuashu':
                        appid = lianaihuashuappid
                    elif params['nametype'] == 'tuodanhuashu':
                        appid = tuodanhuashuappid
                    elif params['nametype'] == 'galiaojiuxing':
                        appid = galiaojiuxingappid
                    elif params['nametype'] == 'liaotianhuashu':
                        appid = liaotianhuashuappid
                    elif params['nametype'] == 'dailiaohuashu':
                        appid = dailiaohuashuappid
                while 1:
                    chaxunret = chaxundingdan(dingdanhao, appid)
                    try:
                        if chaxunret['return_code'] == 'SUCCESS' and chaxunret['result_code'] == 'SUCCESS':
                            if chaxunret['status'] == 'SENT' or chaxunret['status'] == 'RECEIVED':
                                fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
                                fenxiao['tixianjilu'].insert(0, {'tixianjine': tixianjine, 'time': getTime()})
                                fenxiao['ketixian'] -= tixianjine * 0.01
                                es.index(index='fenxiao', doc_type='fenxiao', id=unionid, body=fenxiao)
                                adduserhis({'time': getTime(), 'event': 'tiXian', 'detail': params})
                                tixianunionid.pop(unionid)
                                return encrypt(json.dumps({'MSG': 'YES', 'data': str(round(tixianjine * 0.01, 2))}))
                            if chaxunret['status'] == 'FAILED' or chaxunret['status'] == 'RFUND_ING' or chaxunret[
                                'status'] == 'REFUND':
                                tixianunionid.pop(unionid)
                                return encrypt(json.dumps({'MSG': 'FAIL'}))
                    except:
                        None
                    time.sleep(1)
                None
        else:
            tixianunionid.pop(unionid)
            return encrypt(json.dumps({'MSG': 'ERROR'}))
    except:
        tixianunionid.pop(unionid)


@app.route(apiqianzui + "get_prepay_id", methods=["POST"])
def get_prepay_id():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        zhifutype = int(params['zhifutype'])
        detail = params['detail']
        apptype = params['apptype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    if apptype == 'weixin':
        nametype = 'lianaihuashuai'
        if 'nametype' in params:
            nametype = params['nametype']
        nowappid = xiaochengxus[nametype]['appid']
        trade_type = 'JSAPI'
        openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['openid']
    elif apptype == 'fwh':
        nametype = 'fuwhao'
        nowappid = fuwuhaoappid
        trade_type = 'JSAPI'
        openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['fwhid']
    else:
        nametype = 'lianaituodanhuashu'
        if 'nametype' in params:
            nametype = params['nametype']
        nowappid = apps[nametype]['appid']
        trade_type = 'APP'
        openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['yingyongid']
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    prepaydata = {
        'appid': nowappid,
        'mch_id': mch_id,
        'nonce_str': ''.join(random.sample(string.ascii_letters + string.digits, 32)),
        'device_info': nametype,
        'body': detail,
        'attach': json.dumps({'zhifutype': zhifutype, 'detail': detail, 'unionid': unionid}, ensure_ascii=False),
        'out_trade_no': str(int(time.time())) + '_' + str((random.randint(1000000, 9999999))),
        'total_fee': total_fees[zhifutype],
        'spbill_create_ip': request.remote_addr,
        'notify_url': wangzhi + apiqianzui + "paynotify",
        'trade_type': trade_type,
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
            'partnerid': mch_id,
            'prepayid': prepay_id,
            'package': 'Sign=WXPay',
            'noncestr': result['nonce_str'],
            'timestamp': str(int(time.time())),
        }
    stringA = '&'.join(["{0}={1}".format(k, paySign_data.get(k)) for k in sorted(paySign_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    if apptype == 'weixin' or apptype == 'fwh':
        paySign_data['paySign'] = paySign
    else:
        paySign_data['sign'] = paySign
    # doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
    # doc = doc['_source']
    # if 'phoneNumber' not in doc:
    #     return encrypt(json.dumps({'MSG': 'nophoneNumber', 'data': paySign_data}))
    return encrypt(json.dumps({'MSG': 'OK', 'data': paySign_data}))


@app.route(apiqianzui + "paynotify", methods=["POST"])
def paynotify():
    zhifures = xml_to_dict(request.stream.read().decode('utf8'))
    sign = zhifures['sign']
    zhifures.pop('sign')
    stringA = '&'.join(["{0}={1}".format(k, zhifures.get(k)) for k in sorted(zhifures)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest().upper()
    if sign != paySign:
        return dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'})
    unionid = json.loads(zhifures['attach'])['unionid']
    zhifudata = [zhifures]
    isnew = 1
    flag = 1
    try:
        doc = es.get(index='userzhifu', doc_type='userzhifu', id=unionid)
        isnew = 0
        for line in doc['_source']['zhifudata']:
            if line['transaction_id'] == zhifudata[0]['transaction_id']:
                flag = 0
        if flag:
            zhifudata += doc['_source']['zhifudata']
    except:
        None
    if isnew or (isnew == 0 and flag == 1):
        es.index(index='userzhifu', doc_type='userzhifu', id=unionid,
                 body={'unionid': unionid, 'zhifudata': zhifudata, 'updatatime': zhifures['time_end']})
        doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
        userdoc = doc['_source']
        zhifures['total_fee'] = int(zhifures['total_fee'])
        try:
            zhifutype = int(json.loads(zhifures['attach'])['zhifutype'])
            if userdoc['vipdengji'] < zhifutype:
                userdoc['vipdengji'] = zhifutype
            if userdoc['viptime'] < int(time.time()):
                userdoc['viptime'] = int(time.time()) + viptime[zhifutype]
            else:
                userdoc['viptime'] += viptime[zhifutype]
            if userdoc['sijiaotime'] < int(time.time()):
                userdoc['sijiaotime'] = int(time.time()) + sijiaotime[zhifutype]
            else:
                userdoc['sijiaotime'] += sijiaotime[zhifutype]
            userdoc['xiaofeicishu'] += 1
            userdoc['xiaofeizonge'] += zhifures['total_fee']
            es.index(index='userinfo', doc_type='userinfo', id=unionid, body=userdoc)
            if zhifutype > 1:
                search = {"query": {"match_all": {}}}
                kechengDocs = es.search(index='kechenglist', doc_type='kechenglist', body=search)['hits']['hits']
                try:
                    goumaidoc = es.get(index='kechenggoumai', doc_type='kechenggoumai', id=unionid)['_source']
                    goumaidoc['data'] = json.loads(goumaidoc['data'])
                    for kecheng in kechengDocs:
                        kecheng = kecheng['_source']
                        goumaidoc['data'][kecheng['id']] = 1
                except:
                    goumaidoc = {}
                    goumaidoc['unionid'] = unionid
                    goumaidoc['data'] = {}
                    for kecheng in kechengDocs:
                        kecheng = kecheng['_source']
                        goumaidoc['data'][kecheng['id']] = 1
                goumaidoc['data'] = json.dumps(goumaidoc['data'], ensure_ascii=False)
                es.index(index='kechenggoumai', doc_type='kechenggoumai', id=unionid, body=goumaidoc)
        except Exception as e:
            logger.error(e)
        # try:
        #     newdoc = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
        #     shangji = newdoc['shangji']
        #     shangshangji = newdoc['shangshangji']
        #     if shangji != '':
        #         try:
        #             fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=shangji)['_source']
        #             yijibili = 0.1
        #             if len(fenxiao['yijiyonghu']) >= 30:
        #                 yijibili = 0.4
        #             elif len(fenxiao['yijiyonghu']) >= 10:
        #                 yijibili = 0.3
        #             elif len(fenxiao['yijiyonghu']) >= 3:
        #                 yijibili = 0.2
        #             newzhifu = {}
        #             newzhifu['yonghuming'] = userdoc['nickName']
        #             newzhifu['shangpinming'] = json.loads(zhifures['attach'])['detail']
        #             newzhifu['time'] = getTime()
        #             newzhifu['total_fee'] = zhifures['total_fee'] * 0.01
        #             newzhifu['shouyi'] = zhifures['total_fee'] * 0.00994 * yijibili
        #             fenxiao['dingdan'].insert(0, newzhifu)
        #             fenxiao['zongshouyi'] += zhifures['total_fee'] * 0.00994 * yijibili
        #             fenxiao['ketixian'] += zhifures['total_fee'] * 0.00994 * yijibili
        #             es.index(index='fenxiao', doc_type='fenxiao', id=shangji, body=fenxiao)
        #         except:
        #             None
        #     if shangshangji != '':
        #         try:
        #             fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=shangshangji)['_source']
        #             yijibili = 0.04
        #             if len(fenxiao['yijiyonghu']) >= 30:
        #                 yijibili = 0.1
        #             elif len(fenxiao['yijiyonghu']) >= 10:
        #                 yijibili = 0.08
        #             elif len(fenxiao['yijiyonghu']) >= 3:
        #                 yijibili = 0.06
        #             newzhifu = {}
        #             newzhifu['yonghuming'] = userdoc['nickName']
        #             newzhifu['shangpinming'] = json.loads(zhifures['attach'])['detail']
        #             newzhifu['time'] = getTime()
        #             newzhifu['total_fee'] = zhifures['total_fee'] * 0.01
        #             newzhifu['shouyi'] = zhifures['total_fee'] * 0.00994 * yijibili
        #             fenxiao['dingdan'].insert(0, newzhifu)
        #             fenxiao['zongshouyi'] += zhifures['total_fee'] * 0.00994 * yijibili
        #             fenxiao['ketixian'] += zhifures['total_fee'] * 0.00994 * yijibili
        #             es.index(index='fenxiao', doc_type='fenxiao', id=shangshangji, body=fenxiao)
        #         except:
        #             None
        # except:
        #     None
    return dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'})


@app.route(apiqianzui + "get_kechengprepay_id", methods=["POST"])
def get_kechengprepay_id():
    try:
        params = json.loads(decrypt(request.stream.read()))
        unionid = params['unionid']
        kechengid = params['kechengid']
        detail = params['detail']
        apptype = params['apptype']
    except Exception as e:
        logger.error(e)
        return json.dumps({'MSG': '警告！非法入侵！！！'})
    if apptype == 'weixin':
        nametype = 'lianaihuashuai'
        if 'nametype' in params:
            nametype = params['nametype']
        nowappid = xiaochengxus[nametype]['appid']
        trade_type = 'JSAPI'
        openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['openid']
    elif apptype == 'fwh':
        nowappid = fuwuhaoappid
        trade_type = 'JSAPI'
        openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['fwhid']
    else:
        nametype = 'lianaituodanhuashu'
        if 'nametype' in params:
            nametype = params['nametype']
        nowappid = apps[nametype]['appid']
        trade_type = 'APP'
        openid = es.get(index='userinfo', doc_type='userinfo', id=unionid)['_source']['yingyongid']
    kechengjiage = int(es.get(index='kechenglist', doc_type='kechenglist', id=kechengid)['_source']['jiage'] * 100)
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    prepaydata = {
        'appid': nowappid,
        'mch_id': mch_id,
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
            'partnerid': mch_id,
            'prepayid': prepay_id,
            'package': 'Sign=WXPay',
            'noncestr': result['nonce_str'],
            'timestamp': str(int(time.time())),
        }
    stringA = '&'.join(["{0}={1}".format(k, paySign_data.get(k)) for k in sorted(paySign_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest()
    if apptype == 'weixin' or apptype == 'fwh':
        paySign_data['paySign'] = paySign
    else:
        paySign_data['sign'] = paySign
    doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
    doc = doc['_source']
    if 'phoneNumber' not in doc:
        return encrypt(json.dumps({'MSG': 'nophoneNumber', 'data': paySign_data}))
    return encrypt(json.dumps({'MSG': 'OK', 'data': paySign_data}))


@app.route(apiqianzui + "kechengpaynotify", methods=["POST"])
def kechengpaynotify():
    zhifures = xml_to_dict(request.stream.read().decode('utf8'))
    sign = zhifures['sign']
    zhifures.pop('sign')
    stringA = '&'.join(["{0}={1}".format(k, zhifures.get(k)) for k in sorted(zhifures)])
    stringSignTemp = '{0}&key={1}'.format(stringA, merchant_key)
    paySign = hashlib.md5(stringSignTemp.encode('utf8')).hexdigest().upper()
    if sign != paySign:
        return dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'})
    unionid = json.loads(zhifures['attach'])['unionid']
    zhifudata = [zhifures]
    isnew = 1
    flag = 1
    try:
        doc = es.get(index='userzhifu', doc_type='userzhifu', id=unionid)
        isnew = 0
        for line in doc['_source']['zhifudata']:
            if line['transaction_id'] == zhifudata[0]['transaction_id']:
                flag = 0
        if flag:
            zhifudata += doc['_source']['zhifudata']
    except Exception as e:
        logger.error(e)
    if isnew or (isnew == 0 and flag == 1):
        es.index(index='userzhifu', doc_type='userzhifu', id=unionid,
                 body={'unionid': unionid, 'zhifudata': zhifudata, 'updatatime': zhifures['time_end']})
        zhifures['total_fee'] = int(zhifures['total_fee'])
        doc = es.get(index='userinfo', doc_type='userinfo', id=unionid)
        userdoc = doc['_source']
        userdoc['xiaofeicishu'] += 1
        userdoc['xiaofeizonge'] += zhifures['total_fee']
        es.index(index='userinfo', doc_type='userinfo', id=unionid, body=userdoc)
        try:
            kechengid = json.loads(zhifures['attach'])['kechengid']
            try:
                goumaidoc = es.get(index='kechenggoumai', doc_type='kechenggoumai', id=unionid)['_source']
                goumaidoc['data'] = json.loads(goumaidoc['data'])
                goumaidoc['data'][kechengid] = 1
            except:
                goumaidoc = {}
                goumaidoc['unionid'] = unionid
                goumaidoc['data'] = {}
                goumaidoc['data'][kechengid] = 1
            goumaidoc['data'] = json.dumps(goumaidoc['data'], ensure_ascii=False)
            es.index(index='kechenggoumai', doc_type='kechenggoumai', id=unionid, body=goumaidoc)
        except Exception as e:
            logger.error(e)
        # try:
        #     newdoc = es.get(index='fenxiao', doc_type='fenxiao', id=unionid)['_source']
        #     shangji = newdoc['shangji']
        #     shangshangji = newdoc['shangshangji']
        #     if shangji != '':
        #         try:
        #             fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=shangji)['_source']
        #             yijibili = 0.1
        #             if len(fenxiao['yijiyonghu']) >= 30:
        #                 yijibili = 0.4
        #             elif len(fenxiao['yijiyonghu']) >= 10:
        #                 yijibili = 0.3
        #             elif len(fenxiao['yijiyonghu']) >= 3:
        #                 yijibili = 0.2
        #             newzhifu = {}
        #             newzhifu['yonghuming'] = userdoc['nickName']
        #             newzhifu['shangpinming'] = json.loads(zhifures['attach'])['detail']
        #             newzhifu['time'] = getTime()
        #             newzhifu['total_fee'] = zhifures['total_fee'] * 0.01
        #             newzhifu['shouyi'] = zhifures['total_fee'] * 0.00994 * yijibili
        #             fenxiao['dingdan'].insert(0, newzhifu)
        #             fenxiao['zongshouyi'] += zhifures['total_fee'] * 0.00994 * yijibili
        #             fenxiao['ketixian'] += zhifures['total_fee'] * 0.00994 * yijibili
        #             es.index(index='fenxiao', doc_type='fenxiao', id=shangji, body=fenxiao)
        #         except:
        #             None
        #     if shangshangji != '':
        #         try:
        #             fenxiao = es.get(index='fenxiao', doc_type='fenxiao', id=shangshangji)['_source']
        #             yijibili = 0.04
        #             if len(fenxiao['yijiyonghu']) >= 30:
        #                 yijibili = 0.1
        #             elif len(fenxiao['yijiyonghu']) >= 10:
        #                 yijibili = 0.08
        #             elif len(fenxiao['yijiyonghu']) >= 3:
        #                 yijibili = 0.06
        #             newzhifu = {}
        #             newzhifu['yonghuming'] = userdoc['nickName']
        #             newzhifu['shangpinming'] = json.loads(zhifures['attach'])['detail']
        #             newzhifu['time'] = getTime()
        #             newzhifu['total_fee'] = zhifures['total_fee'] * 0.01
        #             newzhifu['shouyi'] = zhifures['total_fee'] * 0.00994 * yijibili
        #             fenxiao['dingdan'].insert(0, newzhifu)
        #             fenxiao['zongshouyi'] += zhifures['total_fee'] * 0.00994 * yijibili
        #             fenxiao['ketixian'] += zhifures['total_fee'] * 0.00994 * yijibili
        #             es.index(index='fenxiao', doc_type='fenxiao', id=shangshangji, body=fenxiao)
        #         except:
        #             None
        # except:
        #     None
    return dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'})


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 18888), app)
    server.serve_forever()
