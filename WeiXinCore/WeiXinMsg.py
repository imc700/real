# coding:utf-8

import xml.etree.ElementTree as ET
import time

from WeiXinCore.real import TextResult


class WeiXinMsg(object):
    def __init__(self, xml_body=None):
        self.xml_body = xml_body  # unicode(xml_body).encode("utf-8")
        root = ET.fromstring(self.xml_body)

        self.j = {}
        for child in root:
            if child.tag == 'CreateTime':
                value = int(child.text)
            else:
                value = child.text
            self.j[child.tag] = value
        self.ToUserName = self.j['FromUserName']
        self.FromUserName = self.j['ToUserName']
        self.MsgType = self.j['MsgType']

        self.MsgId = self.j['MsgId'] if self.j.__contains__('MsgId') else ''
        self.Content = self.j['Content'] if self.j.__contains__('Content') else ''
        self.PicUrl = self.j['PicUrl'] if self.j.__contains__('PicUrl') else ''
        self.MediaId = self.j['MediaId'] if self.j.__contains__('MediaId') else ''
        self.Recognition = self.j['Recognition'] if self.j.__contains__('Recognition') else ''
        self.Format = self.j['Format'] if self.j.__contains__('Format') else ''
        self.ThumbMediaId = self.j['ThumbMediaId'] if self.j.__contains__('ThumbMediaId') else ''
        self.Location_X = self.j['Location_X'] if self.j.__contains__('Location_X') else ''
        self.Location_Y = self.j['Location_Y'] if self.j.__contains__('Location_Y') else ''
        self.Scale = self.j['Scale'] if self.j.__contains__('Scale') else ''
        self.Label = self.j['Label'] if self.j.__contains__('Label') else ''
        self.Title = self.j['Title'] if self.j.__contains__('Title') else ''
        self.Description = self.j['Description'] if self.j.__contains__('Description') else ''
        self.Url = self.j['Url'] if self.j.__contains__('Url') else ''
        self.EventKey = self.j['EventKey'] if self.j.__contains__('EventKey') else ''
        self.Event = self.j['Event'].lower() if self.j.__contains__('Event') else ''
        self.Ticket = self.j['Ticket'].lower() if self.j.__contains__('Ticket') else ''

    # # ToUserName  开发者微信号
    # # FromUserName    发送方帐号（一个OpenID）
    # # CreateTime  消息创建时间 （整型）
    # # MsgType 消息类型
    # # Content 文本消息内容
    # # MsgId   消息id，64位整型

    # # PicUrl  图片链接
    # # MediaId 图片消息媒体id，可以调用多媒体文件下载接口拉取数据。
    # # MediaId 语音消息媒体id，可以调用多媒体文件下载接口拉取数据。
    # # Format  语音格式，如amr，speex等
    # # MediaId 视频消息媒体id，可以调用多媒体文件下载接口拉取数据。
    # # ThumbMediaId    视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。
    # # MediaId 视频消息媒体id，可以调用多媒体文件下载接口拉取数据。
    # # ThumbMediaId    视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。
    # # Location_X  地理位置维度
    # # Location_Y  地理位置经度
    # # Scale   地图缩放大小
    # # Label   地理位置信息
    # # Title   消息标题
    # # Description 消息描述
    # # Url 消息链接

    def __getitem__(self, name):
        return self.j[name] if self.j.__contains__(name) else ''

    def resp_text(self, text, funcFlag=0):
        template = u'''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>%s</FuncFlag>
</xml>'''
        text_msg = template % (self.ToUserName, self.FromUserName, int(time.time()), text, funcFlag)
        print(text_msg)
        return text_msg

    # todo 2021年2月20日23:05:29抽空在此处增加一个回复链接消息的方法
    def resp_link(self, t_result):
        template3 = u'''<xml>
<ToUserName><![CDATA[{}]]></ToUserName>
<FromUserName><![CDATA[{}]]></FromUserName>
<CreateTime>{}</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>1</ArticleCount>
<Articles>
<item>
  <Title><![CDATA[{}]]></Title>
  <Description><![CDATA[{}]]></Description>
  <PicUrl><![CDATA[{}]]></PicUrl>
  <Url><![CDATA[{}]]></Url>
</item>
</Articles>
</xml>'''.format(self.ToUserName, self.FromUserName, int(time.time()), t_result.result(),
                 t_result.title,t_result.pict_url, t_result.url)
        return template3

