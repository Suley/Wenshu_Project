# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

import execjs
import requests
from scrapy import signals, FormRequest
import random


# 代理池接口地址,可以自己搭
PROXY_SERVER_one = "http://172.19.105.82:8887/resouce/getproxy?num=1"
PROXY_SERVER_1000 = "http://172.19.105.82:8887/resouce/getproxy?num=1000"
COOKIE_URL = 'http://wenshu.court.gov.cn/list/list/?sorttype=1'


# 随机User-Agent
class RandomUserAgentMiddleware(object):
    def __init__(self, agents):
        """接收从from_crawler传的List-agents"""
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        """从settings读取USER_AGENTS，传参到构造函数"""
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        """修改每一个request的header"""
        request.headers.setdefault('User-Agent', random.choice(self.agents))


# 代理服务器
class ProxyMiddleware(object):

    def __init__(self):
        """准备连接动态代理的基本信息"""
        self.num = 0
        self.proxys = requests.get(PROXY_SERVER_1000).text.split(',')
        self.proxies_error_time = 1

    def request_proxies(self):
        try:
            return requests.get(PROXY_SERVER_1000, timeout=8).text.split(',')
        except:
            if self.proxies_error_time < 300:
                self.proxies_error_time *= 2
            print('请求代理服务失败...休眠 %s 秒' % self.proxies_error_time)
            time.sleep(self.proxies_error_time)
            return None

    def process_request(self, request, spider):
        """处理请求request"""
        if self.num > 800:
            while True:
                proxys = requests.get(PROXY_SERVER_1000).text.split(',')
                if proxys:
                    self.proxys = proxys
                    self.num = 0
                    self.proxies_error_time = 1
                    break
        request.meta['proxy'] = 'http://' + self.proxys[self.num]
        self.num += 1

    def process_response(self, request, response, spider):
        """处理返回的response"""
        try:
            html = response.body.decode()
        except UnicodeDecodeError:
            html = None

        if response.status != 200 or html is None or 'remind' in html or '请开启JavaScript' in html or '服务不可用' in html:
            return request.copy()
        else:
            return response

    def process_exception(self, request, exception, spider):
        """处理异常，复制一份request"""
        return request.copy()


# 更新vjkl5的中间件
class Vjkl5Middleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        """从settings读取USER_AGENTS，传参到构造函数"""
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def __init__(self, agents):
        """准备工作"""
        with open('Wenshu/spiders/get_vl5x.js', encoding='utf-8') as f:
            jsdata_1 = f.read()
        self.js_1 = execjs.compile(jsdata_1)
        self.agents = agents
        self.num = 0
        self.vjkl5 = None
        self.vl5x = None

    def process_request(self, request, spider):
        """修改vjkl5"""
        self.num += 1
        if self.num > 800:
            # 重试3次
            tp_vjkl5 = None
            for i in range(3):
                tp_vjkl5 = self.request_cookie()
                if tp_vjkl5 is not None:
                    break
            if tp_vjkl5 is not None:
                self.vjkl5 = tp_vjkl5
                self.vl5x = self.js_1.call('getvl5x', tp_vjkl5)
                # 爬虫的request也更新
                spider.vjkl5 = self.vjkl5
                spider.vl5x = self.vl5x
                print("***新的vlx5:" + self.vl5x)
            else:
                print("***更新vlx5失败")
            self.num = 0

        # FormRequest的修改form表单需要编码
        if self.vjkl5 is not None and type(request) == FormRequest:
            # 修改form表单！！！访问私有属性，堪称无敌，request.replace() 需要重新构造一个dict，还不如这样
            s = request._body.decode('utf-8')
            index = s.find('vl5x=')
            s = s[:index + 5] + self.vl5x + s[index + 29:len(s)]
            request._body = s.encode('utf-8')
            # 修改headers
            request.headers.setdefault('Cookie', 'vjkl5={0}'.format(self.vjkl5).encode('utf-8'))

    def request_cookie(self):
        """
        请求文书网的cookie
        :return: 返回vjkl5
        """
        proxy_url = requests.get(PROXY_SERVER_one).text
        # 代理
        proxies = {"http": "http://" + proxy_url}
        headers = {"User-Agent": random.choice(self.agents)}
        try:
            res = requests.get(COOKIE_URL, headers=headers, proxies=proxies, timeout=8)
            tp_vjkl5 = res.headers['Set-Cookie']
            tp_vjkl5 = tp_vjkl5.split(';')[0].split('=')[1]
            return tp_vjkl5
        except:
            return None


# 法一:连接阿布云动态代理隧道(付费:IP质量好)
# class ProxyMiddleware(object):
#     def __init__(self):
#         """准备连接动态代理的基本信息"""
#         # 阿布云代理服务器, 记得要买动态版的
#         self.proxyServer = "http://http-dyn.abuyun.com:9020"
#         # 代理隧道验证信息
#         proxyUser = "******填写阿布云通行证*******"
#         proxyPass = "******填写阿布云通行密钥*****"
#         # python 3
#         self.proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
#         # self.proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass) # Python2
#
#     # 修改request头
#     def process_request(self, request, spider):
#         """处理请求request"""
#         request.headers['Proxy-Authorization'] = self.proxyAuth
#         request.meta['proxy'] = self.proxyServer
#
#     def process_response(self, request, response, spider):
#         """处理返回的response"""
#         # print(response.url)
#         html = response.body.decode()
#         if response.status != 200 or 'remind key' in html or 'remind' in html or '请开启JavaScript' in html or '服务不可用' in html:
#             # print('正在重新请求************')
#             new_request = request.copy()
#             # 为了重复请求不被过滤
#             new_request.dont_filter = True
#             return new_request
#         else:
#             return response
#
#     def process_exception(self, request, exception, spider):
#         new_request = request.copy()
#         new_request.dont_filter = True
#         return new_request


# 默认的中间件提示
class WenshuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WenshuDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
