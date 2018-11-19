# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  pyTest.py
@time:  2018/11/15
"""
import urllib.request

proxystr = urllib.request.urlopen('http://172.19.105.82:8887/resouce/getproxy?num=1').read().decode('utf-8')
print(proxystr)
