# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  timeutils.py
@time:  2018/11/19
"""
import datetime
import time


class TimeUtils(object):

    @staticmethod
    def get_between_day(begin_date, end_date=None):
        """ 获取区间每一天
        :param begin_date: str 开始日期
        :param end_date: str 结束日期，默认为当前日期
        :return: 生成器
        """
        if end_date is None:
            end_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            begin_date += datetime.timedelta(days=1)
            yield date_str


if __name__ == '__main__':
    for i in TimeUtils.get_between_day("2000-01-01", "2001-01-01"):
        print(i)
