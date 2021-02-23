#coding:utf-8
import json
import urllib.request
import zlib
from urllib import *
from urllib.parse import quote_plus

from WeiXinCore.WeiXinMsg import *


def getJson(url):
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    opener = urllib.request.build_opener()
    response = opener.open(request)
    html = response.read()#.decode('gbk').encode('utf-8')
    gzipped = response.headers.get('Content-Encoding')
    if gzipped:
        html = zlib.decompress(html, 16+zlib.MAX_WBITS)
    return json.loads(html)




