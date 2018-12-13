# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  count_all.py
@time:  2018/12/12
"""
import datetime
import os
import re
import sys

BEGIN_DATE = '2001-01-01'
ENDED_DATE = '2011-12-31'

FILE_RELA_PATH = '../../answer/'


class TimeUtils(object):
    @staticmethod
    def get_between_day(b_date, e_date):
        """
        获取区间每一天的生成器
        :param begin_date: str 开始日期
        :param end_date: str 结束日期，默认为当前日期
        :return: str
        """
        b_date = datetime.datetime.strptime(b_date, "%Y-%m-%d")
        e_date = datetime.datetime.strptime(e_date, "%Y-%m-%d")
        while b_date <= e_date:
            date_str = b_date.strftime("%Y-%m-%d")
            b_date += datetime.timedelta(days=1)
            yield date_str


class CountAll(object):

    def __init__(self, b_date=BEGIN_DATE, e_date=ENDED_DATE, rela_path=FILE_RELA_PATH):
        self.b_date = b_date
        self.e_date = e_date
        self.rela_path = rela_path
        self.pattern = re.compile(',')
        self.num = 0

    def count(self):

        for date in TimeUtils.get_between_day(self.b_date, self.e_date):
            filename = date + '.txt'
            tp_num = self.count_file(filename)
            self.num += tp_num
            print('文件名:{}, 文书个数:{}'.format(filename, tp_num))
        print('日期:{} to {}, 文书个数:{}'.format(self.b_date, self.e_date, self.num))

    def count_file(self, filename):

        # 一个年份一个文件夹
        year = filename[:4]
        dirpath = self.rela_path + year + '/'

        if not os.path.exists(dirpath+filename):
            return 0

        with open(dirpath + filename, 'r', encoding='utf-8') as f:
            text = f.read()

        return len(self.pattern.findall(text))


if __name__ == '__main__':
    try:
        year = sys.argv[1]
        b_date = year + '-01-01'
        e_date = year + '-12-31'
        c = CountAll(b_date, e_date)
        c.count()
    except IndexError:
        c = CountAll()
        c.count()



