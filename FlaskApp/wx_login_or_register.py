import json
from urllib import parse, request


def get_access_code(code, flag):
    """
    获取微信授权码
    :param code:前端或app拉取的到临时授权码
    :param flag:web端或app端
    :return:None 或 微信授权数据
    """
    # 判断是web端登陆还是app端登陆，采用不同的密钥。
    if flag == "web":
        appid = "web_appid"
        secret = "web_secret"
    elif flag == "app":
        appid = "app_appid"
        secret = "app_secret"
    else:
        return None
    try:
        # 把查询条件转成url中形式
        fields = parse.urlencode(
            {"appid": appid, "secret": secret,
            "code": code, "grant_type": "authorization_code"}
        )
        # 拼接请求链接
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?{}'.format(fields)
        print(url)
        req = request.Request(url=url, method="GET")
        # 请求数据
        res = request.urlopen(req, timeout=10)
        # 解析数据
        access_data = json.loads(res.read().decode())
        print(access_data)
    except Exception as e:
        print(e)
        return None

    # 拉取微信授权成功返回
    # {
    # "access_token": "ACCESS_TOKEN", "expires_in": 7200,"refresh_token": "REFRESH_TOKEN",
    # "openid": "OPENID","scope": "SCOPE"
    # }

    if "openid" in access_data:
        return access_data

    # 拉取微信授权失败
    # {
    # "errcode":40029,"errmsg":"invalid code"
    # }
    else:
        return None


def get_wx_user_info(access_data: dict):
    """
    获取微信用户信息
    :return:
    """
    openid = access_data.get("openid")
    access_token = access_data.get("access_token")
    try:
        # 把查询条件转成url中形式
        fields = parse.urlencode({"access_token": access_token, "openid": openid})
        # 拼接请求链接
        url = 'https://api.weixin.qq.com/sns/userinfo?{}'.format(fields)
        print(url)
        req = request.Request(url=url, method="GET")
        # 请求数据,超时10s
        res = request.urlopen(req, timeout=10)
        # 解析数据
        wx_user_info = json.loads(res.read().decode())
        print(wx_user_info)
    except Exception as e:
        print(e)
        return None

    # 获取成功
    # {
    # "openid":"OPENID",
    # "nickname":"NICKNAME",
    # "sex":1,
    # "province":"PROVINCE",
    # "city":"CITY",
    # "country":"COUNTRY",
    # "headimgurl": "test.png",
    # "privilege":[
    # "PRIVILEGE1",
    # "PRIVILEGE2"
    # ],
    # "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
    #
    # }
    if "openid" in wx_user_info:
        return wx_user_info
    #  获取失败
    # {"errcode":40003,"errmsg":"invalid openid"}
    else:
        return None




