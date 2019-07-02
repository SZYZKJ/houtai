# -*- coding: utf-8 -*-
# filename: menu.py
import sys
sys.path.append('../')
import io
import json
import requests
from weixin_app.basic import Basic
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Menu(object):
    def __init__(self):
        pass

    def create(self, postData, accessToken):
        print(accessToken)
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        response = requests.post(postUrl, data=postData)
        print(response.json())

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        response = requests.post(postUrl)
        print(response.json())

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        response = requests.post(postUrl)
        print(response.json())

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        response = requests.post(postUrl)
        print(response.json())


if __name__ == '__main__':
    myMenu = Menu()
    postJson ={
        "button": [
            {
                "name": "加入会员",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "会员",
                        "url": "http://www.lianaizhuli.com/huiyuan",
                        "sub_button": []
                    },
                    {
                        "type": "view",
                        "name": "课程",
                        "url": "http://www.lianaizhuli.com/kechenglist",
                        "sub_button": []
                    },
                ]
            },
            {
                "name": "小程序",
                "type": "miniprogram",
                "appid": "wxa9ef833cef143ce1",
                "pagepath": "pages/home",
                "url": "https://www.lianaizhuli.com/gongzhonghao/lianxiwomen.html",
                "sub_button": []
            },
            {
                "name": "联系我们",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "意见反馈",
                        "url": "http://www.lianaizhuli.com:1888/#/feedback",
                        "sub_button": []
                    },
                    {
                        "type": "view",
                        "name": "联系我们",
                        "url": "https://www.lianaizhuli.com/gongzhonghao/lianxiwomen.html",
                        "sub_button": []
                    },
                    {
                        "type": "view",
                        "name": "人才招聘",
                        "url": "https://mp.weixin.qq.com/s/iCoVfPko0v-egPYSKTbN9Q",
                        "sub_button": []
                    },
                    {
                        "type": "view",
                        "name": "联盟干货",
                        "url": "https://mp.weixin.qq.com/mp/homepage?__biz=MzUyODk3NjUwOQ==&hid=8&sn=62bc4e3e03b70238d3110bf508d2dbaa",
                        "sub_button": []
                    },
                    {
                        "type": "view",
                        "name": "联盟公开课",
                        "url": "https://mp.weixin.qq.com/mp/homepage?__biz=MzUyODk3NjUwOQ==&hid=7&sn=94e73b7866c8b51e69433021e89a146f",
                        "sub_button": []
                    }
                ]
            }
        ]
    }
    accessToken = Basic().get_access_token()
    myMenu.delete(accessToken)
    myMenu.create(json.dumps(postJson,ensure_ascii=False).encode('utf8'), accessToken)
