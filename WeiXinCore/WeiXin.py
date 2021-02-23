# coding:utf-8
# import time
# import MySQLdb
from flask import Flask, g, request, make_response
import hashlib
# import xml.etree.ElementTree as ET
# import urllib2
# import json


from Handlers.weixin_handler import *

# from index import app
# from WeiXin.weixin_handler import *
from WeiXinCore.WeiXinMsg import WeiXinMsg

EventType = {
    "subscribe": onSubscribe,
    "unsubscribe": onUnsubscribe,
    "scan": onScan,
    "location": onEventLocation,
    "click": onClick,
    "view": onView
}
# def onEvent(wxmsg):
#    return EventType[wxmsg.Event](wxmsg) if EventType.__contains__(wxmsg.Event) else ''
Response = {
    "event": lambda wxmsg: EventType[wxmsg.Event](wxmsg) \
        if EventType.__contains__(wxmsg.Event) else '',
    "text": onText,
    "voice": onVoice,
    "image": onImage,
    "video": onVideo,
    "shortvideo": onShortVideo,
    "location": onLocation,
    "link": onLink,
}



def check_signature(request_args):
    query = request.args
    signature = query.get('signature', '')
    timestamp = query.get('timestamp', '')
    nonce = query.get('nonce', '')
    # echostr = query.get('echostr', '')
    s = [timestamp, nonce, TOKEN]
    s.sort()
    s = ''.join(s)
    return hashlib.sha1(s).hexdigest() == signature
