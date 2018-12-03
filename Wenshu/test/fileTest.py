# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  fileTest.py
@time:  2018/12/03
"""

num = 0
for i in range(5):
    with open('hello.txt', 'a', encoding='utf-8') as f:
        f.writelines("hello{}\n".format(num))
        num += 1

with open('hello.txt', 'r', encoding='utf-8') as f:
    text = f.read()
print(text)
