import time
import os
import csv
from weixin_app import reply
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from es.es import Lianailianmeng_ES

datapath = '/home/ubuntu/data/lianailianmeng/data'
os.chdir(datapath)

reply_sentens = {
    'use_limit': '您今天的使用次数已经达到上限30次，欢迎明天再来使用，祝您生活愉快～',
    'no_search_result': '这个问题太高深了，撩妹助理现在也不知道怎么回答[Facepalm]\n',
    'image_msg': '撩妹助理暂时还没有学会识别图片消息，我们还是先用文字交流吧[Smart]\n'
                 '当然语音也可以[Smirk]',
    'subscribe': '海量撩妹话术、精选惯例、迷你情话和恋爱策略可供搜索，并支持语音搜索，您的智能撩妹恋爱助理/:8-)\n'
                 '使用方法：首先把女神的话复制到下面的对话框（支持语音），'
                 '然后我会用叼炸天的人工智能算法帮你挑选几个候选情话，你只需双击文本然后选择复制满意的回复即可🎉🎁💪\n'
                 '助你撩妹成功/:,@f/:handclap/:love',
    'others': '功能正在建设中，敬请期待/:,@f\n'
              '意见或者建议反馈请联系\n'
              '手机/微信号：15622146998\n'
              '邮箱：421542148@qq.com\n'
              '您的支持与反馈是我们前进的不竭动力，非常感谢~'
}
es = Elasticsearch([{"host": "182.254.227.188", "port": 9218, "timeout": 3600}])


# userhiss = []

def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def adduserhis(userhis):
    es.index(index='userhis', doc_type='userhis', body=userhis)
    # global userhiss
    # action = {
    #     "_index": "userhis",
    #     "_type": "userhis",
    #     "_source": userhis
    # }
    # userhiss.append(action)
    # if len(userhis) >= 500:
    #     helpers.bulk(es, userhiss)
    #     userhiss = []
    return None


class Handel:
    usercache = {}
    userdata = {}
    whitelist = {}
    laes = Lianailianmeng_ES()

    def __init__(self):
        self.whitelist['oswSD0qc_PK8GpQpv8_sM10Ktar8'] = 0
        self.whitelist['oswSD0mJaa5BYZD81cMOpLA1Nd-I'] = 0
        self.whitelist['opU7s58jcbrJsJkD_DB4nCgsUF2s'] = 0
        self.whitelist['oswSD0gZN78kpZfASDOkwgvPGyD8'] = 0
        self.whitelist['oswSD0jXQ27ZZq7fDCzGweLTjbvc'] = 0

    def check_user(self, userid):
        if userid in self.whitelist:
            return 1
        if len(userid) != 28: return 0
        timelist = time.asctime().split()
        strtime = timelist[1] + timelist[2] + timelist[4]
        if userid not in self.userdata:
            self.userdata[userid] = {'num': 29, 'time': strtime}
            return 1
        if self.userdata[userid]['time'] != strtime:
            self.userdata[userid] = {'num': 29, 'time': strtime}
            return 1
        if self.userdata[userid]['num'] > 0:
            self.userdata[userid]['num'] -= 1
            return 1
        return 0

    def reply_format(self, response, userid):
        try:
            self.usercache[userid] = {}
            self.usercache[userid]['response'] = response
            if len(response) > 6:
                reply_content = "回复对应编号可快速复制回复\n如第3条c项则回复3c\n回复0代表下一页\n"
            elif len(response) > 1:
                reply_content = "回复对应编号可快速复制回复\n如第3条c项则回复3c\n"
            else:
                reply_content = ""
            for index, item in enumerate(response[:6]):
                if 'title' in item:
                    temp = item['title'] + '\n\n' + item['content']
                else:
                    temp = str(index + 1) + '\n' + '美女: ' + item['MM'] + '\n' + '型男：'
                    if len(item['GG']) == 1:
                        temp += item['GG'][0] + '\n'
                        self.usercache[userid][str(index + 1)] = item['GG'][0]
                    else:
                        for u, v in enumerate(item['GG']):
                            temp += chr(ord('a') + u) + '、' + v + '\n'
                            self.usercache[userid][str(index + 1) + chr(ord('a') + u)] = v
                reply_content += temp
            lenresponse = len(self.usercache[userid]['response'])
            for i in range(min(6, lenresponse)):
                self.usercache[userid]['response'].pop(0)
        except Exception as e:
            print(e)
            reply_content = reply_sentens['no_search_result']
        return reply_content

    def handel_msg(self, recMsg):
        # 发送与接收时的主体和客体是相反的
        userid = recMsg.FromUserName  # 用户
        gongzhonghaoid = recMsg.ToUserName  # 公众号
        createTime = recMsg.CreateTime
        msgType = recMsg.MsgType
        reply_content = ''
        if self.check_user(userid) == 0:
            reply_content = reply_sentens['use_limit']
        else:
            payload = {
                'query': '',
                'open_id': userid,
                'create_time': createTime,
                'msg_type': msgType,
            }
            if msgType == 'text' or msgType == 'voice':
                # 处理文本消息
                if msgType == 'text':
                    receive_content = str(recMsg.Content, encoding='utf8')
                else:
                    receive_content = recMsg.Recognition
                receive_content = receive_content.lower()
                receive_content = receive_content.strip()
                if len(receive_content) > 0 and receive_content[-1] == '。':
                    receive_content = receive_content[:-1]
                if userid in self.usercache and receive_content in self.usercache[userid]:
                    reply_content = self.usercache[userid][receive_content]
                elif (receive_content == '0' or receive_content == '零'):
                    if userid in self.usercache and len(self.usercache[userid]['response']) > 0:
                        reply_content = self.reply_format(self.usercache[userid]['response'], userid)
                    else:
                        reply_content = '下一页没有内容了~'
                else:
                    payload['query'] = receive_content
                    response = self.laes.search(params=payload)
                    if response['msg_type'] == 'text':
                        reply_content = self.reply_format(response['data'], userid)
                    else:
                        repMsg = reply.ImageMsg(userid, gongzhonghaoid, response['data'])
                        return repMsg
            elif msgType == 'image':
                picUrl = recMsg.PicUrl
                msgId = recMsg.MsgId
                mediaId = recMsg.MediaId
                reply_content = reply_sentens['image_msg']
            elif msgType == 'event':
                eventKey = recMsg.EventKey
                adduserhis(
                    {'openid': userid, 'time': getTime(), 'event': recMsg.Event, 'detail': eventKey,
                     'type': '1'})
                # 处理关注或则会取消关注事件
                if recMsg.Event == 'subscribe':
                    reply_content = reply_sentens['subscribe']
                elif recMsg.Event == 'CLICK':
                    # 第三个菜单栏【联系我们】，点击事件处理
                    if eventKey == "lianaizhuli_v1_business":
                        # 【联系我们】商务合作
                        repMsg = reply.ImageMsg(userid, gongzhonghaoid,
                                                mediaId="yYuh_32i1qVXDlPAcwH8RUsstY4vWf3wb19pxwcZKvA")
                        return repMsg
                    elif eventKey == "lianaizhuli_v1_jiaweixinqun":
                        # 【联系我们】加微信群
                        repMsg = reply.ImageMsg(userid, gongzhonghaoid,
                                                mediaId="yYuh_32i1qVXDlPAcwH8RVJpGqSNB_19W28gfuJmafc")
                        return repMsg
                    else:
                        reply_content = reply_sentens['others']
        if len(reply_content) == 0:
            reply_content = reply_sentens['subscribe']
        repMsg = reply.TextMsg(userid, gongzhonghaoid, reply_content)
        return repMsg
