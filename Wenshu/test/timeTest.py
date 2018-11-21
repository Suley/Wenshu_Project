# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  timeTest.py
@time:  2018/11/19
"""
import datetime
import time


def get_between_day(begin_date, end_date=None):
    if end_date is None:
        end_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        begin_date += datetime.timedelta(days=1)
        yield date_str


# for i in get_between_day("2012-01-01"):
#     print(i)

now_time = datetime.datetime.now().strftime('%H:%M:%S')
print(now_time)