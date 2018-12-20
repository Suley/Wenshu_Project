# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  wenshu.py
@time:  2018/11/27
"""
import scrapy
import json
import math
import execjs
import logging
from Wenshu.items import WenshuJsonItem
from Wenshu.utils.case.case import WenshuCase
from Wenshu.utils.regionAndcourt.court import Court
from Wenshu.utils.regionAndcourt.region import Region
from Wenshu.utils.timeutils import TimeUtils


class WenshuSpider(scrapy.Spider):

    name = 'wenshu'
    start_urls = ['http://wenshu.court.gov.cn/list/list/?sorttype=1']

    LIST_URL = 'http://wenshu.court.gov.cn/List/ListContent'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # 获取开始时间，结束时间
        return cls(b_date=crawler.settings.get("BEGIN_DATE"), e_date=crawler.settings.get("END_DATE"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_date = TimeUtils.get_between_day(kwargs["b_date"], kwargs["e_date"])  # 获取日期的迭代器
        self.case = WenshuCase()  # 案由类
        self.region = Region()  # 地域类
        self.court = Court()  # 法院类

        with open('Wenshu/spiders/get_vl5x.js', encoding='utf-8') as f:
            jsdata_1 = f.read()
        self.js_1 = execjs.compile(jsdata_1)

        self.guid = '5969ecb9-eabf-2fac9283-6d278d8fda1b'
        self.vjkl5 = None
        self.vl5x = None

    def get_request_data(self, date, s_type, s_key=None, case_id='#', page='1'):
        """
        准备请求参数
        :param date: 裁判日期
        :param s_type: 搜索类型, 0: 没有地域条件, 1: 法院地域:x, 2: 中级法院:x, 3: 法院名称
        :param s_key: 地域key or 法院key,默认为空
        :param case_id:  案由id, 默认没有
        :param page:  页数str '1' - '10'
        :param direc: 排序方式
        :return: dict
        """
        param = ''
        if case_id == '#':
            param += '裁判日期:{0} TO {1}'.format(date, date)
        else:
            param += '案由:{0},裁判日期:{1} TO {2}'.format(self.case.mp[case_id].name, date, date)

        if s_type == 1:
            if s_key:
                param += ',法院地域:{}'.format(self.region.mp[s_key].name)
        elif s_type == 2:
            if s_key:
                param += ',中级法院:{}'.format(self.court.mp[s_key].name)
        elif s_type == 3:
            if s_key:
                param += ',法院名称:{}'.format(self.court.mp[s_key].name)

        return {
            # 筛选条件
            'Param': param,
            'Index': page,  # 页数
            'Page': '20',  # 获取案件数目
            'Order': '审判程序',  # 排序类型(1.法院层级/2.裁判日期/3.审判程序)
            'Direction': 'asc',  # 排序方式(1.asc:从小到大/2.desc:从大到小)
            'vl5x': self.vl5x,
            'number': 'wens',
            'guid': self.guid
        }

    def get_request_headers(self):
        return {
            'Cookie': 'vjkl5=' + self.vjkl5,  # 在这单独添加cookie,settings中就可以禁用cookie,防止跟踪被ban
            'Host': 'wenshu.court.gov.cn',
            'Origin': 'http://wenshu.court.gov.cn',
        }

    def parse(self, response):
        """获取cookie，设置筛选条件"""
        try:
            self.vjkl5 = response.headers['Set-Cookie'].decode('utf-8')
            self.vjkl5 = self.vjkl5.split(';')[0].split('=')[1]
            self.vl5x = self.js_1.call('getvl5x', self.vjkl5)
        except LookupError:
            print("parse() 获取cookie错误,重新获取")
            return self.error_req(response)
        # 迭代每一天
        for date in self.get_date:
            data = self.get_request_data(date=date, s_type=0)
            headers = self.get_request_headers()
            yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                     meta={'date': date, 's_type': 0, 's_key': '0', 'case_id': '#'},
                                     callback=self.get_content, dont_filter=True)

    def get_content(self, response):
        """获取检索出来的案件的 json数据"""
        html = response.text
        try:  # 可能为 "[]"
            result = eval(json.loads(html))
            count = result[0]['Count']
        except:
            return self.error_req(response)

        self.show_information(count, response)

        s_type = response.meta['s_type']
        int_count = int(count)
        if int_count <= 200:  # 小于200数据了，收割
            return self.get_pages(count, response)
        elif s_type < 3:  # 地域及法院还没搜到3，继续细分
            return self.region_and_court_formrequest(response)
        elif s_type == 3:  # 地域及法院搜到3,根据案由继续细分
            return self.case_formrequsts(count, response)

    def error_req(self, response):
        """
        错误报文
        :param response:
        :return: error_times 计数重发
        """
        if 'error_times' not in response.meta.keys():
            response.meta['error_times'] = 1
        else:
            response.meta['error_times'] = response.meta['error_times'] + 1
            if response.meta['error_times'] > 3:
                return None
        print("response异常次数:{}".format(response.meta['error_times']))
        return response.request.copy()

    def show_information(self, count=0, response=None):
        """
        终端显示数据用
        :param count:
        :param response:
        :return:
        """
        date = response.meta['date']
        s_type = response.meta['s_type']
        s_key = response.meta['s_key']
        case_name = self.case.mp[response.meta['case_id']].name

        if count != '0':
            if s_type == 0:
                s_name = '无'
            elif s_type == 1:
                s_name = '地域'
            elif s_type == 2:
                s_name = '中级人民法院'
            else:
                s_name = '法院名称'

            if s_key != '0':
                if s_type == 1:
                    sss = self.region.mp[s_key].name
                else:
                    sss = self.court.mp[s_key].name
                print('******日期:{}, {}: {}, 案由:{} 数据量:{}'.format(date, s_name, sss, case_name, count))
            else:
                print('******日期:{}, 案由:{}, 数据量:{}'.format(date, case_name, count))

    def region_and_court_formrequest(self, response):
        """
        根据meta的s_type和s_key制作request
        :param response:
        :return: Request
        """
        date = response.meta['date']
        s_type = response.meta['s_type']
        headers = self.get_request_headers()
        if s_type == 0:

            # 法院名称：最高人民法院
            data = self.get_request_data(date=date, s_type=3, s_key='001000')
            yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                     meta={'date': date, 's_type': 3, 's_key': '001000', 'case_id': '#'},
                                     callback=self.get_content, dont_filter=True)

            # 法院地域：所有地域
            for s_key in range(1, 32):
                data = self.get_request_data(date=date, s_type=1, s_key=s_key)
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 's_type': 1, 's_key': s_key, 'case_id': '#'},
                                         callback=self.get_content, dont_filter=True)
        elif s_type < 3:
            if s_type == 1:
                region_key = response.meta['s_key']
                court_key = self.region.mp[region_key].court_key
            else:  # s_type == 2:
                court_key = response.meta['s_key']

            # 法院名称：高级or中级人民法院
            data = self.get_request_data(date=date, s_type=3, s_key=court_key)
            yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                     meta={'date': date, 's_type': 3, 's_key': court_key, 'case_id': '#'},
                                     callback=self.get_content, dont_filter=True)

            # 中级法院：所有辖区人民法院
            son_list = self.court.get_son_keys(court_key)
            for son_court_key in son_list:
                data = self.get_request_data(date=date, s_type=s_type+1, s_key=son_court_key)
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 's_type': s_type+1, 's_key': son_court_key, 'case_id': '#'},
                                         callback=self.get_content, dont_filter=True)

    def case_formrequsts(self, count, response):
        """
        根据date和case_id制作一份Formrequest返回
        :param count: 数量
        :param response: item or request
        :return:
        """
        case_id = response.meta['case_id']
        date = response.meta['date']
        sonid_list = self.case.mp[case_id].son_list
        s_type = response.meta['s_type']
        s_key = response.meta['s_key']
        if len(sonid_list) == 0:
            # 没有子案由还超过200条, 得到200条数据，输出到日志INFO
            logging.info('日期: {0}, 案由: {1}, s_key: {2} 条件下数据量: {3}, 获取前200条'.format(date, case_id, s_key, count))
            for i in self.get_pages(200, response):
                yield i
        else:
            for cid in sonid_list:
                data = self.get_request_data(date=date, s_type=s_type, s_key=s_key, case_id=cid)
                headers = self.get_request_headers()
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 's_type': s_type, 's_key': s_key, 'case_id': cid},
                                         callback=self.get_content, dont_filter=True)

    def get_pages(self, count, response):
        """
        获取不超过200条数据
        :param count: 总数
        :param response: 响应
        :return: item
        """
        if count == '0':
            return

        # 第一页的数据不用请求，直接获取
        for i in self.get_json(response):
            yield i

        date = response.meta['date']
        s_type = response.meta['s_type']
        s_key = response.meta['s_key']
        case_id = response.meta['case_id']
        # 计算出请求多少页
        page = math.ceil(int(count) / 20)  # 向上取整,每页20条
        for i in range(2, int(page) + 1):
            if i <= 10:  # 最多200条，每页20条
                headers = self.get_request_headers()
                data = self.get_request_data(date=date, s_type=s_type, s_key=s_key, case_id=case_id, page=str(i))
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 's_type': s_type, 's_key': s_key, 'case_id': case_id},
                                         callback=self.get_json,  dont_filter=True)

    def get_json(self, response):
        """获取一个json数据"""
        text = response.text
        # 特判貌似不怎么好
        if text == '"[]"':
            return self.error_req(response)

        item = WenshuJsonItem()
        item['json_data'] = text
        item['date'] = response.meta['date']
        yield item
