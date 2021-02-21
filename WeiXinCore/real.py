import traceback
from flask import Flask, render_template, g, json, request
import pymysql
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time
import os

# app = Flask(__name__)
# ctx = app.app_context()
# ctx.push()

# @app.route()

# api文档:https://www.ecapi.cn/index/index/openapi/id/50.shtml?ptype=1
# 云商数据:https://console.ecapi.cn/dashboard/workplace

apkey = '106dd6f8-103e-f437-6b53-43b80c09ef07'
pid = 'mm_50401481_2105100471_110937350217'
tbname = 'imc701'


def query_goods_by_id(itemid):
    '''
    根据商品id查询商品基本详情(名称,价格,图片等)
    :param itemid:
    :return:
    '''
    return requests.get('http://api.web.ecapi.cn/taoke/getItemInfo?apkey={}&itemid={}'.format(apkey, itemid))


def query_youhui_by_itemid(itemid):
    '''
    根据商品id查询商品优惠情况(优惠券和返利比例)
    :param itemid:
    :return:
    '''
    return requests.get(
        'http://api.web.ecapi.cn/taoke/doItemHighCommissionPromotionLink?apkey={}&itemid={}&pid={}&tbname={}&shorturl=1&tpwd=1&extsearch=1&hasiteminfo=1&qrcode=1'.format(
            apkey, itemid, pid, tbname))


def query_youhui_by_tpwdcode(tpwdcode):
    '''
    根据商品id查询商品优惠情况(优惠券和返利比例)
    :param itemid:
    :return:
    '''
    return requests.get(
        'http://api.web.ecapi.cn/taoke/doItemHighCommissionPromotionLinkByTpwd?apkey={}&tpwdcode={}&pid={}&tbname={}&shorturl=1&tpwd=1&extsearch=1&hasiteminfo=1&qrcode=1'.format(
            apkey, tpwdcode, pid, tbname))


def trans_tpwd_to_itemid(tpwd):
    '''
    淘口令取itemid
    :param tpwd:
    :return:
    '''
    return requests.get(
        'http://api.web.ecapi.cn/taoke/doTpwdCovert?apkey={}&pid={}&content={}&tbname={}'.format(apkey, pid, tpwd,
                                                                                                 tbname))


def maybe_u_like_by_itemid(keyword):
    '''
    关键词搜索同类商品作为详情页推荐列表,点击任何一个推荐的商品,就根据商品id去获得专属淘口令供用户购买.
    :param keyword:
    :return:
    '''
    return requests.get(
        'http://api.web.ecapi.cn/platform/getItemList?apkey={}&page=1&keyword={}'.format(apkey, keyword))


def order_thread():
    '''
    需要开通云商数据会员.v1两年1k,一年600,单月88__暂不费钱调试订单接口,先处理其他接口,最后需要订单接口时再买会员,建议买一年.
    每3分钟跑一次淘客订单接口,更新本地db的状态并结算金额.
    :return:
    '''
    return requests.get(
        'http://api.web.ecapi.cn/taoke/tbkOrderDetailsGet?apkey={}&end_time={}&start_time={}&tbname={}'.format(apkey,
                                                                                                                '2020-10-15+18:18:22',
                                                                                                                '2020-11-15+18:18:21',
                                                                                                                tbname))


if __name__ == '__main__':
    # app.run(port=39002, debug=True)

    # response = query_goods_by_id('571900197140')
    # response = query_youhui_by_itemid('634753362776')
    # response = query_youhui_by_tpwdcode('2👈 ha:/啊OrSocxpkeEj啊  苹果12钢化水凝膜苹果X/xr/xs/全屏覆盖iphone7/8/plus偷窥全包边iphone11pro max磨砂纳米手机软膜抗蓝光max')
    response = maybe_u_like_by_itemid('AirPods')
    # response = order_thread()
    response_json = response.json()
    print(response.json())

