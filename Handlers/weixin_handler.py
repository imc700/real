from WeiXinCore.real import *
import requests
import json
import http.client

TOKEN = 'imc700'

def onText(wxmsg):
    '''收到文本
    Content	文本消息内容'''
    inTxt = wxmsg.Content
    if 'tb.cn' in inTxt.lower() or inTxt[0].isdigit():
        t_result = TextResult(share_url=inTxt, username=wxmsg.ToUserName)
        if t_result.code != 200:
            return wxmsg.resp_text(no_youhui_words), t_result
        return wxmsg.resp_link(t_result), t_result
    elif 'jd.' in inTxt.lower():
        itemid = jd_copy_url_2_itemid(inTxt)
        if itemid:
            jd_result = jd_item_youhui(itemid, wxmsg.ToUserName)
            # if jd_result.code != 200:
            if type(jd_result) == str:
                return wxmsg.resp_text(no_youhui_words), jd_result
            return wxmsg.resp_link(jd_result), jd_result
        else:
            return wxmsg.resp_text(u'官人,请分享商品链接给我哟~'), None
    elif 'yangkeduo' in inTxt.lower():
        itemid = pdd_copy_url_2_itemid(inTxt)
        print('用户查询拼多多商品,itemid:', itemid)
        # if itemid:
        #     pdd_result = pdd_item_youhui(itemid, wxmsg.ToUserName)
        #     if pdd_result.code != 200:
        #         return wxmsg.resp_text(no_youhui_words), pdd_result
        #     return wxmsg.resp_link(pdd_result), pdd_result
        # else:
        return wxmsg.resp_text(u'官人,拼多多返利规则有变.请查看菜单栏-返利教程-拼多多返利查看~'), None
    else:
        return wxmsg.resp_text(u'官人,请分享商品链接给我哟~'), None

#todo 9
appid = "wx0212875e85602959"
secret = "34f9bc08889f56fd0408db6c0c8bbb79"
def create_menu():

    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appid + "&secret=" + secret
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, headers=headers)

    print(response.content.decode())

    token = response.json()['access_token']

    ## https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
    # connection = http.client.HTTPSConnection('api.weixin.qq.com')

    data = {
        "button": [
            {
                "type": "view",
                "name": "搜优惠",
                "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx0212875e85602959&redirect_uri=http://afanxyz.xyz&response_type=code&scope=snsapi_base&state=1&#wechat_redirect"
            },
            {
                "name": "返利教程",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "淘宝天猫返利",
                        "url": "https://mp.weixin.qq.com/s/LtyUZkcggW2u9NqHHnFgLA"
                    },
                    {
                        "type": "view",
                        "name": "京东返利",
                        "url": "https://mp.weixin.qq.com/s/SUj_FZFHwsss64QcoOrwlA"
                    },
                    {
                        "type": "view",
                        "name": "拼多多返利",
                        "url": "https://mp.weixin.qq.com/s/aThhAT5sSPw9axVCiBT-mg"
                    }
                    # ,
                    # {
                    #     "type": "click",
                    #     "name": "赞一下我们",
                    #     "key": "V1001_GOOD"
                    # }
                ]
            },
            {
                "name": "我的",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "个人中心",
                        "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx0212875e85602959&redirect_uri=http://afanxyz.xyz/pages/mine/mine&response_type=code&scope=snsapi_base&state=1&#wechat_redirect"
                    },
                    {
                        "type": "view",
                        "name": "我的订单",
                        "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx0212875e85602959&redirect_uri=http://afanxyz.xyz/pages/mine/order&response_type=code&scope=snsapi_base&state=1&#wechat_redirect"
                    },
                    {
                        "type": "view",
                        "name": "提现记录",
                        "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx0212875e85602959&redirect_uri=http://afanxyz.xyz/pages/mine/reward&response_type=code&scope=snsapi_base&state=1&#wechat_redirect"
                    }
                    ]
            }
        ]
    }

    headers = {'Content-type': 'application/json'}
    result = requests.post('https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + token,
                           data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                           headers=headers)
    # connection.request('POST', '/cgi-bin/menu/create?access_token=' + token + '',
    #                    json.dumps(data, ensure_ascii=False).encode('utf-8'), headers)
    # response = connection.getresponse()
    str1 = result.json()

    print(str1)
def tbk_beian():
    appid = "0212875e85602948"
    secret = "34f9bc08889f56fd0408db6c0c8bbb68"
    url = "http://api.web.ecapi.cn/taoke/getRelationOauthTpwd?apkey={}&invitercode=839F99&rtag=imc700839F99&content=onekeybeian".format(apkey)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    response = requests.get(url, headers=headers)

    print(response.content.decode())
    response_json = response.json()
    token = ['access_token']

    ## https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
    # connection = http.client.HTTPSConnection('api.weixin.qq.com')

    data = {
        "button": [
            {
                "type": "view",
                "name": "优惠券",
                "url": "http://www.soso.com/"
            },
            {
                "name": "返利教程",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "淘宝天猫返利",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "京东返利",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "拼多多返利",
                        "url": "http://www.soso.com/"
                    }
                    # ,
                    # {
                    #     "type": "click",
                    #     "name": "赞一下我们",
                    #     "key": "V1001_GOOD"
                    # }
                ]
            },
            {
                "name": "我的",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "我的红包",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "红包记录",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "view",
                        "name": "我的订单",
                        "url": "http://www.soso.com/"
                    }]
            }
        ]
    }

    headers = {'Content-type': 'application/json'}
    result = requests.post('https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + token,
                           data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                           headers=headers)
    # connection.request('POST', '/cgi-bin/menu/create?access_token=' + token + '',
    #                    json.dumps(data, ensure_ascii=False).encode('utf-8'), headers)
    # response = connection.getresponse()
    str1 = result.json()

    print(str1)


if __name__ == '__main__':
    create_menu()


def onImage(wxmsg):
    '''收到图片
    PicUrl	图片链接
	MediaId	图片消息媒体id，可以调用多媒体文件下载接口拉取数据。'''
    # return wxmsg.resp_music('Sorry','对不起，我还识别不了，来听首歌吧。',r'http://7s1r1i.com1.z0.glb.clouddn.com/小皮%20-%20村庄.mp3','')
    return wxmsg.resp_text(u'对不起，我还识别不了……')


def onVoice(wxmsg):
    '''收到语音
    MediaId	语音消息媒体id，可以调用多媒体文件下载接口拉取数据。
	Format	语音格式，如amr，speex等
	Recognition为语音识别结果'''
    return wxmsg.resp_text(wxmsg.Recognition if wxmsg.Recognition is not 'None' else u"没听懂……")


def onVideo(wxmsg):
    '''收到视频
    MediaId	视频消息媒体id，可以调用多媒体文件下载接口拉取数据。
	ThumbMediaId	视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。'''
    return wxmsg.resp_text(u'对不起，我还识别不了……')


def onShortVideo(wxmsg):
    '''收到小视频'''
    return wxmsg.resp_text(u'对不起，我还识别不了……')


def onLocation(wxmsg):
    '''收到位置信息
    Location_X	地理位置维度
	Location_Y	地理位置经度
	Scale	地图缩放大小
	Label	地理位置信息'''
    txt = u"这是您所在位置：\nX:%s\nY:%s" % (wxmsg['Location_X'], wxmsg['Location_Y'])
    return wxmsg.resp_text(txt)


def onLink(wxmsg):
    '''收到链接
    Title	消息标题
	Description	消息描述
	Url	消息链接'''
    return wxmsg.resp_text('url')


def onSubscribe(wxmsg):
    '''关注'''
    return wxmsg.resp_text(u'感谢你关注我,可搜索任意商品优惠信息哟~菜单栏有惊喜!\n\n返利攻略(淘宝京东拼多多):\n1.分享或复制商品链接给我\n2.下单后2分钟内可查看个人中心\n3.确认收货后5分钟即可提现\n\n\nps:拼多多推广规则有变,具体请点击菜单栏-返利教程-拼多多返利')


def onUnsubscribe(wxmsg):
    '''取消关注'''
    return wxmsg.resp_text(u'oh，漏，你还没说为什么！')


def onScan(wxmsg):
    '''扫描二维码'''
    return wxmsg.resp_text(wxmsg.self.Ticket)


def onClick(wxmsg):
    '''点击菜单拉取消息时 
    EventKey	事件KEY值，与自定义菜单接口中KEY值对应'''
    return wxmsg.resp_text('onClick')


def onEventLocation(wxmsg):
    '''用户同意上报地理位置后，每次进入公众号会话时，都会在进入时上报地理位置
    或在进入会话后每5秒上报一次地理位置，公众号可以在公众平台网站中修改以上设置。
    上报地理位置时，微信会将上报地理位置事件推送到开发者填写的URL
    Latitude	地理位置纬度
	Longitude	地理位置经度
	Precision	地理位置精度'''
    return wxmsg.resp_text('xy')


def onView(wxmsg):
    '''点击菜单跳转链接	
    EventKey	事件KEY值，设置的跳转URL'''
    return wxmsg.resp_text('onView')
