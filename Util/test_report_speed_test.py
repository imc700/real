# -*- coding: utf-8 -*-
import platform
import unittest
import uuid

import datetime
import pymysql
import time
from urllib.parse import urlparse
import asyncio

import pytest
from pyppeteer import launch
import nest_asyncio

nest_asyncio.apply()


class UntitledTestCase(unittest.TestCase):
    # app = Flask(__name__)
    # ctx = app.app_context()
    # ctx.push()

    # 获取数据库连接
    def get_db(self):
        db = self.db
        if db is not None:
            try:
                db.ping(True)
                return db
            except Exception as e:
                print(e)
        try:
            db = pymysql.connect("10.8.6.202", "mic_test", "Mic@2017", "dmp_uitest_data",port=5590)
            return db
        except Exception as e:
            print(e)

    @classmethod
    def setUpClass(cls):
        platform_info = platform.uname()  # 获取执行及的系统和硬件信息
        cls.platform = ','.join(platform_info)  # 将数组转换成字符串,以逗号连接
        # 连接数据库
        try:
            cls.db = pymysql.connect("10.8.6.202", "mic_test", "Mic@2017", "dmp_uitest_data",port=5590)
        except Exception as e:
            print(e)
        else:
            print("hello_mysql")
            print("suc_login_sql")

        # 打开浏览器
        # cls.driver = DmpPage.headless_driver()      #无头
        # cls.driver = DmpPage.new_driver()

    def setUp(self):
        self.page_refresh_count = 6  # 页面的刷新次数
        # self.driver.implicitly_wait(30)
        self.accept_next_alert = True
        self.results = []

        self.dom = """          () =>{
                            let mytiming = window.performance.timing;
                            return mytiming.domComplete - mytiming.domInteractive ;}
                """
        self.ari = """          // 页面完全加载完成所耗时间----最重要!!!
                            let mytiming = window.performance.timing;
                            return mytiming.responseStart - mytiming.navigationStart ;
                """

        self.domready = """         () =>{ 
                            let mytiming = window.performance.timing;
                            return mytiming.domContentLoadedEventEnd   - mytiming.fetchStart ;}
                """
        self.loadEventTime = """      // 页面加载时间
                           let mytiming = window.performance.timing;
                           return mytiming.loadEventEnd - mytiming.connectStart ;
                              """
        self.loadEventTime2 = """      // 页面加载时间
                           let mytiming = window.performance.timing;
                           return mytiming.loadEventEnd;
                              """
        self.loadEventTime3 = """      // 页面加载时间
                           let mytiming = window.performance.timing;
                           return mytiming.connectStart ;
                              """

        # 2020年9月16日19:39:23加载时间网址，多个的话,在此处数组中继续添加即可,有多少个网页就放多少个
        self.gather_data_dict_ = [

        ]

        self.cookie_list = [{'domain': '.dmp-test.mypaas.com.cn', 'expiry': 1932717828, 'httpOnly': False, 'name': 'user_org', 'path': '/', 'secure': False, 'value': '""'}, {'domain': '.dmp-test.mypaas.com.cn', 'expiry': 1932717828, 'httpOnly': False, 'name': 'user_name', 'path': '/', 'secure': False, 'value': '%22JL01%22'}, {'domain': '.dmp-test.mypaas.com.cn', 'expiry': 10572689028, 'httpOnly': False, 'name': 'account', 'path': '/', 'secure': False, 'value': 'junlin'}, {'domain': '.dmp-test.mypaas.com.cn', 'expiry': 10572689028, 'httpOnly': False, 'name': 'tenant_code', 'path': '/', 'secure': False, 'value': 'test'}, {'domain': '.dmp-test.mypaas.com.cn', 'expiry': 10572689028, 'httpOnly': False, 'name': 'token', 'path': '/', 'secure': False, 'value': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjM5ZWQ3YWM5LTlhMTUtMGU5Ny1mNWNlLWUzNjFlNzU5YWM2YiIsIl9mbGFnIjoxNjE3MzI5MjMzLCJhY2NvdW50IjoianVubGluIiwiY29kZSI6InRlc3QiLCJncm91cF9pZHMiOm51bGwsImN1c3RvbWl6ZV9yb2xlcyI6W10sImV4dGVybmFsX3VzZXJfaWQiOm51bGx9.n5sKBYl7hiPlYBU98arQF2-ZIbCnQj9JeEQniQ_26mE'}, {'domain': 'dmp-test.mypaas.com.cn', 'expiry': 1617330821, 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'secure': False, 'value': '2f624a5016173290210357770e2922b35a24e816aa1ab88517c56e87914f66'}, {'domain': '.dmp-test.mypaas.com.cn', 'httpOnly': False, 'name': 'dmp_env_code', 'path': '/', 'secure': False, 'value': 'hangzhoub_test_1'}, {'domain': '.mypaas.com.cn', 'httpOnly': False, 'name': '__fast_sid__', 'path': '/', 'secure': False, 'value': '23e9737b96c50c0-938c003b17-6f343654'}, {'domain': '.mypaas.com.cn', 'expiry': 2481329028, 'httpOnly': False, 'name': '__tracker_user_id__', 'path': '/', 'secure': False, 'value': '23e9737b9700200-cf6000c9fc-d7663336'}]

    def cal_core(self, page, res_page):
        """
        计算最大最小和平均值
        :param page:
        :param res_page:
        :return:
        """
        if len(page) > 0:
            page.sort()
            page = page[2:-1]
            res_page['max'] = max(page)
            res_page['min'] = min(page)
            res_page['avg'] = sum(page) // len(page)
        return res_page

    def test_untitled_test_case(self):
        """
        用例
        :return:
        """
        asyncio.get_event_loop().run_until_complete(self._testSpeed())
        print("准备将数据记录于数据库...")
        for re in self.results:  # 把结果存入数据库
            try:
                id_ = str(uuid.uuid4())  # 生成uuid
                try:
                    dashboard_id = re['url'].split('?')[0].split('/')[-1]  # 取出url中的报告id
                except Exception as e2:
                    dashboard_id = '-1'  # 若异常,则默认报告id为-1

                if 'share' in re['url']:  # 下述三个判断得出报告类型
                    page_type = 'share'
                if 'edit' in re['url']:
                    page_type = 'edit'
                if 'preview' in re['url']:
                    page_type = 'preview'
                if 'dataview-mobile' in re['url']:
                    page_type = 'mobile'

                db = self.get_db()  # 拿到数据库db
                cursor = db.cursor()
                # 插入主表
                trans_one_sql = "INSERT INTO test_page_speed (id,url,dashboard_id,dashboard_name,cache_count,no_cache_count,client_info,page_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                # 插入无缓存表
                trans_no_cache_sql = "INSERT INTO no_cache_time (id,max_time_dom,min_time_dom,avg_time_dom," \
                                     "max_time_complete,min_time_complete,avg_time_complete," \
                                     "max_time_domready,min_time_domready,avg_time_domready," \
                                     "max_time_page,min_time_page,avg_time_page) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                # 插入有缓存表
                trans_cache_sql = "INSERT INTO cache_time (id,max_time_dom,min_time_dom,avg_time_dom," \
                                  "max_time_complete,min_time_complete,avg_time_complete," \
                                  "max_time_domready,min_time_domready,avg_time_domready," \
                                  "max_time_page,min_time_page,avg_time_page) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                # 上述三个sql语句的参数在下述三个元组中
                params1 = (
                id_, re['url'], dashboard_id, re['NoCache']['title'], re['number'], re['number'], self.platform,
                page_type)
                params2 = (id_
                           , re['NoCache']['dom']['max'], re['NoCache']['dom']['min'], re['NoCache']['dom']['avg']
                           , re['NoCache']['ari']['max'], re['NoCache']['ari']['min'], re['NoCache']['ari']['avg']
                           , re['NoCache']['domready']['max'], re['NoCache']['domready']['min'],
                           re['NoCache']['domready']['avg']
                           , re['NoCache']['page']['max'], re['NoCache']['page']['min'], re['NoCache']['page']['avg']
                           )
                params3 = (id_
                           , re['Cache']['dom']['max'], re['Cache']['dom']['min'], re['Cache']['dom']['avg']
                           , re['Cache']['ari']['max'], re['Cache']['ari']['min'], re['Cache']['ari']['avg']
                           , re['Cache']['domready']['max'], re['Cache']['domready']['min'],
                           re['Cache']['domready']['avg']
                           , re['Cache']['page']['max'], re['Cache']['page']['min'], re['Cache']['page']['avg']
                           )
                # 三个sql语句和参数都有了,则分别执行三个sql,返回是影响行数
                effect_row1 = cursor.execute(trans_one_sql, params1)
                effect_row2 = cursor.execute(trans_no_cache_sql, params2)
                effect_row3 = cursor.execute(trans_cache_sql, params3)
                db.commit()  # 提交
                cursor.close()
                # db.close()
                print('插入成功!主记录表,cache表,noche表分别插入条数为:', effect_row1, effect_row2, effect_row3)
                # return str(effect_row1)
            except Exception as e:
                print('发生了异常:')
                print(e)

    async def _testSpeed(self):
        result = []  # 返回结果
        # 读取压测数数据，返回加载结果！__get_page_load_time_Cache
        for data in self.gather_data_dict_:  # 将多个网址循环
            result_temp = {
                "dashboard_id": data["url"],
                "url": data["url"],
                "number": self.page_refresh_count,
                "Cache": asyncio.get_event_loop().run_until_complete(
                    self.__get_page_load_time_Cache(data['url'], self.page_refresh_count)),  # 进行有缓存取加载时间
                "NoCache": asyncio.get_event_loop().run_until_complete(
                    self.__get_page_load_time_NoCache(data['url'], self.page_refresh_count))  # 进行无缓存取加载时间
            }
            result.append(result_temp)  # 将有无缓存的结果放入result
        print(result)
        self.results = result
        # return result

    def cal_load_time(self, title_,
                      res_dom, dom,
                      res_ari, ari,
                      res_page, page,
                      res_domready, domready
                      ):
        """
        计算加载时间
        :param res_page:
        :param page:
        :param res_domready:
        :param domready:
        :return:
        """
        for _i in range(self.page_refresh_count):
            page.append(1000)
            # dom.append(1000)
            # domready.append(1000)

        res_dom = self.cal_core(dom, res_dom)
        res_ari = self.cal_core(ari, res_ari)
        res_domready = self.cal_core(domready, res_domready)
        res_page = self.cal_core(page, res_page)
        return {
            "dom": res_dom
            , "ari": res_ari
            , "domready": res_domready
            , "page": res_page
            , "title": title_
        }

    def gen_cookie(self):
        return {
            'domain': f'.{urlparse(self.url).netloc}',
            'name': 'token',
            'value': self.token,
            'expiry': 7200 + 3600 * 24 * 100000,
            'path': '/',
            'httpOnly': True,
            'secure': False
        }

    async def __get_page_load_time_NoCache(self, url, number=20):
        """
        网页无缓存的情况下进行加载速度测试
        :param url: 加载的网址
        :param number: 加载次数
        :return:
        """
        print("正在处理" + url + "网页无缓存的情况...")
        self.url = url
        dom = []  # 执行最上面dom的js所得的结果列表(数值类型的集合)
        ari = []  # -----------------执行kappa所想出来的求页面加载时间的方法(在driver请求前后利用隐式等待)所得的结果列表-------------------
        pages = []  # 执行最上面page的js所得的结果列表
        domready = []  # 执行最上面domready的js所得的结果列表

        res_dom = {}  # 下述四个字典分别将上述对应的集合转成json格式,因为有最大最小和平均时间.
        res_ari = {}
        res_domready = {}
        res_page = {}

        # 进行测试前先用带ck的方式登录下该网址
        path = '/Users/Library/Application Support/pyppeteer/local-chromium/588429/chrome-mac/'
        browser = None
        browser = await launch(headless=True, userDataDir=r'D:\temporary', args=['--disable-infobars', '--no-sandbox'])
        title_ = ''
        for i in range(number + 1 -2 ):  # number是该网址要测试的次数,循环一下
            # 调用浏览器打开一个新窗口(因为要无缓存)
            page = await browser.newPage()
            # 设置cookie
            for ck in self.cookie_list:
                await page.setCookie(ck)
            q = datetime.datetime.now().timestamp()
            await page.goto(self.url, {'timeout': 60 * 1000, 'waitUntil': ['networkidle0']})
            load_total_time = str(datetime.datetime.now().timestamp() - q)[0:5]  # 页面链接数为0(500ms内再无链接进入)
            load = await page.evaluate(self.dom)
            domcontentloaded = await page.evaluate(self.domready)
            title_ = await page.title()  # 取页面的标题
            # 关闭窗口
            await page.close()
            if i > 0:
                load_total_time = float(load_total_time) - 0.5
                print('无缓存此次加载页面完成时间为:' + str(round(load_total_time, 2))+' ,load时间为:' + str(round(float(load), 2))+' ,dom树加载完成时间为:'+ str(round(float(domcontentloaded), 2)))
                dom.append(int(float(load) ))
                domready.append(int(float(domcontentloaded) ))
                ari.append(int(float(load_total_time) * 1000))
                time.sleep(1)
        await browser.close()

        # 开始组装结果
        return self.cal_load_time(title_,
                                  res_dom, dom,
                                  res_ari, ari,
                                  res_page, pages,
                                  res_domready, domready
                                  )

    async def __get_page_load_time_Cache(self, url, number=20):
        """
        网页有缓存的情况下进行加载速度测试
        :param url: 加载的网址
        :param number: 加载次数
        :return:
        """
        print("正在处理" + url + "网页有缓存的情况...")
        self.url = url
        dom = []  # 执行最上面dom的js所得的结果列表(数值类型的集合)
        ari = []  # -----------------执行kappa所想出来的求页面加载时间的方法(在driver请求前后利用隐式等待)所得的结果列表-------------------
        pages = []  # 执行最上面page的js所得的结果列表
        domready = []  # 执行最上面domready的js所得的结果列表

        res_dom = {}  # 下述四个字典分别将上述对应的集合转成json格式,因为有最大最小和平均时间.
        res_ari = {}
        res_domready = {}
        res_page = {}

        # 进行测试前先用带ck的方式登录下该网址executablePath=path,
        path = '/Users/Library/Application Support/pyppeteer/local-chromium/588429/chrome-mac/'
        browser = None
        browser = await launch(headless=True, userDataDir=r'D:\temporary', args=['--disable-infobars', '--no-sandbox'])
        title_ = ''
        page = await browser.newPage()
        # 设置cookie
        for ck in self.cookie_list:
            await page.setCookie(ck)
        for i in range(number + 1):  # number是该网址要测试的次数,循环一下



            q = datetime.datetime.now().timestamp()
            await page.goto(self.url, {'timeout': 60 * 1000, 'waitUntil': ['networkidle0']})
            load_total_time = str(datetime.datetime.now().timestamp() - q)[0:5]  # 加载完页面再取一次当前时间用于计算

            load = await page.evaluate(self.dom)
            domcontentloaded = await page.evaluate(self.domready)

            title_ = await page.title()  # 取页面的标题
            if i > 0:
                load_total_time = float(load_total_time) - 0.5
                print('有缓存此次加载页面完成时间为:' + str(round(load_total_time, 2)) + ' ,load时间为:' + str(
                    round(float(load), 2)) + ' ,dom树加载完成时间为:' + str(round(float(domcontentloaded), 2)))
                dom.append(int(float(load) ))
                domready.append(int(float(domcontentloaded) ))
                ari.append(int(float(load_total_time) * 1000))
                time.sleep(1)
        await browser.close()
        # 开始组装结果
        return self.cal_load_time(title_,
                                  res_dom, dom,
                                  res_ari, ari,
                                  res_page, pages,
                                  res_domready, domready
                                  )

    def tearDown(self):
        pass





"""
# 无头
网页无缓存的情况:
20次刷新页面后,domready,页面加载7项的时间分别为
[301, 321, 203, 326, 245, 201, 208, 199, 218, 344, 324, 215, 244, 221, 204, 231, 206, 333, 211, 222]
[639, 393, 274, 431, 327, 273, 307, 361, 342, 414, 425, 355, 398, 306, 313, 319, 325, 435, 357, 388]
网页有缓存的情况:
20次刷新页面后,domready,页面加载7项的时间分别为
[281, 1135, 1115, 1120, 1110, 1121, 1112, 1109, 1116, 1120, 1110, 1104, 1111, 1106, 1112, 1112, 1093, 1117, 1104, 1112]
[417, 1309, 1232, 1198, 1255, 1272, 1246, 1263, 1220, 1266, 1229, 1179, 1210, 1180, 1187, 1187, 1231, 1242, 1246, 1187]
[{'dashboard_id': 'https://dmp-test.mypaas.com.cn/dataview/share/39f78829-4047-55fe-9f9e-ecd71367e8e3?code=uitest', 'url': 'https://dmp-test.mypaas.com.cn/dataview/share/39f78829-4047-55fe-9f9e-ecd71367e8e3?code=uitest', 'number': 20, 'NoCache': {'domready': {'max': 301, 'min': 208, 'avg': 231.6}, 'page': {'max': 398, 'min': 319, 'avg': 356.5}}, 'Cache': {'domready': {'max': 1116, 'min': 1109, 'avg': 1111.9}, 'page': {'max': 1246, 'min': 1187, 'avg': 1224.1}}}]
'max'


'INSERT INTO test_page_speed (url,cache_count,cache_max_time,cache_min_time,cache_avg_time,no_cache_count,no_cache_max_time,no_cache_min_time,no_cache_avg_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

# 开了有头

网页无缓存的情况:
20次刷新页面后,domready,页面加载7项的时间分别为
[357, 229, 215, 220, 216, 231, 217, 219, 216, 260, 219, 337, 216, 255, 238, 216, 218, 213, 217, 234]
[737, 314, 291, 302, 292, 309, 296, 296, 295, 335, 297, 420, 293, 331, 318, 291, 302, 294, 298, 311]
网页有缓存的情况:
20次刷新页面后,domready,页面加载7项的时间分别为
[384, 998, 972, 980, 976, 967, 971, 974, 983, 973, 968, 984, 976, 970, 982, 983, 979, 978, 981, 989]
[426, 1073, 1047, 1053, 1052, 1041, 1045, 1048, 1057, 1046, 1043, 1055, 1050, 1042, 1056, 1059, 1058, 1053, 1053, 1064]
[{'dashboard_id': 'https://dmp-test.mypaas.com.cn/dataview/share/39f78829-4047-55fe-9f9e-ecd71367e8e3?code=uitest', 'url': 'https://dmp-test.mypaas.com.cn/dataview/share/39f78829-4047-55fe-9f9e-ecd71367e8e3?code=uitest', 'number': 20, 'NoCache': {'domready': {'max': 234, 'min': 216, 'avg': 222.0}, 'page': {'max': 314, 'min': 295, 'avg': 302.0}}, 'Cache': {'domready': {'max': 982, 'min': 972, 'avg': 977.1}, 'page': {'max': 1056, 'min': 1046, 'avg': 1051.3}}}]

https://tlanyan.me/trojan-pac.php?p=1081
"""
if __name__ == '__main__':
    pytest.main(['-s',"test_report_speed_test.py","--reruns=1","--reruns-delay=2"])