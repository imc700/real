# #!/usr/bin/env python
# # coding=utf-8
# from aliyunsdkcore.Ac import *
# from aliyunsdkcore.request import CommonRequest
#
# #pip3 install aliyun-python-sdk-core-v3
# #pip3 install aliyun-python-sdk-cdn
# #https://dysms.console.aliyun.com/dysms.htm?spm=5176.8195934.J_5834642020.4.32314378jivEWj#/overview
# #https://api.aliyun.com/new#/?product=Dysmsapi&version=2017-05-25&api=SendSms&params={%22RegionId%22:%22cn-hangzhou%22}&tab=DEMO&lang=PYTHON
# # 阿里短信api调用用户:imc700@1719596909413170.onaliyun.com-Hanxu7456..
# # 用户登录名称 imc700@1719596909413170.onaliyun.com
# # flask登录接口,cookie设置等.服务号建立和短信模板的建立.自动回复link的功能.和商城详情页接口的处理.
#
# request = CommonRequest()
# request.set_accept_format('json')
# request.set_domain('dysmsapi.aliyuncs.com')
# request.set_method('POST')
# request.set_protocol_type('https')  # https | http
# request.set_version('2017-05-25')
# request.set_action_name('SendSms')
#
# request.add_query_param('RegionId', "cn-hangzhou")
# request.add_query_param('PhoneNumbers', "18627783779")
# request.add_query_param('SignName', "111")
# request.add_query_param('TemplateCode', "222")
#
# response = AcsClient.do_action_with_exception(request)
# print(str(response, encoding='utf-8'))
