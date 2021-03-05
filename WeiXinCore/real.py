import datetime
import traceback
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

details_url = 'http://afanxyz.xyz/pages/goodsdetail/goodsdetail?goodsId='


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


def trans_zfb(money, realname, alipay, millis):
    """
    支付宝代付接口
    :param money:
    :param realname:
    :param alipay:
    :return:
    """

    return requests.get('http://api.web.ecapi.cn/platform/paymentToAlipay?apkey={}&alipay={}&realname={}&money={}&beizhu=97go返现&thirdorder={}'.format(apkey, alipay, realname, money, str(millis)))


def getTbCategory(cid=0):
    """
    淘宝分类接口
    :param cid:
    :return:
    """
    return requests.get(
        'http://api.web.ecapi.cn/platform/getTbCategory?apkey={}&cid={}'.format(apkey, cid))


def maybe_u_like_by_keyword(keyword):
    '''
    关键词搜索同类商品作为详情页推荐列表,点击任何一个推荐的商品,就根据商品id去获得专属淘口令供用户购买.
    :param keyword:
    :return:http://api.web.ecapi.cn/taoke/getTkMaterialItem?apkey=登录会员中心查看&pid=mm_123456_456789_789132&tbname=xxxxx
    '''
    return requests.get(
        'http://api.web.ecapi.cn/taoke/getTkMaterialItem?sort=tk_total_sales_des&pagesize=100&apkey={}&pid={}&tbname={}&keyword={}'.format(apkey, pid,
                                                                                                      tbname,
                                                                                                      urllib.parse.quote(
                                                                                                          keyword,
                                                                                                          safe='')))


def tb_beian():
    '''
    http://api.web.ecapi.cn/taoke/getTbkQdBeiAn?apkey=登录会员中心查看&invitercode=r48Gjb&infotype=1&tbname=xxxxx
    :return:
    '''


def order_thread():
    '''
    需要开通云商数据会员.v1两年1k,一年600,单月88__暂不费钱调试订单接口,先处理其他接口,最后需要订单接口时再买会员,建议买一年.
    每3分钟跑一次淘客订单接口,更新本地db的状态并结算金额.
    :return:
    '''
    now = time.strftime("%Y-%m-%d+%H:%M:%S", time.localtime())
    before = (datetime.datetime.now() - datetime.timedelta(minutes=20)).strftime("%Y-%m-%d+%H:%M:%S")

    order_response = requests.get('http://api.web.ecapi.cn/taoke/tbkOrderDetailsGet?apkey={}&end_time={}&start_time={}&tbname={}&page_size=100'.format(apkey,now,before,tbname))
    order_json = order_response.json()
    if order_json['code']==200:
        list_ = order_json['data']['list']
        for item in list_:
            pass

    print()


class TextResult:
    def __init__(self, share_url=None, itemid=None, username=None):
        self.username = username
        self.intext = share_url
        if share_url:
            response = query_youhui_by_tpwdcode(share_url)
        if itemid:
            response = query_youhui_by_itemid(itemid)
        response_json = response.json()
        self.code = response_json['code']
        if 200 == self.code:
            self.title = response_json['data']['item_info']['title']
            self.shop_name = response_json['data']['item_info']['nick']
            self.selled_goods_count = response_json['data']['item_info']['volume']
            self.small_images = response_json['data']['item_info']['small_images']['string']
            self.pict_url = response_json['data']['item_info']['pict_url']
            if response_json['data']['item_info']['user_type'] == 1:
                self.shop_type = '天猫'
            else:
                self.shop_type = '淘宝'
            self.item_id = response_json['data']['item_id']
            self.coupon_start_time = response_json['data']['coupon_start_time'] if response_json['data'].__contains__(
                'coupon_start_time') else ''
            self.coupon_end_time = response_json['data']['coupon_end_time'] if response_json['data'].__contains__(
                'coupon_end_time') else ''
            self.has_coupon = response_json['data']['has_coupon'] if response_json['data'].__contains__(
                'has_coupon') else ''
            self.ori_price = float(response_json['data']['item_info']['zk_final_price'])
            self.max_commission_rate = float(response_json['data']['max_commission_rate'])
            if self.has_coupon:
                self.quanzhi = float(response_json['data']['youhuiquan'])
                self.fanxian = round((self.ori_price - self.quanzhi) * self.max_commission_rate / 100.0, 2)
            else:
                self.quanzhi = 0
                self.fanxian = round(self.ori_price * self.max_commission_rate / 100.0, 2)
            self.mykoulin = response_json['data']['tpwd_simple']
            self.tar_price = round(self.ori_price - self.quanzhi, 2)
            self.final_price = round(self.tar_price - self.fanxian, 2)
            # todo 此处的前端详情页要接收淘口令去走接口拿同样的数据显示在页面.因为不知道如何把json对象包在链接里,后期优化建议是用户查询数据后存在数据库,详情页直接取数据库不走云商接口.
            self.url = details_url + str(self.item_id) + '&username=' + str(self.username)

    def handle_to_str(self):
        '''
        因为发现在用户页复制如下口令,无法生效.但是单独复制口令是可以的.所以放弃改方案.用网页.
        :return:
        '''
        if 200 == self.code:
            return '''★原价: ￥ {}
★优惠券: [红包]￥ {}
★券后价: ￥ {}
★额外返现: ￥ {}
复制本条消息,打开[手机淘宝],领券
-------------------
{}
-------------------'''.format(self.ori_price, self.quanzhi, self.tar_price, self.fanxian, self.mykoulin)
        else:
            return '该商品没有返利，换一个试试吧'

    def result(self):
        return '''【97go】优惠券￥{} 返利红包￥{} 到手价￥{}'''.format(self.quanzhi, self.fanxian, self.final_price)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class RecommendItem:
    def __init__(self, item):
        self.title = item['title']
        self.selled_goods_count = item['volume']
        self.pict_url = item['pict_url']
        if item['user_type'] == 1:
            self.shop_type = '天猫'
        else:
            self.shop_type = '淘宝'
        self.item_id = item['num_iid']
        self.shop_name = item['shop_title']
        self.ori_price = float(item['zk_final_price'])
        self.max_commission_rate = float(item['commission_rate'])
        self.quanzhi = float(item['youhuiquan'])
        self.fanxian = round((self.ori_price - self.quanzhi) * self.max_commission_rate / 10000.0, 2)
        self.tar_price = round(self.ori_price - self.quanzhi, 2)
        self.final_price = round(self.tar_price - self.fanxian, 2)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class RecommendResult:
    '''
    商品详情页的更多推荐
    苹果12钢化水凝膜苹果
1.5m加长2米3米iPhone6数据线6s苹果5s手机7Plus充电线器7P8X超长3m快充Xs原裝正品ipad
    '''

    def __init__(self, keyword):
        response = maybe_u_like_by_keyword(keyword)
        response_json = response.json()
        self.code = response_json['code']
        results = []
        if 200 == self.code:
            for item in response_json['data']:
                if 'youhuiquan' in item.keys():
                    recommend_item = RecommendItem(item)
                    results.append(recommend_item.to_json())
        self.results = results

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


if __name__ == '__main__':
    keyword = maybe_u_like_by_keyword('')
    json = keyword.json()
    print()
    order_thread()
    share_url = '哈哈￥QykNcCn5zZh￥'
    share_url = '苹果12钢化水凝膜苹果X/xr/xs/全屏覆盖iphone7/8/plus偷窥全包边iphone11pro max磨砂纳米手机软膜抗蓝光max'
    print((share_url[0:5]))
    # response = query_goods_by_id('571900197140')
    # response = query_youhui_by_itemid('634753362776')
    # t_result = TextResult(share_url)
    # to_str = t_result.handle_to_str()
    # print(to_str)
    response = query_youhui_by_tpwdcode(share_url)
    # response = maybe_u_like_by_keyword('AirPods')
    # response = order_thread()
    response_json = response.json()
    print(response.json())
