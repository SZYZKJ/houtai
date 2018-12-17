"""
@Author  : monabai
@Time    : 2018/8/16 16:39
@Software: PyCharm
@File    : qr_generate.py
"""
import io
import requests
import json
from basic import Basic


if __name__ == '__main__':
    name='天涯'
    accessToken = Basic().get_access_token()
    postUrl = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % accessToken
    postJson = '{"action_name":"QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": "'+name+'"}}}'
    response = requests.post(postUrl, data=postJson.encode('utf8'))
    response=response.json()
    print(response)
    response=requests.get(url='https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket='+response['ticket'])
    f=open(name+'.jpg','wb')
    f.write(response.content)
    f.close()
