# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  setTest.py
@time:  2018/12/05
"""

with open(r'D:\AllCode\python\Wenshu_Project\Wenshu\answer\2010\2010-05-10-id.txt', 'r', encoding='utf-8') as f:
    tx = f.read()

lis = tx.split('\n')[:-1]
s = set()
for i in lis:
    s.add(i)

print(len(s))
