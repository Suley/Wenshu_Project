# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  NoneTest.py
@time:  2018/11/26
"""
import os

dirpath = '../answer/2017/'

isexists = os.path.exists(dirpath)
if not isexists:
    os.makedirs(dirpath)

