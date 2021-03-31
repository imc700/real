import datetime
import smtplib
from email.mime.text import MIMEText

from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from sqlalchemy import extract, or_

from WeiXinCore.WeiXin import *
from WeiXinCore.WeiXinMsg import WeiXinMsg
from WeiXinCore.real import TextResult

app = Flask(__name__)
ctx = app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ssss2222@116.63.138.138:3306/real?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 开启sql语句的显示
# app.config['SQLALCHEMY_ECHO'] = True
# 继承db.model 是为了方便操作数据库
# 注册数据库连接
db = SQLAlchemy(app)


class Msg(db.Model):
    __tablename = 'msg'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), nullable=True)
    intext = db.Column(db.String(256), nullable=True)
    title = db.Column(db.String(256), nullable=True)
    shop_name = db.Column(db.String(256), nullable=True)
    selled_goods_count = db.Column(db.String(256), nullable=True)
    small_images = db.Column(db.String(256), nullable=True)
    pict_url = db.Column(db.String(256), nullable=True)
    shop_type = db.Column(db.String(256), nullable=True)
    item_id = db.Column(db.String(256), nullable=True)
    coupon_start_time = db.Column(db.String(256), nullable=True)
    coupon_end_time = db.Column(db.String(256), nullable=True)
    has_coupon = db.Column(db.String(256), nullable=True)
    ori_price = db.Column(db.String(256), nullable=True)
    max_commission_rate = db.Column(db.String(256), nullable=True)
    quanzhi = db.Column(db.String(256), nullable=True)
    fanxian = db.Column(db.String(256), nullable=True)
    mykoulin = db.Column(db.String(256), nullable=True)
    tar_price = db.Column(db.String(256), nullable=True)
    final_price = db.Column(db.String(256), nullable=True)
    url = db.Column(db.String(256), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class User(db.Model):
    '''
    比如赞助会员只能拥有1个月的钻石权限
    等级的修改也加入到money_record表中,若等级有效期到了,可追溯record表,按时间倒序取第二个.
    '''
    __tablename = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), nullable=True)
    dai_tixian = db.Column(db.String(256), nullable=True)
    ke_tixian = db.Column(db.String(256), nullable=True)
    yi_tixian = db.Column(db.String(256), nullable=True)
    dai_shenhe = db.Column(db.String(256), nullable=True)
    leiji_shouru = db.Column(db.String(256), nullable=True)
    xuyao_tuikuan = db.Column(db.String(256), nullable=True)
    level = db.Column(db.String(256), nullable=True)
    level_dead_line = db.Column(db.String(256), nullable=True)
    alipay_name = db.Column(db.String(256), nullable=True)
    alipay_account = db.Column(db.String(256), nullable=True)
    order_count = db.Column(db.String(256), nullable=True)
    tixian_count = db.Column(db.String(256), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        if "create_time" in item:
            del item["create_time"]
        if "update_time" in item:
            del item["update_time"]
        return item


class UserMoneyRecord(db.Model):
    '''
    用户的每一个字段的金额发生变化,都记录于该表.若发生回退情况,根据订单id回退.
    '''
    __tablename = 'user_money_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), nullable=True)
    dai_tixian = db.Column(db.String(256), nullable=True)
    ke_tixian = db.Column(db.String(256), nullable=True)
    yi_tixian = db.Column(db.String(256), nullable=True)
    dai_shenhe = db.Column(db.String(256), nullable=True)
    leiji_shouru = db.Column(db.String(256), nullable=True)
    xuyao_tuikuan = db.Column(db.String(256), nullable=True)
    trade_parent_id = db.Column(db.String(256), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class CopyTwdRecord(db.Model):
    '''
    用户进入详情页复制淘口令的话,就记录于此方便追踪订单定位.(不能靠消息是因为用户可以直接搜索下单,未发送msg)
    '''
    __tablename = 'copy_twd_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), nullable=True)
    item_id = db.Column(db.String(256), nullable=True)
    item_pic_url = db.Column(db.String(256), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# class TBcategary(db.Model):
#     '''
#     用户进入详情页复制淘口令的话,就记录于此方便追踪订单定位.(不能靠消息是因为用户可以直接搜索下单,未发送msg)
#     '''
#     __tablename = 'tb_categary'
#     cid = db.Column(db.String(64), primary_key=True)
#     parent_cid = db.Column(db.String(64), nullable=True)
#     name = db.Column(db.String(256), nullable=True)
#     create_time = db.Column(db.DateTime, default=datetime.datetime.now)
#     update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
#
#     def to_json(self):
#         """将实例对象转化为json"""
#         item = self.__dict__
#         if "_sa_instance_state" in item:
#             del item["_sa_instance_state"]
#         return item-1 未支付; 0-已支付；1-已成团；2-确认收货；3-审核成功；4-审核失败（不可提现）；5-已经结算；8-非多多进宝商品（无佣金订单）;10-已处罚

pdd_status_map = {'-1': '未支付', '0': '已支付', '2': '确认收货', '3': '审核成功','1':'已成团','4':'审核失败','5':'已经结算','8':'无佣金订单','10':'已处罚'}
tk_status_map = {'12': '付款', '13': '关闭', '14': '确认收货', '3': '结算成功'}
jd_status_map = {'16': '已付款', '17': '已完成', '18': '已结算', '15': '待付款'}
jd_sys_status_map = {'16': '待提现', '17': '可提现', '18': '已结算', '15': '待付款'}
wx_status_map = {'12': '待提现', '13': '关闭', '14': '可提现', '3': '结算成功'}


class Order(db.Model):
    '''
    增加等级机制.增加赞助功能.(接微信支付.连续交易30天可申请给用户发红包权限)(增加等级介绍页面)
    进场即青铜.
    买两单即白银.
    买五单或赞助5块钱即黄金.(新增权限:确认收货五分钟内即可提现.)
    买十单或赞助10块钱即钻石.



    (ps:不同等级的返利比例不同.随等级增加而升高.)
00
    --用户进入网页时,拿到用户openid时就增加一条用户表.

    订单线程每3分钟取一次联盟订单.根据订单状态情况完成以下逻辑:
    淘客订单状态
    12-付款，13-关闭，14-确认收货，3-结算成功


    已付款：指订单已付款，但还未确认收货
        增加:一条订单记录
        更新:用户的dai_tixian += actual_fanli
    已收货：指订单已确认收货，但商家佣金未支付
    已结算：指订单已确认收货，且商家佣金已支付成功
    已失效：指订单关闭/订单佣金小于0.01元，订单关闭主要有：1）买家超时未付款； 2）买家付款前，买家/卖家取消了订单；3）订单付款后发起售中退款成功；3：订单结算，12：订单付款， 13：订单失效，14：订单成功
        增加一条订单记录
    '''
    __tablename = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), nullable=True)
    item_id = db.Column(db.String(256), nullable=True)
    pic_url = db.Column(db.String(256), nullable=True)
    shop_type = db.Column(db.String(256), nullable=True)
    order_from = db.Column(db.String(256), nullable=True)
    item_title = db.Column(db.String(256), nullable=True)
    paid_time = db.Column(db.String(256), nullable=True)
    order_status = db.Column(db.String(256), nullable=True)
    sys_status = db.Column(db.String(256), nullable=True)
    pay_price = db.Column(db.String(256), nullable=True)
    actual_pre_fanli = db.Column(db.String(256), nullable=True)
    actual_fanli = db.Column(db.String(256), nullable=True)
    trade_parent_id = db.Column(db.String(256), nullable=True)
    response_text = db.Column(db.Text(), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 轮询新订单
def tb_new_order_job():
    # now = time.strftime("%Y-%m-%d+%H:%M:%S", time.localtime())
    # before = (datetime.datetime.now() - datetime.timedelta(minutes=20)).strftime("%Y-%m-%d+%H:%M:%S")
    before = '2021-03-29+20:00:27'
    now = '2021-03-29+21:00:27'

    order_response = requests.get(
        'http://api.web.ecapi.cn/taoke/tbkOrderDetailsGet?apkey={}&end_time={}&start_time={}&tbname={}&page_size=100'.format(
            apkey, now, before, tbname))
    order_json = order_response.json()
    if order_json['code'] == 200:
        list_ = order_json['data']['list']
        for item in list_:
            # 判断是否存在于订单表.不存在就插入订单表
            trade_parent_id_firstOrder = db.session.query(Order).filter(Order.trade_parent_id == item['trade_parent_id']).first()
            if trade_parent_id_firstOrder:
                print(item['trade_parent_id'], 'already in db.')
            else:
                trade_parent_id__firstOrder = db.session.query(Order).filter(Order.trade_parent_id == item['trade_parent_id']).first()
                if trade_parent_id__firstOrder is None:
                    print(item['trade_parent_id'], 'not in db.')
                    # 找出这个订单属于谁.默认给离付款时间最近发送过该itemid的人
                    first = db.session.query(CopyTwdRecord).filter(CopyTwdRecord.item_id==item['item_id']).order_by(
                        CopyTwdRecord.create_time.desc()).first()
                    db.session.commit()
                    if first:
                        order = Order(username=first.username,
                                      item_id=item['item_id'],
                                      pic_url=item['item_img'],
                                      shop_type=item['order_type'],
                                      order_from='tb',
                                      item_title=item['item_title'],
                                      paid_time=item['tk_paid_time'],
                                      order_status='已付款' if item['tk_status'] == 12 else item['tk_status'],
                                      sys_status='待提现' if item['tk_status'] == 12 else item['tk_status'],
                                      pay_price=item['alipay_total_price'],
                                      actual_pre_fanli=item['pub_share_pre_fee'],
                                      actual_fanli=item['pub_share_fee'],
                                      trade_parent_id=item['trade_parent_id'],
                                      response_text=str(item))
                        db.session.add(order)
                        db.session.commit()
                        # 新增了订单,就把该用户的待提现金额+=预估金额(金额有改动,就insert到金额的记录表)
                        user = db.session.query(User).filter(User.username==first.username).first()
                        user.dai_tixian = round(float(user.dai_tixian) + float(order.actual_pre_fanli), 2)
                        db.session.commit()
                        record = UserMoneyRecord(username=first.username, dai_tixian=order.actual_pre_fanli,
                                                 trade_parent_id=item['trade_parent_id'])
                        db.session.add(record)
                        db.session.commit()
                    else:
                        print('#####there is a new order but cant find tpwd copyer###'+item['trade_parent_id'])


def pdd_new_order_job():
    now = int(time.time())
    before = str((datetime.datetime.now() - datetime.timedelta(minutes=90)).timestamp()).split('.')[0]

    order_response = requests.get(
        'http://api.web.ecapi.cn/pinduoduo/getOauthIncrementOrderList?apkey={}&start_update_time={}&end_update_time={}&pdname=18627783779'.format(
            apkey, before, now))
    order_json = order_response.json()
    if order_json['code'] == 200:
        list_ = order_json['data']['order_list']
        for item in list_:
            # 判断是否存在于订单表.不存在就插入订单表
            trade_parent_id_firstOrder = db.session.query(Order).filter(Order.trade_parent_id == item['order_sn']).first()
            if trade_parent_id_firstOrder:
                print(item['order_sn'], 'already in db.')
            else:
                trade_parent_id__firstOrder = db.session.query(Order).filter(Order.trade_parent_id == item['order_sn']).first()
                if trade_parent_id__firstOrder is None:
                    print(item['order_sn'], 'not in db.')
                    # 找出这个订单属于谁.默认给离付款时间最近发送过该itemid的人
                    first = db.session.query(CopyTwdRecord).filter(CopyTwdRecord.item_id == item['goods_id']).order_by(
                        CopyTwdRecord.create_time.desc()).first()
                    db.session.commit()
                    if first:
                        order = Order(username=first.username,
                                      item_id=item['goods_id'],
                                      pic_url=item['goods_thumbnail_url'],
                                      shop_type='拼多多',
                                      order_from='pdd',
                                      item_title=item['goods_name'],
                                      paid_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['order_pay_time'])),
                                      order_status='已付款' if item['order_status'] == 0 else item['order_status'],
                                      sys_status='待提现' if item['order_status'] == 0 else item['order_status'],
                                      pay_price=item['order_amount'],
                                      actual_pre_fanli = round(int(item['promotion_amount'])/100.0, 2),
                                      actual_fanli = round(int(item['promotion_amount'])/100.0, 2),
                                      trade_parent_id=item['order_sn'],
                                      response_text=str(item))
                        db.session.add(order)
                        db.session.commit()
                        # 新增了订单,就把该用户的待提现金额+=预估金额(金额有改动,就insert到金额的记录表)
                        user = db.session.query(User).filter(User.username==first.username).first()
                        user.dai_tixian = round(float(user.dai_tixian) + float(order.actual_pre_fanli), 2)
                        db.session.commit()
                        record = UserMoneyRecord(username=first.username, dai_tixian=order.actual_pre_fanli,
                                                 trade_parent_id=item['order_sn'])
                        db.session.add(record)
                        db.session.commit()
                    else:
                        print('#####there is a new order but cant find tpwd copyer###'+item['trade_parent_id'])


def jd_new_order_job():
    now = time.strftime("%Y%m%d%H", time.localtime())
    # now = '2021031213'
    order_response = requests.get(
        'http://api.web.ecapi.cn/jingdong/getJdUnionOrders?apkey={}&time={}&type=1&pageNo=1&pageSize=100&key_id={}'.format(
            apkey, now, key_id))
    order_json = order_response.json()
    if order_json['code'] == 200:
        list = order_json['data']['list']
        for list_ in list:
            for item in list_['skuList']:
                # 判断是否存在于订单表.不存在就插入订单表
                trade_parent_id__firstOrder = db.session.query(Order).filter(Order.trade_parent_id == list_['orderTime']).first()
                db.session.commit()
                if trade_parent_id__firstOrder:
                    print(list_['orderTime'], 'already in db.')
                else:
                    print(list_['orderTime'], 'not in db.')
                    # 找出这个订单属于谁.默认给离付款时间最近发送过该itemid的人
                    first = db.session.query(CopyTwdRecord).filter(CopyTwdRecord.item_id == item['skuId']).order_by(
                        CopyTwdRecord.create_time.desc()).first()
                    db.session.commit()
                    if first:
                        order = Order(username=first.username,
                                      item_id=item['skuId'],
                                      pic_url=first.item_pic_url,
                                      shop_type='京东',
                                      order_from='jd',
                                      item_title=item['skuName'],
                                      paid_time='',
                                      order_status=jd_status_map[str(item['validCode'])],
                                      sys_status=jd_sys_status_map[str(item['validCode'])],
                                      pay_price=item['estimateCosPrice'],
                                      actual_pre_fanli=item['estimateFee'],
                                      actual_fanli=item['actualFee'],
                                      trade_parent_id=str(list_['orderTime'])+'-'+str(item['skuId']),
                                      response_text=str(item))
                        db.session.add(order)
                        db.session.commit()
                        # 新增了订单,就把该用户的待提现金额+=预估金额(金额有改动,就insert到金额的记录表)
                        user = db.session.query(User).filter(User.username==first.username).first()
                        user.dai_tixian = round(float(user.dai_tixian) + float(order.actual_pre_fanli), 2)
                        db.session.commit()
                        record = UserMoneyRecord(username=first.username, dai_tixian=order.actual_pre_fanli,
                                                 trade_parent_id=str(list_['orderTime'])+'-'+str(item['skuId']))
                        db.session.add(record)
                        db.session.commit()
                    else:
                        print('#####there is a new order but cant find tpwd copyer###'+list_['orderTime'])



class CodeRecord(db.Model):
    __tablename = 'code_record'
    code = db.Column(db.String(256), primary_key=True)
    openid = db.Column(db.String(256), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        if "create_time" in item:
            del item["create_time"]
        if "update_time" in item:
            del item["update_time"]
        return item


class TixianRecord(db.Model):
    __tablename = 'tixian_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(256), nullable=True)
    money = db.Column(db.String(256), nullable=True)
    fafang_status = db.Column(db.String(256), nullable=True)
    fafang_time = db.Column(db.String(256), nullable=True)
    alipay_orderid = db.Column(db.String(256), nullable=True)
    orderid = db.Column(db.String(256), nullable=True)
    thirdorder = db.Column(db.String(256), nullable=True)
    reason = db.Column(db.String(256), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


db.create_all()



def record_msg(t_result):
    if t_result.code == 200:
        return Msg(username=str(t_result.username),
                   intext=str(t_result.intext),
                   title=str(t_result.title),
                   shop_name=str(t_result.shop_name),
                   selled_goods_count=str(t_result.selled_goods_count),
                   small_images=None,
                   pict_url=str(t_result.pict_url),
                   shop_type=str(t_result.shop_type),
                   item_id=str(t_result.item_id),
                   coupon_start_time=str(t_result.coupon_start_time),
                   coupon_end_time=str(t_result.coupon_end_time),
                   has_coupon=str(t_result.has_coupon),
                   ori_price=str(t_result.ori_price),
                   max_commission_rate=str(t_result.max_commission_rate),
                   quanzhi=str(t_result.quanzhi),
                   fanxian=str(t_result.fanxian),
                   mykoulin=str(t_result.mykoulin),
                   tar_price=str(t_result.tar_price),
                   final_price=str(t_result.final_price),
                   url=str(t_result.url))
    else:
        return Msg(username=str(t_result.username),
                   intext=str(t_result.intext))


@app.route('/wx', methods=['GET', 'POST'])
def echo():
    if not app.debug and not check_signature(request.args):
        # 不在Debug模式下，则需要验证。
        return ""
    if request.method == 'GET':
        return make_response(request.args.get('echostr', ''))
    else:
        wxmsg = WeiXinMsg(request.data)
        respXml = Response[wxmsg.MsgType](wxmsg) if wxmsg.MsgType in Response else ''
        if isinstance(respXml, tuple):
            response = make_response(respXml[0])
            t_result = respXml[1]
            if t_result:
                db.session.add(record_msg(t_result))
                db.session.commit()
        else:
            response = make_response(respXml)
        response.content_type = 'application/xml'
        return response


@app.route('/tb/details_one', methods=['GET', 'POST'])
def tb_details_one():
    req_data = request.get_json(silent=True)
    if req_data:
        itemid = req_data['itemid']
        print('details_one', itemid)
        t_result = TextResult(itemid=itemid)
        return jsonify(t_result.to_json())
    return ''


@app.route('/jd/details_one', methods=['GET', 'POST'])
def jd_details_one():
    req_data = request.get_json(silent=True)
    if req_data:
        itemid = req_data['itemid']
        print('details_one', itemid)
        t_result = jd_item_youhui(itemid, '')
        return jsonify(t_result.to_json())
    return ''


@app.route('/pdd/details_one', methods=['GET', 'POST'])
def pdd_details_one():
    req_data = request.get_json(silent=True)
    if req_data:
        itemid = req_data['itemid']
        print('pdd_details_one', itemid)
        t_result = pdd_item_youhui(itemid, '')
        return jsonify(t_result.to_json())
    return ''


@app.route('/wx/order_tx_counts', methods=['GET', 'POST'])
def wx_order_tx_counts():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        order_count = str(db.session.query(Order).filter_by(username=openid).count())
        tixian_count = str(db.session.query(TixianRecord).filter_by(username=openid).count())
        result = {'order_count': order_count, 'tixian_count': tixian_count}
        return jsonify(result)
    else:
        return ''


@app.route('/wx/login_user', methods=['GET', 'POST'])
def wx_login_user():
    req_data = request.get_json(silent=True)
    if req_data:
        code = req_data['code']
        openid = get_openid(code)
        user = judge_user_exsits(openid)
        print(user.to_json())
        return jsonify(user.to_json())
    print('login_user nothing')
    return ''


def judge_user_exsits(openid):
    user = db.session.query(User).filter_by(username=openid).first()
    if user:
        print('old')
        # 若不是新用户,就查出订单数和提现数
    else:
        user = User(username=openid,
                    dai_tixian=0,
                    ke_tixian=0,
                    yi_tixian=0,
                    dai_shenhe=0,
                    leiji_shouru=0,
                    xuyao_tuikuan=0,
                    order_count=0,
                    tixian_count=0,
                    level='',
                    level_dead_line='',
                    alipay_name='',
                    alipay_account='')
        db.session.add(user)
        db.session.commit()
        user = db.session.query(User).filter_by(username=openid).first()
    return user


@app.route('/wx/copy_twd_record', methods=['GET', 'POST'])
def copy_twd_record():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        # 复制淘口令的时候,若用户不在库里,就新建用户
        judge_user_exsits(openid)
        item_id = req_data['item_id']
        item_pic_url = req_data['item_pic_url'] if req_data.__contains__('item_pic_url') else ''
        copy_twd = CopyTwdRecord(username=openid, item_id=item_id, item_pic_url=item_pic_url)
        db.session.add(copy_twd)
        db.session.commit()
        return jsonify(copy_twd.to_json())
    return ''


def trans_2_zfb(openid, jine, name, account):
    millis = int(round(time.time() * 1000))
    response = trans_zfb(jine, name, account, millis)
    response_json = response.json()
    print(response_json)
    if response_json['code'] == 200:
        return millis
    return None


@app.route('/result', methods=['GET', 'POST'])
def result():
    thirdorder = request.args.get('thirdorder')
    record = db.session.query(TixianRecord).filter_by(thirdorder=thirdorder).first()
    if '已提交' not in record.fafang_status:
        return 'error.该提现记录已给过结果.'
    openid = record.username
    jine = record.money
    event = request.args.get('event')
    if 'SUC' in event:
        fafang_status = '已到账'
        user = db.session.query(User).filter_by(username=openid).first()
        user.yi_tixian = round(float(user.yi_tixian) + float(jine), 2)
        user.dai_shenhe = round(float(user.dai_shenhe) - float(jine), 2)
        db.session.commit()
        record = UserMoneyRecord(username=openid, yi_tixian=float(jine), dai_shenhe=-float(jine))
        db.session.add(record)
        db.session.commit()
    else:
        fafang_status = '失败'
        # 失败就把用户的钱再加回来
        # 修改用户的可提现金额
        user = db.session.query(User).filter_by(username=openid).first()
        user.ke_tixian = round(float(user.ke_tixian) + float(jine), 2)
        # user.yi_tixian = round(float(user.yi_tixian) - float(jine), 2)
        user.dai_shenhe = round(float(user.dai_shenhe) - float(jine), 2)
        db.session.commit()
        # 金额有变化,就插到金额变化表
        record = UserMoneyRecord(username=openid, ke_tixian=float(jine), dai_shenhe=-float(jine))
        db.session.add(record)
        db.session.commit()

    # 无论成功失败都要将结果更新到提现记录表
    # orderid = request.form.get('orderid')
    # alipay_orderid = request.form.get('alipay_orderid')
    # reason = request.form.get('reason')
    record = db.session.query(TixianRecord).filter_by(thirdorder=thirdorder).first()
    record.fafang_status = fafang_status
    record.fafang_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # record.orderid = orderid
    # record.alipay_orderid = alipay_orderid
    # record.reason = reason
    db.session.commit()
    return 'success'


def send_mail(title, content, millis_email):
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "imc700@163.com"  # 用户名
    mail_pass = "EARNLXZLZYSRXKQL"  # 密码(这里的密码不是登录邮箱密码，而是授权码)

    sender = 'imc700@163.com'  # 发件人邮箱
    receivers = ['imc701@163.com', 'imc700@qq.com']  # 接收人邮箱

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)
    return millis_email


@app.route('/wx/tixian', methods=['GET', 'POST'])
def tixian():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        try:
            jine = float(req_data['jine'])
        except Exception as e:
            return {'tixian': '小鬼,别闹.'}
        name = req_data['name']
        account = req_data['account']
        user = db.session.query(User).filter_by(username=openid).first()
        # 用户提现的时候,输入的支付宝信息保存一下
        user.alipay_name = name
        user.alipay_account = account
        db.session.commit()
        if float(user.ke_tixian) < jine:
            return {'tixian': '可提现余额不足'}
        else:
            # 给指定支付宝转账
            # thirdorder = trans_2_zfb(openid, jine, name, account)
            millis_email = int(round(time.time() * 1000))
            thirdorder = send_mail('97go_zfb_'+str(user.ke_tixian), user.username+'\n'+str(jine)+'\n'+str(name)+'\n'+str(account)+'\n\n'+'http://afanxyz.xyz:39004/result?thirdorder='+str(millis_email)+'&event=SUCCESS'+'\n\n'+'http://afanxyz.xyz:39004/result?thirdorder='+str(millis_email)+'&event=FAIL', millis_email)
            if thirdorder is not None:
                # 修改用户的可提现金额
                user = db.session.query(User).filter_by(username=openid).first()
                user.ke_tixian = round(float(user.ke_tixian) - float(jine), 2)
                # user.yi_tixian = round(float(user.yi_tixian) + float(jine), 2)
                user.dai_shenhe = round(float(user.dai_shenhe) + float(jine), 2)
                db.session.commit()
                # 金额有变化,就插到金额变化表
                record = UserMoneyRecord(username=openid, ke_tixian=-float(jine), dai_shenhe=float(jine))
                db.session.add(record)
                db.session.commit()
                # 增加提现记录
                tixian_record = TixianRecord(username=openid, money=jine, fafang_status='已提交', thirdorder=thirdorder)
                db.session.add(tixian_record)
                db.session.commit()
                return {'tixian': '申请成功'}
            else:
                return {'tixian': '申请失败'}
    return ''


@app.route('/wx/getOrders', methods=['GET', 'POST'])
def getOrders():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        orders = db.session.query(Order).filter_by(username=openid).all()
        list_result = []
        for order in orders:
            list_result.append(order.to_json())
        return {'results': list_result}
    print('getOrders nothing')
    return ''


@app.route('/wx/getTixians', methods=['GET', 'POST'])
def getTixians():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        tixians = db.session.query(TixianRecord).filter_by(username=openid).all()
        list_result = []
        for tixian in tixians:
            list_result.append(tixian.to_json())
        return {'results': list_result}
    return ''


def get_openid(code):
    code_record = db.session.query(CodeRecord).get(code)
    if code_record:
        openid = code_record.openid
        print('use the old openid')
    else:
        t_result = requests.get(
            'https://api.weixin.qq.com/sns/oauth2/access_token?appid=' + appid + '&secret=' + secret + '&code=' + code + '&grant_type=authorization_code')
        result_json = t_result.json()
        openid = result_json['openid']
        code_record = CodeRecord(code=code, openid=openid)
        db.session.add(code_record)
        db.session.commit()
        print('use the new openid')
    return openid


@app.route('/tb/details_many', methods=['GET', 'POST'])
def tb_details_many():
    req_data = request.get_json(silent=True)
    if req_data:
        keyword = req_data['keyword']
        if len(keyword) > 30:
            # keyword = keyword[0:int(round(len(keyword) / 2, 0))]
            keyword = keyword[0:30]
        t_result = RecommendResult(keyword)
        return jsonify(t_result.to_json())
    return ''


@app.route('/pdd/details_many', methods=['GET', 'POST'])
def pdd_details_many():
    req_data = request.get_json(silent=True)
    if req_data:
        keyword = req_data['keyword']
        if len(keyword) > 30:
            keyword = keyword[0:30]
        t_result = RecommendPddResult(keyword)
        return jsonify(t_result.to_json())
    return ''


@app.route('/jd/details_many', methods=['GET', 'POST'])
def jd_details_many():
    req_data = request.get_json(silent=True)
    if req_data:
        keyword = req_data['keyword']
        if len(keyword) > 30:
            keyword = keyword[0:30]
        t_result = RecommendJdResult(keyword)
        return jsonify(t_result.to_json())
    return ''


def juege_order_exist(orders, trade_parent_id, _status):
    for order in orders:
        if order.trade_parent_id == trade_parent_id and _status in order.order_status:
            return True
    return False


def find_dif_status_order(list_):
    trade_ids = []
    new_items = []
    for _t in list_:
        trade_ids.append(_t['trade_parent_id'])
    trade_ids = tuple(trade_ids)
    orders = db.session.query(Order).filter(Order.trade_parent_id.in_(trade_ids)).all()
    for item in list_:
        # 判断这个item跟系统的order的状态是否一致,若不一致,就加入到new_items
        _status = tk_status_map[str(item['tk_status'])]
        trade_parent_id = item['trade_parent_id']
        if not juege_order_exist(orders, trade_parent_id, _status):
            new_items.append(item)
    db.session.commit()
    return new_items


def find_dif_status_pdd_order(list_):
    trade_ids = []
    new_items = []
    for _t in list_:
        trade_ids.append(_t['order_sn'])
    trade_ids = tuple(trade_ids)
    orders = db.session.query(Order).filter(Order.trade_parent_id.in_(trade_ids)).all()
    for item in list_:
        # 判断这个item跟系统的order的状态是否一致,若不一致,就加入到new_items
        _status = pdd_status_map[str(item['order_status'])]
        trade_parent_id = item['order_sn']
        if not juege_order_exist(orders, trade_parent_id, _status):
            new_items.append(item)
    db.session.commit()
    return new_items


def any_timestamp_to_strtime(timestamp, strformat):
    local_str_time = datetime.datetime.fromtimestamp(float(timestamp) / 1000.0).strftime(strformat)
    return local_str_time

def tb_order_status_job():
    """
    查order表状态为已付款的订单,按paid_time智能排序.
    :return:
    """
    orders = db.session.query(Order).filter_by(order_status='已付款', order_from='tb').order_by(Order.paid_time.asc()).all()
    db.session.commit()
    list = []
    trade_id_status = {}
    for order in orders:
        trade_id_status[order.trade_parent_id] = order.order_status
        list.append(datetime.datetime.strptime(order.paid_time, '%Y-%m-%d %H:%M:%S'))
    final_list = group_time(list)
    for time_group in final_list:
        now = time_group[1]
        before = time_group[0]
        order_response = requests.get(
            'http://api.web.ecapi.cn/taoke/tbkOrderDetailsGet?apkey={}&end_time={}&start_time={}&tbname={}&page_size=100'.format(
                apkey, now, before, tbname))
        order_json = order_response.json()
        if order_json['code'] == 200:
            list_ = order_json['data']['list']
            # 把_list与当前订单状态一致的,直接从_list删除
            list_ = find_dif_status_order(list_)
            for item in list_:
                # 判断该订单状态是否为12(已付款),不是就更新
                if item['tk_status'] != 12:
                    _order = db.session.query(Order).filter_by(trade_parent_id=item['trade_parent_id']).first()
                    db.session.commit()
                    _status = tk_status_map[str(item['tk_status'])]
                    _wx_status = wx_status_map[str(item['tk_status'])]
                    _order.order_status = _status
                    _order.sys_status = _wx_status
                    db.session.commit()
                    if item['tk_status'] == 14 or item['tk_status'] == 3:
                        # (确认收货)后把金额加到可提现中_____2021年03月11日10:43:12因余悦的牙刷单发现淘宝会出现确认收货直接就是结算状态.所以此处加逻辑
                        # 修改用户的可提现金额和待提现金额
                        userMoneyRecord = db.session.query(UserMoneyRecord).filter_by(trade_parent_id=_order.trade_parent_id).order_by(UserMoneyRecord.create_time.desc()).first()
                        db.session.commit()
                        if userMoneyRecord is not None and userMoneyRecord.ke_tixian is not None:
                            continue
                        else:
                            user = db.session.query(User).filter_by(username=_order.username).first()
                            user.dai_tixian = round(float(user.dai_tixian) - float(_order.actual_pre_fanli), 2)
                            user.ke_tixian = round(float(user.ke_tixian) + float(_order.actual_pre_fanli), 2)
                            db.session.commit()
                            # 金额有变化,就插到金额变化表
                            record = UserMoneyRecord(username=_order.username, ke_tixian=float(_order.actual_pre_fanli), dai_tixian=-float(_order.actual_pre_fanli), trade_parent_id=_order.trade_parent_id)
                            db.session.add(record)
                            db.session.commit()
                    if item['tk_status'] == 13:
                        # (订单关闭)了的话,应追溯该订单号的所有金额来往,还原回去.
                        records = db.session.query(UserMoneyRecord).filter_by(trade_parent_id=_order.trade_parent_id).all()
                        db.session.commit()
                        for record in records:
                            user = db.session.query(User).filter_by(username=_order.username).first()
                            if record.dai_tixian is not None:
                                user.dai_tixian = round(float(user.dai_tixian) - float(record.dai_tixian), 2)
                            if record.ke_tixian is not None:
                                user.ke_tixian = round(float(user.ke_tixian) - float(record.ke_tixian), 2)
                            db.session.commit()


def pdd_order_status_job():
    """
    查order表状态为已付款的订单,按paid_time智能排序.
    :return:
    """
    orders = db.session.query(Order).filter(Order.order_from=='pdd').filter(or_(Order.order_status.like('已付款'), Order.order_status.like('已成团'), Order.order_status.like('1'))).order_by(Order.paid_time.asc()).all()
    db.session.commit()
    list = []
    trade_id_status = {}
    for order in orders:
        trade_id_status[order.trade_parent_id] = order.order_status
        list.append(datetime.datetime.strptime(order.paid_time, '%Y-%m-%d %H:%M:%S'))
    final_list = group_time(list)
    for time_group in final_list:
        flag_now = time_group[1]
        now = time_group[1]
        before = time_group[0]
        now = (datetime.datetime.strptime(now, '%Y-%m-%d+%H:%M:%S') + datetime.timedelta(minutes=10)).strftime('%Y-%m-%d+%H:%M:%S')
        now = str(datetime.datetime.strptime(now, '%Y-%m-%d+%H:%M:%S').timestamp()).split('.')[0]
        before = str(datetime.datetime.strptime(before, '%Y-%m-%d+%H:%M:%S').timestamp()).split('.')[0]
        order_response = requests.get(
            'http://api.web.ecapi.cn/pinduoduo/getOauthIncrementOrderList?apkey={}&start_update_time={}&end_update_time={}&pdname=18627783779'.format(
                apkey, before, now))
        order_json = order_response.json()
        if order_json['code'] == 200:
            list_ = order_json['data']['order_list']
            print(flag_now, 'pdd当前时段查到订单数量为:', len(list_))
            # 把_list与当前订单状态一致的,直接从_list删除
            list_ = find_dif_status_pdd_order(list_)
            print(flag_now, 'pdd当前时段跟库里比对后查到订单状态有变化的数量为:', len(list_))
            for item in list_:
                # 判断该订单状态是否为12(已付款),不是就更新
                _order = db.session.query(Order).filter_by(trade_parent_id=item['order_sn']).first()
                db.session.commit()
                _status = pdd_status_map[str(item['order_status'])]
                _wx_status = _status
                _order.order_status = _status
                _order.sys_status = _wx_status
                _order.paid_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['order_modify_at']))
                db.session.commit()
                if item['order_status'] == 2 or item['order_status'] == 5:
                    # (确认收货)后把金额加到可提现中_____2021年03月11日10:43:12因余悦的牙刷单发现淘宝会出现确认收货直接就是结算状态.所以此处加逻辑
                    # 修改用户的可提现金额和待提现金额
                    userMoneyRecord = db.session.query(UserMoneyRecord).filter_by(trade_parent_id=_order.trade_parent_id).order_by(UserMoneyRecord.create_time.desc()).first()
                    db.session.commit()
                    if userMoneyRecord is not None and userMoneyRecord.ke_tixian is not None:
                        continue
                    else:
                        user = db.session.query(User).filter_by(username=_order.username).first()
                        user.dai_tixian = round(float(user.dai_tixian) - float(_order.actual_pre_fanli), 2)
                        user.ke_tixian = round(float(user.ke_tixian) + float(_order.actual_pre_fanli), 2)
                        db.session.commit()
                        # 金额有变化,就插到金额变化表
                        record = UserMoneyRecord(username=_order.username, ke_tixian=float(_order.actual_pre_fanli), dai_tixian=-float(_order.actual_pre_fanli), trade_parent_id=_order.trade_parent_id)
                        db.session.add(record)
                        db.session.commit()
                if item['order_status'] == 4 or item['order_status'] == 8:
                    # (订单关闭)了的话,应追溯该订单号的所有金额来往,还原回去.
                    records = db.session.query(UserMoneyRecord).filter_by(trade_parent_id=_order.trade_parent_id).all()
                    db.session.commit()
                    for record in records:
                        user = db.session.query(User).filter_by(username=_order.username).first()
                        if record.dai_tixian is not None:
                            user.dai_tixian = round(float(user.dai_tixian) - float(record.dai_tixian), 2)
                        if record.ke_tixian is not None:
                            user.ke_tixian = round(float(user.ke_tixian) - float(record.ke_tixian), 2)
                        db.session.commit()


def find_jd_dif_order_status(trade_parent_id, items, trade_id_status):
    new_items = []
    for item in items:
        if trade_id_status[str(trade_parent_id) + '-' + str(item['skuId'])] != jd_status_map[str(item['validCode'])]:
            new_items.append(item)
    return new_items


def jd_order_status_job():
    """
    查order表状态为已付款的订单,按paid_time智能排序.
    :return:
    """
    orders = db.session.query(Order).filter_by(order_status='已付款', order_from='jd').order_by(Order.paid_time.asc()).all()
    db.session.commit()
    list = []
    trade_id_status = {}
    for order in orders:
        trade_id_status[order.trade_parent_id] = order.order_status
        list.append(any_timestamp_to_strtime(order.trade_parent_id.split('-')[0], '%Y%m%d%H'))
    final_list = set(list)
    for now in final_list:
        order_response = requests.get(
            'http://api.web.ecapi.cn/jingdong/getJdUnionOrders?apkey={}&time={}&type=1&pageNo=1&pageSize=100&key_id={}'.format(
                apkey, now, key_id))
        order_json = order_response.json()
        if order_json['code'] == 200:
            list = order_json['data']['list']
            for list_ in list:
                # 选出与库里状态不同的进行接下来的处理
                dif_status_items = find_jd_dif_order_status(list_['orderTime'], list_['skuList'], trade_id_status)
                for item in dif_status_items:
                    # 判断该订单状态是否为12(已付款),不是就更新
                    if int(item['validCode']) != 16:
                        _order = db.session.query(Order).filter_by(trade_parent_id=str(list_['orderTime']) + '-' + str(item['skuId'])).first()
                        db.session.commit()
                        _status = jd_status_map[str(item['validCode'])]
                        _wx_status = jd_sys_status_map[str(item['validCode'])]
                        _order.order_status = _status
                        _order.sys_status = _wx_status
                        db.session.commit()
                        if int(item['validCode']) == 17:
                            # (确认收货)后把金额加到可提现中
                            # 修改用户的可提现金额和待提现金额
                            user = db.session.query(User).filter_by(username=_order.username).first()
                            user.dai_tixian = round(float(user.dai_tixian) - float(_order.actual_pre_fanli), 2)
                            user.ke_tixian = round(float(user.ke_tixian) + float(_order.actual_pre_fanli), 2)
                            db.session.commit()
                            # 金额有变化,就插到金额变化表
                            record = UserMoneyRecord(username=_order.username, ke_tixian=float(_order.actual_pre_fanli),
                                                     dai_tixian=-float(_order.actual_pre_fanli),
                                                     trade_parent_id=_order.trade_parent_id)
                            db.session.add(record)
                            db.session.commit()
                        if int(item['validCode']) < 15:
                            # (订单关闭)了的话,应追溯该订单号的所有金额来往,还原回去.
                            records = db.session.query(UserMoneyRecord).filter_by(trade_parent_id=_order.trade_parent_id).all()
                            db.session.commit()
                            for record in records:
                                user = db.session.query(User).filter_by(username=_order.username).first()
                                if record.dai_tixian is not None:
                                    user.dai_tixian = round(float(user.dai_tixian) - float(record.dai_tixian), 2)
                                if record.ke_tixian is not None:
                                    user.ke_tixian = round(float(user.ke_tixian) - float(record.ke_tixian), 2)
                                db.session.commit()



def group_time(list):
    new_list = []
    for i in list:
        if i.strftime('%Y-%m-%d %H:%M:%S') in time_2_str_list(new_list):
            continue
        _max = i + datetime.timedelta(minutes=178)
        _list = []
        for j in list:
            if j.strftime('%Y-%m-%d %H:%M:%S') in time_2_str_list(new_list):
                continue
            else:
                if j < _max:
                    _list.append(j)
                else:
                    break
        new_list.append(_list)
    # 此时new_list已经分好组了,再取每个组的第一个值和最后一个值.
    final_list = []
    for zu in new_list:
        _t_list = [(zu[0] - datetime.timedelta(minutes=1)).strftime('%Y-%m-%d+%H:%M:%S'),
                   zu[-1].strftime('%Y-%m-%d+%H:%M:%S')]
        final_list.append(_t_list)
    return final_list


def time_2_str_list(new_list):
    str_time_list = []
    for x in new_list:
        for y in x:
            stry = y.strftime('%Y-%m-%d %H:%M:%S')
            str_time_list.append(stry)
    return str_time_list


def tb_order_task():
    print("task start " + str(os.getpid()))
    scheduler = APScheduler()
    scheduler.init_app(app)
    # 淘宝联盟查询订单的定时任务，每隔60s执行1次
    scheduler.add_job(func=tb_new_order_job, trigger='interval', seconds=60, id='tb_order_task')
    scheduler.add_job(func=tb_order_status_job, trigger='interval', seconds=300, id='tb_upd_order_status_task')
    scheduler.add_job(func=jd_new_order_job, trigger='interval', seconds=60, id='jd_order_task')
    scheduler.add_job(func=jd_order_status_job, trigger='interval', seconds=300, id='jd_upd_order_status_task')
    scheduler.add_job(func=pdd_new_order_job, trigger='interval', seconds=60, id='pdd_order_task')
    scheduler.add_job(func=pdd_order_status_job, trigger='interval', seconds=300, id='pdd_upd_order_status_task')
    scheduler.start()


tb_new_order_job()

# 写在main里面，IIS不会运行
# tb_order_task()




if __name__ == '__main__':



    # zhuanba_task()
    # print()
    # jd_new_order_job()
    # float___ = round(float('1.23') + float('1.11'), 2)
    # tb_new_order_job()
    print('app start...')
    app.run(host='0.0.0.0', port=39004)
