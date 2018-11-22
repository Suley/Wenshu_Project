# -*- coding: utf-8 -*-
import datetime

import scrapy, json, re, math, execjs
from Wenshu.items import WenshuDocidItem
from Wenshu.spiders.utils import timeutils


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
        self.guid = 'aaaabbbb-aaaa-aaaabbbb-aaaabbbbcccc'
        with open(r'Wenshu/spiders/get_vl5x.js', encoding='utf-8') as f:
            jsdata_1 = f.read()
        with open(r'Wenshu/spiders/docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_1 = execjs.compile(jsdata_1)
        self.js_2 = execjs.compile(jsdata_2)

    def parse(self, response):
        """获取cookie"""
        try:
            vjkl5 = response.headers['Set-Cookie'].decode('utf-8')
            # print('******cookie:' + vjkl5)
            vjkl5 = vjkl5.split(';')[0].split('=')[1]
            url_num = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
            data = {
                'guid': self.guid
            }
            yield scrapy.FormRequest(url_num, formdata=data, meta={'vjkl5': vjkl5}, callback=self.get_count,
                                     dont_filter=True)
        except:
            yield scrapy.Request(WenshuSpider.start_urls, callback=self.parse, dont_filter=True)

    def get_count(self, response):
        """获取案件数目,设置请求页数"""
        # K4CBNQLY 获取到一个奇怪的码,解密后用来请求json
        number = response.text
        # response 获取到开始时候在request设置的的vjkl5
        vjkl5 = response.meta['vjkl5']
        # 获取到 vl5x
        vl5x = self.js_1.call('getvl5x', vjkl5)
        # 网页也是，先算出vl5x再提交一个form请求获取页面的json数据
        url = 'http://wenshu.court.gov.cn/List/ListContent'
        for date in self.get_date:
            data = {
                'Param': '裁判日期:{}  TO {}'.format(date, date),
                # 检索筛选条件 (多条件筛选: 裁判年份:2018,中级法院:北京市第一中级人民法院,审判程序:一审,关键词:返还)
                'Index': '1',  # 页数
                'Page': '10',  # 只为了获取案件数目,所有请求0条就行了
                'Order': '裁判日期',  # 排序类型(1.法院层级/2.裁判日期/3.审判程序)
                'Direction': 'asc',  # 排序方式(1.asc:从小到大/2.desc:从大到小)
                'vl5x': vl5x,
                'number': number,
                'guid': self.guid
            }
            headers = {
                # 在这单独添加cookie,settings中就可以禁用cookie,防止跟踪被ban
                'Cookie': 'vjkl5=' + response.meta['vjkl5'],
                'Host': 'wenshu.court.gov.cn',
                'Origin': 'http://wenshu.court.gov.cn',
            }
            # print(response.request.headers.getlist('Cookie'))
            yield scrapy.FormRequest(url, formdata=data,
                                     meta={'vl5x': vl5x, 'vjkl5': vjkl5, 'number': number, 'date': date},
                                     callback=self.get_content, headers=headers, dont_filter=True)

    def get_content(self, response):
        """获取每页的案件"""
        # 这里其实是处理和显示 get_count 函数的response
        html = response.text
        result = eval(json.loads(html))
        count = result[0]['Count']
        print('*******{}:该日期下数据数据量:{}'.format(response.meta['date'], count))
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
                    'vl5x': response.meta['vl5x'],  # 保存1个小时
                    'number': response.meta['number'],
                    'guid': self.guid
                }
                headers = {
                    # 再次自己准备cookie
                    'Cookie': 'vjkl5=' + response.meta['vjkl5'],
                    'Host': 'wenshu.court.gov.cn',
                    'Origin': 'http://wenshu.court.gov.cn',
                }
                yield scrapy.FormRequest(url, formdata=data, meta={'date': response.meta['date']},
                                         callback=self.get_docid, headers=headers, dont_filter=True)

    def get_docid(self, response):
        """计算出docid"""
        html = response.text
        result = eval(json.loads(html))
        runeval = result[0]['RunEval']
        content = result[1:]
        count_num = 0
        for i in content:
            casewenshuid = i.get('文书ID', '')
            docid = self.decrypt_id(runeval, casewenshuid)
            # print('*************文书ID:' + docid)
            # 只需要docid和判决日期
            count_num += 1
            item = WenshuDocidItem()
            item['docid'] = docid
            item['judgedate'] = response.meta['date']
            yield item

            # url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(docid)
            # yield scrapy.Request(url, callback=self.get_detail, dont_filter=True)
        # 输出时间
        now_time = datetime.datetime.now().strftime('%H:%M:%S')
        print('******时间:{},爬了{}个!!!'.format(now_time, count_num))

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

    # def get_detail(self, response):
    #     '''获取每条案件详情'''
    #     html = response.text
    #     content_1 = json.loads(re.search(r'JSON.stringify\((.*?)\);', html).group(1))  # 内容详情字典1
    #     content_2 = re.findall(r'value: "(.*?)"', html)  # 内容详情字典2 #2/3/5/6
    #     content_3 = re.search(r'"Html\\":\\"(.*?)\\"}', html).group(1)  # 内容详情字典3(doc文档正文)
    #     len2 = len(content_2)
    #     reg = re.compile(r'<[^>]+>', re.S)
    #     # 存储到item
    #     item = WenshuCaseItem()
    #     item['casecourt'] = {
    #         'casecourtid': content_1.get('法院ID', 'null'),
    #         'casecourtname': content_1.get('法院名称', 'null'),
    #         'casecourtprovince': content_1.get('法院省份', 'null'),
    #         'casecourtcity': content_1.get('法院地市', 'null'),
    #         'casecourtdistrict': content_1.get('法院区县', 'null'),
    #         'casecourtarea': content_1.get('法院区域', 'null'),
    #     }
    #     item['casecontent'] = {
    #         'casebasecontent': content_1.get('案件基本情况段原文', 'null'),
    #         'caseaddcontent': content_1.get('附加原文', 'null'),
    #         'caseheadcontent': content_1.get('文本首部段落原文', 'null'),
    #         'casemaincontent': content_1.get('裁判要旨段原文', 'null'),
    #         'casecorrectionscontent': content_1.get('补正文书', 'null'),
    #         'casedoccontent': content_1.get('DocContent', 'null'),
    #         'caselitigationcontent': content_1.get('诉讼记录段原文', 'null'),
    #         'casepartycontent': content_1.get('诉讼参与人信息部分原文', 'null'),
    #         'casetailcontent': content_1.get('文本尾部原文', 'null'),
    #         'caseresultcontent': content_1.get('判决结果段原文', 'null'),
    #         'casestrcontent': reg.sub('', content_3),  # 去除html标签后的文书内容
    #     }
    #     item['casetype'] = content_2[1] if len2 >= 2 else 'null'  # 案件类型
    #     item['casereason'] = content_2[2] if len2 >= 3 else 'null'  # 案由
    #     item['casejudgedate'] = content_2[4] if len2 >= 5 else 'null'  # 判决日期
    #     item['caseparty'] = content_2[5] if len2 >= 6 else 'null'  # 当事人
    #     item['caseprocedure'] = content_1.get('审判程序', 'null')
    #     item['casenumber'] = content_1.get('案号', 'null')
    #     item['casenopublicreason'] = content_1.get('不公开理由', 'null')
    #     item['casedocid'] = content_1.get('文书ID', 'null')
    #     item['casename'] = content_1.get('案件名称', 'null')
    #     item['casecontenttype'] = content_1.get('文书全文类型', 'null')
    #     item['caseuploaddate'] = time.strftime("%Y-%m-%d",
    #                                            time.localtime(int(content_1['上传日期'][6:-5]))) if 'Date' in content_1[
    #         '上传日期'] else 'null'
    #     item['casedoctype'] = content_1.get('案件名称').split('书')[0][-2:] if '书' in content_1.get(
    #         '案件名称') else '令'  # 案件文书类型:判决或者裁定...还有令
    #     item['caseclosemethod'] = content_1.get('结案方式', 'null')
    #     item['caseeffectivelevel'] = content_1.get('效力层级', 'null')
    #     yield item
