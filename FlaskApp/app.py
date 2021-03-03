import datetime

from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from WeiXinCore.WeiXin import *
from WeiXinCore.WeiXinMsg import WeiXinMsg
from WeiXinCore.real import TextResult

app = Flask(__name__)
ctx = app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ssss2222@116.63.138.138:3306/real?charset=utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 开启sql语句的显示
app.config['SQLALCHEMY_ECHO'] = True
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
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


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
def tb_order_job():
    now = time.strftime("%Y-%m-%d+%H:%M:%S", time.localtime())
    before = (datetime.datetime.now() - datetime.timedelta(minutes=20)).strftime("%Y-%m-%d+%H:%M:%S")
    # before = '2021-03-03+08:00:00'
    # now = '2021-03-03+10:00:00'

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
                                  order_status=item['tk_status'],
                                  sys_status=item['tk_status'],
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
                UserMoneyRecord(username=first.username, dai_tixian=order.actual_pre_fanli, trade_parent_id=item['trade_parent_id'])
    return None



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
    in_out = db.Column(db.String(256), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


db.create_all()


#
#
# class LoginForm(FlaskForm):
#     username = StringField('账户名：', validators=[DataRequired(), Length(1, 30)])
#     password = PasswordField('密码：', validators=[DataRequired(), Length(1, 64)])
#     remember_me = BooleanField('记住密码', validators=[Optional()])
#
#
# login_manager_local = login_manager.LoginManager()
# login_manager_local.init_app(app)
# login_manager_local.session_protection = 'strong'
# login_manager_local.login_view = 'login'
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     print(1)
#     if request.method == 'GET':
#         print(2)
#         form = LoginForm()
#         return render_template('login.html', form=form)
#     else:
#         print(3)
#         form = LoginForm(request.form)
#         if form.validate():
#             username = request.form['name']
#             pwd = request.form['pwd']
#             user = User.query_by_username(username)
#
#             if user and user.verify_password(pwd):
#                 login_user(user)
#                 return 'login ok'
#         else:
#             print(form.errors)
#         return render_template('login.html', form=form)
#
# @app.route("/testWXLoginOrRegister",methods=["GET"])
# def test_wx_login_or_register():
#     """
#     测试微信登陆注册
#     :return:
#     """
#     # 前端获取到的临时授权码
#     code = request.args.get("code")
#     # 标识web端还是app端登陆或注册
#     flag = request.args.get("flag")
#
#     # 参数错误
#     if code is None or flag is None:
#         return "参数错误"
#
#     # 获取微信用户授权码
#     access_code = get_access_code(code=code, flag=flag)
#     if access_code is None:
#         return "获取微信授权失败"
#
#     # 获取微信用户信息
#     wx_user_info = get_wx_user_info(access_data=access_code)
#     if wx_user_info is None:
#         return "获取微信授权失败"
#
#     # 验证微信用户信息本平台是否有，
#     data = login_or_register(wx_user_info=wx_user_info)
#     if data is None:
#         return "登陆失败"
#     return data
#
# @app.route('/')
# @login_required
# def index():
#     return "Hello, World!"

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
        print(respXml)
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
        print(1)
        print(code)
        openid = get_openid(code)
        print(2)
        print(openid)
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
    return None\


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
        print(result_json)
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


def tb_order_job2():
    # todo 买云商的v1会员,然后走订单接口.(注意防止漏掉或者多查),防漏就获取近5分钟的订单,多查就定义个全局set.
    results = [{}]
    orders = Order.query.all()


def tb_order_task():
    print("task start " + str(os.getpid()))
    scheduler = APScheduler()
    scheduler.init_app(app)
    # 淘宝联盟查询订单的定时任务，每隔60s执行1次
    scheduler.add_job(func=tb_order_job, trigger='interval', seconds=60, id='tb_order_task')
    scheduler.start()


# 写在main里面，IIS不会运行
# tb_order_task()


if __name__ == '__main__':
    # tb_order_job()
    # first = Msg.query.filter_by(item_id='571900197140').order_by(Msg.create_time.desc()).first()
    # user = User.query.filter_by(username='111').first()
    # user_serialize = user.serialize()
    # print()
    app.run(host='0.0.0.0', port=39004)
