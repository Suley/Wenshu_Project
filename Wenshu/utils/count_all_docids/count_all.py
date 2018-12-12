# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  count_all.py
@time:  2018/12/12
"""
import datetime
import re
import sys

BEGIN_DATE = '2001-01-01'
ENDED_DATE = '2001-01-01'

FILE_RELA_PATH = '../../answer/'


class CountAll(object):

    def __init__(self, b_date=BEGIN_DATE, e_date=ENDED_DATE, rela_path=FILE_RELA_PATH):
        self.b_date = b_date
        self.e_date = e_date
        self.rela_path = rela_path
        self.num = 0

    def get_between_day(self, b_date, e_date):
        begin_date = datetime.datetime.strptime(b_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(e_date, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            begin_date += datetime.timedelta(days=1)
            yield date_str

    def count(self):

        for date in self.get_between_day(self.b_date, self.e_date):
            filename = date + '.txt'
            tp_num = self.count_file(filename)
            self.num += tp_num
            print('文件名:{}, 文书个数:{}'.format(filename, tp_num))
        print('日期:{} to {}, 文书个数:{}'.format(self.b_date, self.e_date, self.num))

    def count_file(self, filename):

        # 一个年份一个文件夹
        year = filename[:4]
        dirpath = self.rela_path + year + '/'

        with open(dirpath + filename, 'r', encoding='utf-8') as f:
            text = f.read()
        return len(re.findall(',', text))


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



