# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  NoneTest.py
@time:  2018/11/26
"""
import scrapy
from scrapy import FormRequest
from scrapy import Request

wode = '111111111111111111111111'
s = 'Param=%E8%A3%81%E5%88%A4%E6%97%A5%E6%9C%9F%3A2007-12-29++TO+2007-12-29&Index=4&Page=10&Order=%E8%A3%81%E5%88%A4%E6%97%A5%E6%9C%9F&Direction=asc&vl5x=6e2a742531236c9ec227f52d&number=wens&guid=5969ecb9-eabf-2fac9283-6d278d8fda1b'


class A(object):
    def __init__(self):
        self._body = s.encode('utf-8')


a = A()
s = a._body.decode('utf-8')
print(s)
index = s.find('vl5x=')
s = s[:index+5] + wode + s[index+29:len(s)]
print(s)
a._body = s.encode('utf-8')
print(a._body)

x = FormRequest("http://www.baidu.com")
print(type(x))
print(type(x) == FormRequest)


