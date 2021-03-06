import datetime

# from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from WeiXinCore.WeiXin import *
from WeiXinCore.WeiXinMsg import WeiXinMsg
from WeiXinCore.real import TextResult

app = Flask(__name__)
ctx = app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ssss2222@116.63.138.138:3306/kappa?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 开启sql语句的显示
app.config['SQLALCHEMY_ECHO'] = True
# 继承db.model 是为了方便操作数据库
# 注册数据库连接
db = SQLAlchemy(app)


class Upcommand(db.Model):
    __tablename = 'upcommand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    version = db.Column(db.String(256), nullable=True)
    feature = db.Column(db.String(256), nullable=True)
    command = db.Column(db.String(256), nullable=True)
    repeatable = db.Column(db.String(256), nullable=True)
    envs = db.Column(db.String(256), nullable=True)
    command_index = db.Column(db.String(256), nullable=True)

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


class Env(db.Model):
    __tablename = 'env'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    env = db.Column(db.String(256), nullable=True)
    now_version = db.Column(db.String(256), nullable=True)
    to_version = db.Column(db.String(256), nullable=True)
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
#         return item

tk_status_map = {'12': '付款', '13': '关闭', '14': '确认收货', '3': '结算成功'}
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
    now = time.strftime("%Y-%m-%d+%H:%M:%S", time.localtime())
    before = (datetime.datetime.now() - datetime.timedelta(minutes=20)).strftime("%Y-%m-%d+%H:%M:%S")
    # before = '2021-03-03+08:44:27'
    # now = '2021-03-03+08:45:27'

    order_response = requests.get(
        'http://api.web.ecapi.cn/taoke/tbkOrderDetailsGet?apkey={}&end_time={}&start_time={}&tbname={}&page_size=100'.format(
            apkey, now, before, tbname))
    order_json = order_response.json()
    if order_json['code'] == 200:
        list_ = order_json['data']['list']
        for item in list_:
            # 判断是否存在于订单表.不存在就插入订单表
            trade_parent_id__firstOrder = Order.query.filter_by(trade_parent_id=item['trade_parent_id']).first()
            if trade_parent_id__firstOrder:
                print(item['trade_parent_id'], 'already in db.')
            else:
                # 找出这个订单属于谁.默认给离付款时间最近发送过该itemid的人
                first = CopyTwdRecord.query.filter_by(item_id=item['item_id']).order_by(
                    CopyTwdRecord.create_time.desc()).first()
                if first:
                    order = Order(username=first.username,
                                  item_id=item['item_id'],
                                  pic_url=item['item_img'],
                                  shop_type=item['order_type'],
                                  item_title=item['item_title'],
                                  paid_time=item['tk_paid_time'],
                                  order_status='已付款' if item['tk_status'] == 12 else item['tk_status'],
                                  sys_status='待提现' if item['tk_status'] == 12 else item['tk_status'],
                                  pay_price=item['alipay_total_price'],
                                  actual_pre_fanli=item['pub_share_pre_fee'],
                                  actual_fanli=item['pub_share_fee'],
                                  trade_parent_id=item['trade_parent_id'],
                                  response_text=str(item))
                else:
                    order = Order(item_id=item['item_id'],
                                  pic_url=item['item_img'],
                                  shop_type=item['order_type'],
                                  item_title=item['item_title'],
                                  paid_time=item['tk_paid_time'],
                                  order_status=item['tk_status'],
                                  sys_status=item['tk_status'],
                                  pay_price=item['alipay_total_price'],
                                  actual_pre_fanli=item['pub_share_pre_fee'],
                                  actual_fanli=item['pub_share_fee'],
                                  trade_parent_id=item['trade_parent_id'],
                                  response_text=str(item))
                db.session.add(order)
                db.session.commit()
                # 新增了订单,就把该用户的待提现金额+=预估金额(金额有改动,就insert到金额的记录表)
                user = User.query.filter_by(username=first.username).first()
                user.dai_tixian = float(user.dai_tixian) + float(order.actual_pre_fanli)
                db.session.commit()
                record = UserMoneyRecord(username=first.username, dai_tixian=order.actual_pre_fanli,
                                         trade_parent_id=item['trade_parent_id'])
                db.session.add(record)
                db.session.commit()


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
        t_result = TextResult(itemid=itemid)
        return jsonify(t_result.to_json())
    return None


@app.route('/wx/order_tx_counts', methods=['GET', 'POST'])
def wx_order_tx_counts():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        order_count = str(Order.query.filter_by(username=openid).count())
        tixian_count = str(TixianRecord.query.filter_by(username=openid).count())
        result = {'order_count': order_count, 'tixian_count': tixian_count}
        return jsonify(result)
    else:
        return None


@app.route('/wx/login_user', methods=['GET', 'POST'])
def wx_login_user():
    req_data = request.get_json(silent=True)
    if req_data:
        code = req_data['code']
        openid = get_openid(code)
        user = judge_user_exsits(openid)
        return jsonify(user.to_json())
    return None


def judge_user_exsits(openid):
    user = User.query.filter_by(username=openid).first()
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
    return user


@app.route('/wx/copy_twd_record', methods=['GET', 'POST'])
def copy_twd_record():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        # 复制淘口令的时候,若用户不在库里,就新建用户
        judge_user_exsits(openid)
        item_id = req_data['item_id']
        copy_twd = CopyTwdRecord(username=openid, item_id=item_id)
        db.session.add(copy_twd)
        db.session.commit()
    return None


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
    thirdorder = request.form.get('thirdorder')
    record = TixianRecord.query.filter_by(thirdorder=thirdorder).first()
    openid = record.username
    jine = record.money
    event = request.form.get('event')
    if 'SUC' in event:
        fafang_status = '已到账'
    else:
        fafang_status = '失败'
        # 失败就把用户的钱再加回来
        # 修改用户的可提现金额
        user = User.query.filter_by(username=openid).first()
        user.ke_tixian = float(user.ke_tixian) + float(jine)
        db.session.commit()
        # 金额有变化,就插到金额变化表
        record = UserMoneyRecord(username=openid, ke_tixian=float(jine))
        db.session.add(record)
        db.session.commit()

    # 无论成功失败都要将结果更新到提现记录表
    orderid = request.form.get('orderid')
    alipay_orderid = request.form.get('alipay_orderid')
    reason = request.form.get('reason')
    record = TixianRecord.query.filter_by(thirdorder=thirdorder).first()
    record.fafang_status = fafang_status
    record.fafang_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    record.orderid = orderid
    record.alipay_orderid = alipay_orderid
    record.reason = reason
    db.session.commit()
    return 'success'


@app.route('/wx/tixian', methods=['GET', 'POST'])
def tixian():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        jine = float(req_data['jine'])
        name = req_data['name']
        account = req_data['account']
        user = User.query.filter_by(username=openid).first()
        # 用户提现的时候,输入的支付宝信息保存一下
        user.alipay_name = name
        user.alipay_account = account
        db.session.commit()
        if float(user.ke_tixian) < jine:
            return None
        else:
            # 给指定支付宝转账
            thirdorder = trans_2_zfb(openid, jine, name, account)
            if thirdorder is not None:
                # 修改用户的可提现金额
                user = User.query.filter_by(username=openid).first()
                user.ke_tixian = float(user.ke_tixian) - float(jine)
                user.yi_tixian = float(user.yi_tixian) + float(jine)
                db.session.commit()
                # 金额有变化,就插到金额变化表
                record = UserMoneyRecord(username=openid, ke_tixian=-float(jine), yi_tixian=float(jine))
                db.session.add(record)
                db.session.commit()
                # 增加提现记录
                tixian_record = TixianRecord(username=openid, money=jine, fafang_status='已提交', thirdorder=thirdorder)
                db.session.add(tixian_record)
                db.session.commit()
                return {'tixian': 'success'}
    return None


@app.route('/wx/getOrders', methods=['GET', 'POST'])
def getOrders():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        orders = Order.query.filter_by(username=openid).all()
        list_result = []
        for order in orders:
            list_result.append(order.to_json())
        return {'results': list_result}
    return None


@app.route('/wx/getTixians', methods=['GET', 'POST'])
def getTixians():
    req_data = request.get_json(silent=True)
    if req_data:
        openid = req_data['openid']
        tixians = TixianRecord.query.filter_by(username=openid).all()
        list_result = []
        for tixian in tixians:
            list_result.append(tixian.to_json())
        return {'results': list_result}
    return None


def get_openid(code):
    code_record = CodeRecord.query.get(code)
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
    return None


def tb_order_status_job():
    """
    查order表状态为已付款的订单,按paid_time智能排序.
    :return:
    """
    orders = Order.query.filter_by(order_status='已付款').order_by(Order.paid_time.asc()).all()
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
            for item in list_:
                # 判断该订单状态是否为12(已付款),不是就更新
                if item['tk_status'] != 12:
                    _order = Order.query.filter_by(trade_parent_id=item['trade_parent_id']).first()
                    _status = tk_status_map[str(item['tk_status'])]
                    _wx_status = wx_status_map[str(item['tk_status'])]
                    _order.order_status = _status
                    _order.sys_status = _wx_status
                    db.session.commit()
                    if item['tk_status'] == 14:
                        # (确认收货)后把金额加到可提现中
                        # 修改用户的可提现金额和待提现金额
                        user = User.query.filter_by(username=_order.username).first()
                        user.dai_tixian = float(user.dai_tixian) - float(_order.actual_pre_fanli)
                        user.ke_tixian = float(user.ke_tixian) + float(_order.actual_pre_fanli)
                        db.session.commit()
                        # 金额有变化,就插到金额变化表
                        record = UserMoneyRecord(username=_order.username, ke_tixian=float(_order.actual_pre_fanli),
                                                 dai_tixian=-float(_order.actual_pre_fanli),
                                                 trade_parent_id=_order.trade_parent_id)
                        db.session.add(record)
                        db.session.commit()
                    if item['tk_status'] == 3:
                        # (订单关闭)了的话,应追溯该订单号的所有金额来往,还原回去.
                        records = UserMoneyRecord.query.filter_by(trade_parent_id=_order.trade_parent_id).all()
                        for record in records:
                            user = User.query.filter_by(username=_order.username).first()
                            if record.dai_tixian is not None:
                                user.dai_tixian = float(user.dai_tixian) - float(record.dai_tixian)
                            if record.ke_tixian is not None:
                                user.ke_tixian = float(user.ke_tixian) - float(record.ke_tixian)
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


# def tb_order_task():
#     print("tb_order_task start " + str(os.getpid()))
#     scheduler = APScheduler()
#     scheduler.init_app(app)
#     # 淘宝联盟查询订单的定时任务，每隔60s执行1次
#     scheduler.add_job(func=tb_new_order_job, trigger='interval', seconds=60, id='tb_order_task')
#     scheduler.add_job(func=tb_order_status_job, trigger='interval', seconds=300, id='tb_upd_order_status_task')
#     scheduler.start()


# def handle_categary():
#     category = getTbCategory()
#     category_json = category.json()
#     category_list = []
#     for _i in category_json['data']:
#         t = TBcategary(cid=_i['cid'], parent_cid=_i['parent_cid'], name=_i['name'])
#         category_list.append(t)


# 写在main里面，IIS不会运行


# tb_order_task()


@app.route('/list', methods=['GET', 'POST'])
def ks_index():
    upcommand__all = db.session.query(Upcommand).all()
    result_jsons = []
    for command in upcommand__all:
        result_jsons.append(command.to_json())
    return {'result': result_jsons}


@app.route('/list2', methods=['GET', 'POST'])
def ks_index2():
    env_all = db.session.query(Env).all()
    result_jsons = []
    for env in env_all:
        result_jsons.append(env.to_json())
    return {'result': result_jsons}


@app.route('/upd', methods=['GET', 'POST'])
def upd():
    req_data = request.get_json(silent=True)
    data = req_data['data']
    first = db.session.query(Upcommand).filter(Upcommand.id == data['id']).first()
    first.version = data['version']
    first.feature = data['feature']
    first.command = data['command']
    db.session.commit()
    upcommand__all = db.session.query(Upcommand).all()
    result_jsons = []
    for command in upcommand__all:
        result_jsons.append(command.to_json())
    return {'result': result_jsons}


@app.route('/add', methods=['GET', 'POST'])
def add():
    req_data = request.get_json(silent=True)
    data = req_data['data']
    upcommand = Upcommand(version=data['version'], feature=data['feature'], command=data['command'], repeatable=1,
                          envs='所有生产环境')
    db.session.add(upcommand)
    db.session.commit()
    upcommand__all = db.session.query(Upcommand).all()
    result_jsons = []
    for command in upcommand__all:
        result_jsons.append(command.to_json())
    return {'result': result_jsons}


@app.route('/del', methods=['GET', 'POST'])
def delete():
    req_data = request.get_json(silent=True)
    data = req_data['data']
    print('#############', data)
    first = db.session.query(Upcommand).filter(Upcommand.id == data['id']).first()
    db.session.delete(first)
    db.session.commit()
    upcommand__all = db.session.query(Upcommand).all()
    result_jsons = []
    for command in upcommand__all:
        result_jsons.append(command.to_json())
    return {'result': result_jsons}


@app.route('/add2', methods=['GET', 'POST'])
def add2():
    req_data = request.get_json(silent=True)
    data = req_data['data']
    env = Env(env=data['env'])
    db.session.add(env)
    db.session.commit()
    return {'result': 'ok'}


headers = {
    'Cookie': '__tracker_user_id__=2319d2cd4671800-0e9ac0000073-397357270844; experimentation_subject_id=ImVhMjQ5ZDM5LTFkZjYtNGQwNC05YTdkLWIzOGQzYjkyNzdiNyI%3D--ca5f096d0903f902a3bd4ca87fb841e218eb3f03; grafana_auth_account=c8b480b6d97521234460769777ecfbda; yl-fab=""; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Imx2amwiLCJfZmxhZyI6MTYxNjMxMjE5NywiYWNjb3VudCI6Imx2amwifQ.rLWCB3FwPUcvX5Li1Wud8qChtT7I0bqN4OiFR6A4gCA; user_name=lvjl; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Imx2amwiLCJfZmxhZyI6MTYxNjMxMjE5NywiYWNjb3VudCI6Imx2amwifQ.rLWCB3FwPUcvX5Li1Wud8qChtT7I0bqN4OiFR6A4gCA',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac 05 X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}


@app.route('/envs', methods=['GET', 'POST'])
def envs():
    get = requests.get('https://dmp-mop-test.mypaas.com.cn/api/client/list', headers=headers)
    json = get.json()
    items = []
    for item in json['data']:
        items.append({'label': item['env_tag']+'('+item['description']+')', 'value': item['env_tag']+'('+item['description']+')'})
    return {'result': items}


@app.route('/zhixing', methods=['GET', 'POST'])
def add2():
    req_data = request.get_json(silent=True)
    datas = req_data['data']
    for data in datas:
        env = Env(env=data['env'])

    db.session.add(env)
    db.session.commit()
    return {'result': 'ok'}


if __name__ == '__main__':
    # get = requests.get('https://dmp-mop-test.mypaas.com.cn/api/client/list', headers=headers)
    # json = get.json()
    # print()

    # record = UserMoneyRecord(username='oo5JJ5mg3bd1GV1MP0i2hyyHUXtY', ke_tixian=-float('0.1'))
    # db.session.add(record)
    # db.session.commit()
    # trans_2_zfb('0.1','韩旭','18627783779')
    # first = Msg.query.filter_by(item_id='571900197140').order_by(Msg.create_time.desc()).first()
    # user = User.query.filter_by(username='111').first()
    # user_serialize = user.serialize()
    # print()
    app.run(host='0.0.0.0', port=39004)
