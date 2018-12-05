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
from Wenshu.utils.case.maptree import WenshuCase
from Wenshu.utils.regionAndcourt.court import Court
from Wenshu.utils.regionAndcourt.region import Region
from Wenshu.utils.timeutils import get_between_day


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
        self.get_date = get_between_day(kwargs["begin_date"], kwargs["end_date"])  # 获取日期的迭代器
        self.cls_case = WenshuCase()  # 案由类
        self.region = Region()  # 地域类
        self.court = Court()  # 法院类

        with open('Wenshu/spiders/get_vl5x.js', encoding='utf-8') as f:
            jsdata_1 = f.read()
        with open('Wenshu/spiders/docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_1 = execjs.compile(jsdata_1)
        self.js_2 = execjs.compile(jsdata_2)
        self.guid = '5969ecb9-eabf-2fac9283-6d278d8fda1b'
        self.vjkl5 = None
        self.vl5x = None

    def get_request_data(self, date, s_type=0, s_key=None, case_id='#', page='1'):
        """
        准备请求参数
        :param date: 裁判日期
        :param s_type: 搜索类型, 0: 没有地域条件, 1: 法院地域:x, 2: 中级法院:x, 3: 法院名称
        :param s_key: 地域key or 法院key,默认为空
        :param case_id:  案由id, 默认没有
        :param page:  页数str '1' - '10'
        :return: dict
        """
        param = ''
        if case_id == '#':
            param += '裁判日期:{0} TO {1}'.format(date, date)
        else:
            param += '案由:{0},裁判日期:{1} TO {2}'.format(self.cls_case.case[case_id].name, date, date)

        if s_type == 1:
            if s_key:
                param += ',法院地域:{}'.format(self.region.mp[s_key].name)
            else:
                print('你怕是个傻逼,region_key都不传')
        elif s_type == 2:
            if s_key:
                param += ',中级法院:{}'.format(self.court.mp[s_key].name)
            else:
                print('你有毛病吧,court_key都不传')
        elif s_type == 3:
            if s_key:
                param += ',法院名称:{}'.format(self.court.mp[s_key].name)
            else:
                print('你有毛病吧,court_key都不传')

        return {
            # 筛选条件
            'Param': param,
            'Index': page,  # 页数
            'Page': '20',  # 获取案件数目
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
            data = self.get_request_data(date, case_id='#')
            headers = self.get_request_headers()
            yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                     meta={'date': date, 's_type': 0},
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

        self.show_information(count, response)

        s_type = response.meta['s_type']
        int_count = int(count)
        if int_count <= 200:  # 小于200数据了，收割
            return self.get_pages(count, response)
        if s_type < 3:  # 还没搜到3，继续搜
            return self.region_and_court_formrequest(response)
        elif s_type == 3:  # 搜到3了
            return self.get_pages(count, response)
        #    return self.case_formrequsts(date, case_id, count, response)

    def show_information(self, count, response):
        date = response.meta['date']
        s_type = response.meta['s_type']

        if count != '0':
            s_name = ''
            if s_type == 0:
                s_name = '无'
            elif s_type == 1:
                s_name = '地域'
            elif s_type == 2:
                s_name = '中级人民法院'
            elif s_type == 3:
                s_name = '法院名称'

            if 's_key' in response.meta.keys():
                s_key = response.meta['s_key']
                if s_type == 1:
                    sss = self.region.mp[s_key].name
                else:
                    sss = self.court.mp[s_key].name
                print('******日期:{}, {}: {}, 数据量:{}'.format(date, s_name, sss, count))
            else:
                print('******日期:{}, 数据量:{}'.format(date, count))

    # def case_formrequsts(self, date, case_id, count, response):
    #     """
    #     根据date和case_id制作一份Formrequest返回
    #     :param date: 日期
    #     :param case_id: 案由id
    #     :param count: 数量
    #     :param response: item or request
    #     :return:
    #     """
    #     sonid_list = self.cls_case.case[case_id].son_list
    #     if len(sonid_list) == 0:
    #         # 没有子案由还超过200条, 得到200条数据，输出到日志INFO
    #         logging.info('日期: {0}, 案由: {1} 条件下数据量: {2}, 获取前200条'.format(date, case_id, count))
    #         for i in self.get_pages(date=date, case_id=case_id, count=200, response=response):
    #             yield i
    #     else:
    #         for cid in sonid_list:
    #             data = self.get_request_data(date=date, case_id=cid)
    #             headers = self.get_request_headers()
    #             yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
    #                                      meta={'date': date, 'case_id': cid},
    #                                      callback=self.get_content, dont_filter=True)

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
            data = self.get_request_data(date, 3, '001000')
            yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                     meta={'date': date, 's_type': 3, 's_key': '001000'},
                                     callback=self.get_content, dont_filter=True)

            # 法院地域：所有地域
            for s_key in range(1, 32):
                data = self.get_request_data(date, 1, s_key)
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 's_type': 1, 's_key': s_key},
                                         callback=self.get_content, dont_filter=True)
        elif s_type < 3:
            if s_type == 1:
                region_key = response.meta['s_key']
                court_key = self.region.mp[region_key].court_key
            else:  # s_type == 2:
                court_key = response.meta['s_key']

            # 法院名称：高级or中级人民法院
            data = self.get_request_data(date, 3, court_key)
            yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                     meta={'date': date, 's_type': 3, 's_key': court_key},
                                     callback=self.get_content, dont_filter=True)

            # 中级法院：所有辖区人民法院
            son_list = self.court.get_son_keys(court_key)
            for son_court_key in son_list:
                data = self.get_request_data(date, s_type+1, son_court_key)
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 's_type': s_type+1, 's_key': son_court_key},
                                         callback=self.get_content, dont_filter=True)

    def get_pages(self, count, response):
        """
        获取不超过200条数据
        :param date: 日期
        :param case_id: 案由id
        :param count: 总数
        :param response: 响应
        :return: item
        """
        if count == '0':
            return

        # 第一页的数据不用请求，直接获取
        for i in self.get_docid(response):
            yield i

        date = response.meta['date']
        s_type = response.meta['s_type']
        s_key = response.meta['s_key']
        headers = self.get_request_headers()
        # 计算出请求多少页
        page = math.ceil(int(count) / 20)  # 向上取整,每页10条
        for i in range(2, int(page) + 1):
            if i <= 10:  # 最多200条，每页20条
                data = self.get_request_data(date=date, s_type=s_type, s_key=s_key, page=str(i))  # 每次20条
                yield scrapy.FormRequest(url=self.LIST_URL, headers=headers, formdata=data,
                                         meta={'date': date, 's_type': s_type, 's_key': s_key},
                                         callback=self.get_docid,  dont_filter=True)

    def get_docid(self, response):
        """获取一个json数据，到这里就成功啦！"""
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
