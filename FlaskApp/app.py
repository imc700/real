from flask_sqlalchemy import SQLAlchemy
from flask import request, render_template, Flask, make_response
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import *
from wtforms.validators import DataRequired, Optional, Length

from flask_login import login_manager, UserMixin, login_required, login_user
from FlaskApp.wx_login_or_register import get_access_code, get_wx_user_info, login_or_register
from FlaskApp.model import db
from WeiXinCore.WeiXin import *
from WeiXinCore.WeiXinMsg import WeiXinMsg
from WeiXinCore.real import *

app = Flask(__name__)
ctx = app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ssss2222@116.63.138.138:3306/real?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 继承db.model 是为了方便操作数据库
# 注册数据库连接
db.app = app
db.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    pwd_hash = db.Column(db.String(300))

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd

    @staticmethod
    def query_by_username(username):
        return User.query.filter(User.username == username).first()

    @property
    def pwd(self):
        raise AttributeError(u'密码不可读')

    @pwd.setter
    def pwd(self, pwd):
        self.pwd_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.pwd_hash, pwd)

    def __repr__(self):
        return '<User:%s>' % self.username


db.create_all()


class LoginForm(FlaskForm):
    username = StringField('账户名：', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('密码：', validators=[DataRequired(), Length(1, 64)])
    remember_me = BooleanField('记住密码', validators=[Optional()])


login_manager_local = login_manager.LoginManager()
login_manager_local.init_app(app)
login_manager_local.session_protection = 'strong'
login_manager_local.login_view = 'login'


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(1)
    if request.method == 'GET':
        print(2)
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        print(3)
        form = LoginForm(request.form)
        if form.validate():
            username = request.form['name']
            pwd = request.form['pwd']
            user = User.query_by_username(username)

            if user and user.verify_password(pwd):
                login_user(user)
                return 'login ok'
        else:
            print(form.errors)
        return render_template('login.html', form=form)

@app.route("/testWXLoginOrRegister",methods=["GET"])
def test_wx_login_or_register():
    """
    测试微信登陆注册
    :return:
    """
    # 前端获取到的临时授权码
    code = request.args.get("code")
    # 标识web端还是app端登陆或注册
    flag = request.args.get("flag")

    # 参数错误
    if code is None or flag is None:
        return "参数错误"

    # 获取微信用户授权码
    access_code = get_access_code(code=code, flag=flag)
    if access_code is None:
        return "获取微信授权失败"

    # 获取微信用户信息
    wx_user_info = get_wx_user_info(access_data=access_code)
    if wx_user_info is None:
        return "获取微信授权失败"

    # 验证微信用户信息本平台是否有，
    data = login_or_register(wx_user_info=wx_user_info)
    if data is None:
        return "登陆失败"
    return data

@app.route('/')
@login_required
def index():
    return "Hello, World!"


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
        # return respXml
        response = make_response(respXml)
        response.content_type = 'application/xml'
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=39004)
