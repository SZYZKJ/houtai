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
    '胖版动物圣诞版': '点击复制网盘链接进去下载即可：https://pan.baidu.com/s/1SYdMyFLRXS7GjKzxSXDrAw，非常高清而又好玩的胖版动物视频供你分享哦',
    '谜男方法': '点击以下百度网盘链接：https://pan.baidu.com/s/1eEHI2VwwOhBZaH3oZCyApg，复制网址进入浏览器下载即可，感谢支持\n《迷男方法》书籍可能大家之前看过，也可能没看过，但是无论看过还是没看过，我们建议大家再次回去认真学习，里面提供的方法，远远比市场上面的聊天教程，速推教程（恋爱联盟不提倡不尊敬女性的行为）要好！我们再次推送，希望对你有帮助，再次感谢大家的支持',
    '人工智能': '《人工智能时代：未来已来》链接: https://pan.baidu.com/s/1mr9rA4ZOv146yvUaiQk3cQ 提取码: 2a68，愚人节彩蛋，希望大家喜欢。人工智能撩妹将作为我们战略性版本更新方向，敬请期待',
    '从行动开始': '链接: https://pan.baidu.com/s/1s89bKVS09E5uheUklU2M5Q 提取码: yqxh 《从行动开始》这是一本关于自我管理，从行动出发，切切实实的一步一步去做，这样才会靠自己创造出一个未来！一起加油，一起成长',
    '思维导图': '链接: https://pan.baidu.com/s/1T71bItHrZvTeppvW0kCpKw 提取码: 6e8q 《谜男方法》思维导图，让你快速了解全局M3模型',
    'image_msg': '撩妹助理暂时还没有学会识别图片消息，我们还是先用文字交流吧[Smart]\n',
    'subscribe': '感谢您关注恋爱联盟，这是一款智能回复妹纸的撩妹聊天神器，点击公众号菜单栏中间的小程序，复制女生聊天的话在小程序里搜索，轻轻一点即可复制回复女生。海量幽默、推拉话术、套路可供搜索使用，海量形象展示、撩妹实战、土味情话、情感百科、心理测试免费供你使用。恋爱联盟竭诚为您服务，祝您赢取女神欢心！/:rose/:rose/:rose',
}
es = Elasticsearch([{"host": "182.254.227.188", "port": 9218, "timeout": 3600}])


def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def adduserhis(userhis):
    es.index(index='userhis', doc_type='userhis', body=userhis)
    return None


class Handel:

    def __init__(self):
        None

    def handel_msg(self, recMsg):
        # 发送与接收时的主体和客体是相反的
        userid = recMsg.FromUserName  # 用户
        gongzhonghaoid = recMsg.ToUserName  # 公众号
        createTime = recMsg.CreateTime
        msgType = recMsg.MsgType
        reply_content = ''
        if msgType == 'text' or msgType == 'voice':
            # 处理文本消息
            if msgType == 'text':
                receive_content = str(recMsg.Content, encoding='utf8')
            else:
                receive_content = recMsg.Recognition
            if receive_content in reply_sentens:
                reply_content = reply_sentens[receive_content]
            else:
                reply_content = reply_sentens['subscribe']
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
        if len(reply_content) == 0:
            reply_content = reply_sentens['subscribe']
        repMsg = reply.TextMsg(userid, gongzhonghaoid, reply_content)
        return repMsg
