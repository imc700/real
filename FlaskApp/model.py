from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 用户姓名
    name = db.Column(db.String(20), nullable=False)
    # 用户年龄
    age = db.Column(db.Integer, nullable=False)


class UserLoginMethod(db.Model):
    """
    用户登陆验证表
    """
    __tablename__ = 'user_login_method'
    # 用户登陆方式主键ID
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # 用户主键ID
    user_id = db.Column(db.Integer, nullable=False)
    # 用户登陆方式，WX微信，P手机
    login_method = db.Column(db.String(36), nullable=False)
    # 用户登陆标识，微信ID或手机号
    identification = db.Column(db.String(36), nullable=False)
    # 用户登陆通行码，密码或token
    access_code = db.Column(db.String(36), nullable=True)
