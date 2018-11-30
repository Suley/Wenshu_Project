# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  wenshu.py
@time:  2018/11/27
"""
import datetime
import scrapy
import json
import re
import math
import execjs
import logging
from Wenshu.items import WenshuJsonItem
from Wenshu.utils import timeutils
from Wenshu.utils.maptree import WenshuCase


class WenshuSpider(scrapy.Spider):

    name = 'wenshu'
    start_urls = ['http://wenshu.court.gov.cn/list/list/?sorttype=1']

    LIST_URL = 'http://wenshu.court.gov.cn/List/ListContent'

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # 获取开始时间，结束时间
        return cls(begin_date=crawler.settings.get("BEGIN_DATE"), end_date=crawler.settings.get("END_DATE"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取日期的迭代器
        self.get_date = timeutils.get_between_day(kwargs["begin_date"], kwargs["end_date"])
        self.cls_case = WenshuCase()
        self.guid = '5969ecb9-eabf-2fac9283-6d278d8fda1b'
        with open('Wenshu/spiders/get_vl5x.js', encoding='utf-8') as f:
            jsdata_1 = f.read()
        with open('Wenshu/spiders/docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_1 = execjs.compile(jsdata_1)
        self.js_2 = execjs.compile(jsdata_2)
        self.vjkl5 = None
        self.vl5x = None

    def get_request_data(self, date, case_id='#', page='1'):
        """
        :param date: 日期字符串，必要
        :param case_name: 案由名字符串，不必要
        :param page: str，页数字符串，不必要
        :return: data字典
        """
        if case_id == '#':
            param = '裁判日期:{0}  TO {1}'.format(date, date)
        else:
            param = '案由:{0},裁判日期:{1}  TO {2}'.format(self.cls_case.case[case_id].name, date, date)
        return {
            # 筛选条件
            'Param': param,
            'Index': page,  # 页数
            'Page': '10',  # 获取案件数目
            'Order': '裁判日期',  # 排序类型(1.法院层级/2.裁判日期/3.审判程序)
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
        except:
            print("parse() 获取cookie错误")
            return response.request.copy()
        # 迭代每一天
        for date in self.get_date:
            # 修改案由需要改两处地方，测试用
            data = self.get_request_data(date, case_id='#')
            headers = self.get_request_headers()
            yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                     meta={'date': date, 'case_id': '#'},
                                     callback=self.get_content, dont_filter=True)

    def get_content(self, response):
        """获取检索出来的案件的 json数据"""
        html = response.text
        try:
            result = eval(json.loads(html))
            count = result[0]['Count']
        except:
            print("get_content() json解析错误或者json数据错误")
            return response.request.copy()

        date = response.meta['date']
        case_id = response.meta['case_id']
        case_name = self.cls_case.case[case_id].name
        if count != '0':
            print('*******日期:{}, 案由:{}, 数据量:{}'.format(date, case_name, count))

        # 如果数据量超过200，迭代案由
        int_count = int(count)
        if int_count > 200:
            return self.get_case_formrequst(date, case_id, count, response)
        elif int_count > 0:
                return self.get_pages(date, case_id, count, response)

    def get_case_formrequst(self, date, case_id, count, response):
        """
        根据date和case_id制作一份Formrequest返回
        :param date: 日期
        :param case_id: 案由id
        :param count: 数量
        :param response: item or request
        :return:
        """
        sonid_list = self.cls_case.case[case_id].son_list
        if len(sonid_list) == 0:
            # 没有子案由还超过200条, 得到200条数据，输出到日志INFO
            logging.info('日期: {0}, 案由: {1} 条件下数据量: {2}, 获取前200条'.format(date, case_id, count))
            for i in self.get_pages(date=date, case_id=case_id, count=200, response=response):
                yield i
        else:
            for cid in sonid_list:
                data = self.get_request_data(date=date, case_id=cid)
                headers = self.get_request_headers()
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 'case_id': cid},
                                         callback=self.get_content, dont_filter=True)

    def get_pages(self, date, case_id, count, response):
        """
        获取不超过200条数据
        :param date: 日期
        :param case_id: 案由id
        :param count: 总数
        :param response: 响应
        :return: item
        """
        # 计算出请求多少页
        page = math.ceil(int(count) / 10)  # 向上取整,每页10条
        # 第一页的数据不用请求，直接获取
        for i in self.get_docid(response):
            yield i

        for i in range(2, int(page) + 1):
            if i <= 20:  # max:10*20=200 ; 20181005 -只能爬取20页,每页10条!!!!!!
                data = self.get_request_data(date=date, case_id=case_id, page=str(i))
                headers = self.get_request_headers()
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 'case_id': case_id},
                                         callback=self.get_docid,  dont_filter=True)

    def get_docid(self, response):
        """获取一个json数据的DocId，到这里就成功啦！"""
        item = WenshuJsonItem()
        text = response.text
        """ 有时候会出错 dict['文书ID'] 编程 dict['xxxID'] """
        item['json_data'] = text
        item['date'] = response.meta['date']
        yield item



    # def get_docid(self, response):
    #     """获取一个json数据的DocId，到这里就成功啦！"""
    #     html = response.text
    #     try:
    #         result = eval(json.loads(html))
    #         runeval = result[0]['RunEval']
    #         content = result[1:]
    #     except:
    #         print("get_docid() json解析错误或者json数据错误")
    #         yield response.request.copy()
    #
    #     for i in content:
    #         casewenshuid = i.get('文书ID', '')
    #         docid = self.decrypt_id(runeval, casewenshuid)
    #         item = WenshuDocidItem()
    #         item['docid'] = docid
    #         item['judgedate'] = response.meta['date']
    #         yield item
    #     # 输出时间
    #     #now_time = datetime.datetime.now().strftime('%H:%M:%S')
    #     #print('***时间: {}'.format(now_time))
    #
    # def decrypt_id(self, RunEval, id):
    #     """docid解密"""
    #     js = self.js_2.call("GetJs", RunEval)
    #     js_objs = js.split(";;")
    #     js1 = js_objs[0] + ';'
    #     js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
    #     key = self.js_2.call("EvalKey", js1, js2)
    #     key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]
    #     docid = self.js_2.call("DecryptDocID", key, id)
    #     return docid
