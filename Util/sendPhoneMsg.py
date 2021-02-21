#!/usr/bin/env python
# coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

#pip install aliyun-python-sdk-core-v3
#pip install aliyun-python-sdk-cdn
#https://dysms.console.aliyun.com/dysms.htm?spm=5176.8195934.J_5834642020.4.32314378jivEWj#/overview
#https://api.aliyun.com/new#/?product=Dysmsapi&version=2017-05-25&api=SendSms&params={%22RegionId%22:%22cn-hangzhou%22}&tab=DEMO&lang=PYTHON
# 阿里短信api调用用户:imc700@1719596909413170.onaliyun.com-Hanxu7456..
# 用户登录名称 imc700@1719596909413170.onaliyun.com
# AccessKey ID LTAI4GGjxx5FLRLgQmdVfnaG
# AccessKey Secret vx8fTCQHEry9V7mwi7T0po7pZuQoAG

client = AcsClient('LTAI4GGjxx5FLRLgQmdVfnaG', 'vx8fTCQHEry9V7mwi7T0po7pZuQoAG', 'cn-hangzhou')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https')  # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')

request.add_query_param('RegionId', "cn-hangzhou")

response = client.do_action(request)
# python2:  print(response)
print(str(response, encoding='utf-8'))
