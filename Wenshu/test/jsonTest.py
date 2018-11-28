# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  jsonTest.py
@time:  2018/11/22
"""
import json
import re

import execjs


with open('D:\AllCode\python\Wenshu_Project\items.json', encoding='utf-8') as f:
    text = f.read()

l = json.loads(text)
print(type(l[0]))
for i in l:
    d = json.loads(i['json_data'])
    s = eval(d)
    print(type(mp[0]))
    print(d)
