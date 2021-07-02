import datetime
import traceback
import pymysql
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time
import os

# api文档:https://www.ecapi.cn/index/index/openapi/id/50.shtml?ptype=1
# 云商数据:https://console.ecapi.cn/dashboard/workplace

apkey = '106dd6f8-103e-f437-6b53-43b80c09ef07'
#tb
pid = 'mm_50401481_2105100471_110937350217'
tbname = 'imc701'
#jd
key_id = 'J4737658254124025'

details_url = 'http://afanxyz.xyz/pages/goodsdetail/goodsdetail?goodsId='
details_urljd = 'http://afanxyz.xyz/pages/goodsdetail/goodsdetailjd?goodsId='
details_urlpdd = 'http://afanxyz.xyz/pages/goodsdetail/goodsdetailpdd?goodsId='
no_youhui_words = '该商品没有返利，换一个试试吧~'


def jd_item_youhui(skuid, username):
    response = requests.get('http://api.web.ecapi.cn/jingdong/getJdUnionItems?apkey={}&skuIds={}'.format(apkey, skuid))
    response_json = response.json()
    if 200 == response_json['code']:
        data = response_json['data']
        if len(data['list']) > 0:
            result_jd = TextResult_JD(data['list'][0], username)
            return result_jd
        else:
            return no_youhui_words
    else:
        return no_youhui_words


def jd_item_youhui_list(keyword, username):
    response = requests.get('http://api.web.ecapi.cn/jingdong/getJdUnionItems?apkey={}&keyword={}&hasBestCoupon=1'.format(apkey, keyword))
    response_json = response.json()
    if 200 == response_json['code']:
        data = response_json['data']
        if len(data['list']) > 0:
            return data['list']
        else:
            return no_youhui_words
    else:
        return no_youhui_words


def pdd_item_youhui(goods_id, username):
    response = requests.get('http://api.web.ecapi.cn/pinduoduo/goodsSearch?apkey={}&keyword={}&pdname=18627783779&pid=13643409_176823327&page=1&page_size=30'.format(apkey, goods_id))
    response_json = response.json()
    if 200 == response_json['code']:
        data = response_json['data']
        if len(data) > 0:
            result_pdd = TextResult_PDD(data['list'][0], username)
            return result_pdd
        else:
            return no_youhui_words
    else:
        return no_youhui_words


def pdd_item_youhui_list(goods_id, username):
    response = requests.get('http://api.web.ecapi.cn/pinduoduo/goodsSearch?apkey={}&keyword={}&pdname=18627783779&with_coupon=true&pid=13643409_176823327&page=1&page_size=30'.format(apkey, goods_id))
    response_json = response.json()
    if 200 == response_json['code']:
        data = response_json['data']
        if len(data['list']) > 0:
            return data['list']
        else:
            return no_youhui_words
    else:
        return no_youhui_words


def tuiguangwei():
    return requests.get('http://api.web.ecapi.cn/jingdong/getUnionPosition?apkey={}&key_id={}&unionType=1&pageIndex=1&pageSize=100'.format(apkey, key_id))


def jd_item_mine(item_url):
    return requests.get('http://api.web.ecapi.cn/jingdong/doItemCpsUrl?autoSearch=1&apkey={}&materialId={}&key_id={}'.format(apkey, urllib.parse.quote(item_url), key_id))


def pdd_item_mine(goods_id):
    return requests.get('http://api.web.ecapi.cn/pinduoduo/createItemPromotionUrl?apkey={}&p_id=13643409_176823327&pdname=18627783779&goods_sign={}'.format(apkey, goods_id))

def find_the_best_jd_quan(item):
    for _j in item['couponInfo']['couponList']:
        if _j['isBest'] == 1:
            return _j
    return ''


def timestamp_to_strtime(timestamp):
    local_str_time = datetime.datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d')
    return local_str_time


def timestamp_to_strtime10(timestamp):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d", time_local)
    return dt

class TextResult_JD:
    def __init__(self, item, username=''):
        self.username = username
        self.code = 200
        self.intext = ''
        self.title = item['skuName']
        self.shop_name = item['shopInfo']['shopName']
        self.selled_goods_count = item['inOrderCount30Days']
        self.small_images = []
        for _i in item['imageInfo']['imageList']:
            self.small_images.append(_i['url'])
        self.pict_url = item['imageInfo']['whiteImage'] if item['imageInfo'].__contains__('whiteImage') else ''
        self.shop_type = '京东'
        self.item_id = item['skuId']
        self.ori_price = float(item['priceInfo']['price'])
        self.max_commission_rate = float(item['commissionInfo']['commissionShare'])
        self.has_coupon = item['couponInfo']['couponList'] if item['couponInfo'].__contains__('couponList') else False
        if self.has_coupon != '' and len(item['couponInfo']['couponList']) > 0:
            quan = find_the_best_jd_quan(item)
            if quan:
                self.has_coupon = True
                self.quan_menkan = quan['quota']
                self.coupon_start_time = timestamp_to_strtime(quan['getStartTime'])
                self.coupon_end_time = timestamp_to_strtime(quan['getEndTime'])
                self.quanzhi = float(quan['discount'])
                self.fanxian = round((self.ori_price - self.quanzhi) * self.max_commission_rate / 100.0, 2)
            else:
                self.has_coupon = False
        if not self.has_coupon:
            self.quanzhi = 0
            self.fanxian = round(self.ori_price * self.max_commission_rate / 100.0, 2)
            self.coupon_start_time = ''
            self.coupon_end_time = ''
        self.mykoulin = ''
        self.tar_price = round(self.ori_price - self.quanzhi, 2)
        self.final_price = round(self.tar_price - self.fanxian, 2)
        if self.username:
            self.url = details_urljd + str(self.item_id) + '&username=' + str(self.username)
        else:
            mine = jd_item_mine('https://wqitem.jd.com/item/view?sku={}'.format(self.item_id))
            mine = mine.json()
            if mine['code'] == 200:
                self.url = mine['data']['shortURL']
            else:
                self.url = ''

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

    def result(self):
        return '''【97go】优惠券￥{} 返利红包￥{} 到手价￥{}'''.format(self.quanzhi, self.fanxian, self.final_price)


class TextResult_PDD:
    def __init__(self, item, username=''):
        self.username = username
        self.code = 200
        self.intext = ''
        self.title = item['goods_name']
        self.goods_sign = item['goods_sign']
        self.shop_name = item['mall_name']
        self.selled_goods_count = item['sales_tip']
        self.small_images = []
        for _i in item['goods_gallery_urls']  if item.__contains__('goods_gallery_urls') else []:
            self.small_images.append(_i)
        self.pict_url = item['goods_image_url']
        if len(self.small_images) < 1:
            self.small_images.append(self.pict_url)
        self.shop_type = '拼多多'
        self.item_id = item['goods_id']
        self.ori_price = round(float(item['min_group_price'])/100, 2)
        self.max_commission_rate = float(item['promotion_rate'])
        self.has_coupon = item['has_coupon']
        if self.has_coupon:
            self.has_coupon = True
            self.quan_menkan = item['coupon_min_order_amount']
            self.coupon_start_time = timestamp_to_strtime10(item['coupon_start_time'])
            self.coupon_end_time = timestamp_to_strtime10(item['coupon_end_time'])
            self.quanzhi = float(item['coupon_discount'])/100
            self.fanxian = round((self.ori_price - self.quanzhi) * self.max_commission_rate / 1000.0, 2)
        if not self.has_coupon:
            self.quanzhi = 0
            self.fanxian = round(self.ori_price * self.max_commission_rate / 1000.0, 2)
            self.coupon_start_time = ''
            self.coupon_end_time = ''
        self.mykoulin = ''
        self.tar_price = round(self.ori_price - self.quanzhi, 2)
        self.final_price = round(self.tar_price - self.fanxian, 2)
        if self.username:
            self.url = details_urlpdd + str(self.item_id) + '&username=' + str(self.username)
        else:
            mine = pdd_item_mine(self.goods_sign)
            mine = mine.json()
            if mine['code'] == 200:
                self.url = mine['data']['url'][0]['mobile_short_url']
            else:
                self.url = ''

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

    def result(self):
        return '''【97go】优惠券￥{} 返利红包￥{} 到手价￥{}'''.format(self.quanzhi, self.fanxian, self.final_price)











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
            self.small_images = response_json['data']['item_info']['small_images']['string'] if response_json['data']['item_info'].__contains__(
                'small_images') else ''
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
                self.fanxian = round((self.ori_price - self.quanzhi) * self.max_commission_rate / 100.0 * 0.7, 2)
            else:
                self.quanzhi = 0
                self.fanxian = round(self.ori_price * self.max_commission_rate / 100.0 * 0.7, 2)
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


class RecommendPddItem:
    def __init__(self, item):
        self.title = item['goods_name']
        self.selled_goods_count = item['sales_tip']
        self.pict_url = item['goods_image_url']
        self.shop_type = '拼多多'
        self.item_id = item['goods_id']
        self.shop_name = item['mall_name']
        self.ori_price = round(float(item['min_group_price'])/100, 2)
        self.max_commission_rate = float(item['promotion_rate'])
        self.quanzhi = float(item['coupon_discount'])/100
        self.fanxian = round((self.ori_price - self.quanzhi) * self.max_commission_rate / 1000.0, 2)
        self.tar_price = round(self.ori_price - self.quanzhi, 2)
        self.final_price = round(self.tar_price - self.fanxian, 2)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class RecommendJdItem:
    def __init__(self, item):
        self.title = item['skuName']
        self.selled_goods_count = item['inOrderCount30Days']
        self.pict_url = item['imageInfo']['whiteImage'] if item['imageInfo'].__contains__('whiteImage') else ''
        self.shop_type = '京东'
        self.item_id = item['skuId']
        self.shop_name = item['shopInfo']['shopName']
        self.ori_price = float(item['priceInfo']['price'])
        self.max_commission_rate = float(item['commissionInfo']['commissionShare'])
        quan = find_the_best_jd_quan(item)
        self.quanzhi = float(quan['discount'])
        self.fanxian = round((self.ori_price - self.quanzhi) * self.max_commission_rate / 100.0, 2)
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


class RecommendPddResult:
    '''
    商品详情页的更多推荐
    苹果12钢化水凝膜苹果
    '''

    def __init__(self, keyword):
        result_list = pdd_item_youhui_list(keyword, '')
        results = []
        if len(result_list) > 0:
            for item in result_list:
                recommend_item = RecommendPddItem(item)
                results.append(recommend_item.to_json())
        self.results = results

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class RecommendJdResult:
    '''
    商品详情页的更多推荐
    '''

    def __init__(self, keyword):
        result_list = jd_item_youhui_list(keyword, '')
        results = []
        if len(result_list) > 0:
            for item in result_list:
                recommend_item = RecommendJdItem(item)
                results.append(recommend_item.to_json())
        self.results = results

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


def jd_copy_url_2_itemid(url):
    try:
        split = url.split('.html')
        return split[0].split('product/')[1]
    except Exception:
        return ''


def pdd_copy_url_2_itemid(url):
    try:
        split = url.split('goods_id=')
        return split[1].split('&')[0]
    except Exception:
        return ''


if __name__ == '__main__':
    now_millis = int(time.time())
    before_millis = str((datetime.datetime.now() - datetime.timedelta(minutes=20)).timestamp()).split('.')[0]

    itemid = pdd_item_mine('161466624757')
    print()

    # response = jd_item_mine('https://wqitem.jd.com/item/view?sku=100016960656')
    response = jd_item_youhui('100014997622')
    response_json = response.json()
    print(response.json())
