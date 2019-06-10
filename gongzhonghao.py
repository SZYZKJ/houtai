from gevent import monkey
from gevent import pywsgi

monkey.patch_all()
from flask import Flask, request
from flask_cors import *
import hashlib
import os
import json
from weixin_app import handel
from weixin_app import receive
from weixin_app import reply
from msg_crypto.WXBizMsgCrypt import WXBizMsgCrypt
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
# 恋爱助理
appid = 'wxc1deae6a065dffa9'
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


@app.route("/lianailianmeng", methods=["GET", "POST"])
def lianailianmeng():
    if request.method == "GET":
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        data = [token, timestamp, nonce]
        data.sort()
        newstring=data[0]+data[1]+data[2]
        sha1=hashlib.sha1()
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


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 13888), app)
    server.serve_forever()
