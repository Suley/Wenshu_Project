# -*- coding: utf-8 -*-
import datetime

import scrapy, json, re, math, execjs
from Wenshu.items import WenshuDocidItem
from Wenshu.utils import timeutils


class WenshuSpider(scrapy.Spider):
    name = 'wenshu'

    start_urls = ['http://wenshu.court.gov.cn/list/list/?sorttype=1']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(begin_date=crawler.settings.get("BEGIN_DATE"), end_date=crawler.settings.get("END_DATE"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取日期的迭代器
        self.get_date = timeutils.get_between_day(kwargs["begin_date"], kwargs["end_date"])
        self.guid = '5969ecb9-eabf-2fac9283-6d278d8fda1b'
        with open(r'Wenshu/spiders/get_vl5x.js', encoding='utf-8') as f:
            jsdata_1 = f.read()
        with open(r'Wenshu/spiders/docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_1 = execjs.compile(jsdata_1)
        self.js_2 = execjs.compile(jsdata_2)
        self.vjkl5 = None
        self.vl5x = None

    def parse(self, response):
        """获取cookie，设置筛选条件"""
        try:
            self.vjkl5 = response.headers['Set-Cookie'].decode('utf-8')
            self.vjkl5 = self.vjkl5.split(';')[0].split('=')[1]
            self.vl5x = self.js_1.call('getvl5x', self.vjkl5)
            # 先算出vl5x再提交一个form请求获取页面的json数据
            url = 'http://wenshu.court.gov.cn/List/ListContent'
            # 迭代每一天
            for date in self.get_date:
                data = {
                    # 筛选条件
                    'Param': '裁判日期:{}  TO {}'.format(date, date),
                    'Index': '1',  # 页数
                    'Page': '10',  # 只为了获取案件数目,所有请求0条就行了
                    'Order': '裁判日期',  # 排序类型(1.法院层级/2.裁判日期/3.审判程序)
                    'Direction': 'asc',  # 排序方式(1.asc:从小到大/2.desc:从大到小)
                    'vl5x': self.vl5x,
                    'number': 'wens',
                    'guid': self.guid
                }
                headers = {
                    # 在这单独添加cookie,settings中就可以禁用cookie,防止跟踪被ban
                    'Cookie': 'vjkl5=' + self.vjkl5,
                    'Host': 'wenshu.court.gov.cn',
                    'Origin': 'http://wenshu.court.gov.cn',
                }
                yield scrapy.FormRequest(url, formdata=data,
                                         meta={'date': date},
                                         callback=self.get_content, headers=headers, dont_filter=True)
        except Exception:
            yield scrapy.Request(WenshuSpider.start_urls, callback=self.parse, dont_filter=True)

    def get_content(self, response):
        """获取检索出来的案件的 json数据"""
        # 获取到json数据
        html = response.text
        result = eval(json.loads(html))
        count = result[0]['Count']

        print('*******{}:该日期下数据数据量:{}'.format(response.meta['date'], count))

        # 如果数据量超过200，加其它筛选条件(待写...)
        return self.get_pages(count, response)

    def get_pages(self, count, response):
        """获取不超过200条数据"""
        # 计算出请求多少页
        page = math.ceil(int(count) / 10)  # 向上取整,每页10条
        for i in range(1, int(page) + 1):
            if i <= 20:  # max:10*20=200 ; 20181005 -只能爬取20页,每页10条!!!!!!
                url = 'http://wenshu.court.gov.cn/List/ListContent'
                data = {
                    'Param': '裁判日期:{}  TO {}'.format(response.meta['date'], response.meta['date']),
                    # 检索筛选条件 (多条件筛选: 裁判年份:2018,中级法院:北京市第一中级人民法院,审判程序:一审,关键词:返还)
                    'Index': str(i),  # 页数
                    'Page': '10',  # 每页显示的条目数
                    'Order': '裁判日期',  # 排序类型(1.法院层级/2.裁判日期/3.审判程序)
                    'Direction': 'asc',  # 排序方式(1.asc:从小到大/2.desc:从大到小)
                    'vl5x': self.vl5x,  # 保存1个小时
                    'number': 'wens',
                    'guid': self.guid
                }
                headers = {
                    # 再次自己准备cookie
                    'Cookie': 'vjkl5=' + self.vjkl5,
                    'Host': 'wenshu.court.gov.cn',
                    'Origin': 'http://wenshu.court.gov.cn',
                }
                yield scrapy.FormRequest(url, formdata=data, meta={'date': response.meta['date']},
                                         callback=self.get_docid, headers=headers, dont_filter=True)

    def get_docid(self, response):
        """获取一个json数据的DocId，到这里就成功啦！"""
        html = response.text
        result = eval(json.loads(html))
        runeval = result[0]['RunEval']
        content = result[1:]
        # print(response.request.headers['Cookie'])
        for i in content:
            casewenshuid = i.get('文书ID', '')
            docid = self.decrypt_id(runeval, casewenshuid)
            # print('*************文书ID:' + docid)
            # 只需要docid和判决日期
            # count_num += 1
            item = WenshuDocidItem()
            item['docid'] = docid
            item['judgedate'] = response.meta['date']
            yield item
        # 输出时间
        now_time = datetime.datetime.now().strftime('%H:%M:%S')
        print('***时间: {}'.format(now_time))

    def decrypt_id(self, RunEval, id):
        """docid解密"""
        js = self.js_2.call("GetJs", RunEval)
        js_objs = js.split(";;")
        js1 = js_objs[0] + ';'
        js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
        key = self.js_2.call("EvalKey", js1, js2)
        key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]
        docid = self.js_2.call("DecryptDocID", key, id)
        return docid
