# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  getdocid.py
@time:  2018/11/29
"""
import datetime
import os
import sys
import time

import execjs


BEGIN_DATE = '2001-01-01'
ENDED_DATE = '2001-01-01'


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


class GetDocId(object):

    def __init__(self, b_date=BEGIN_DATE, e_date=ENDED_DATE, rela_path=FILE_RELA_PATH):
        with open('get_file_docids.js', encoding='utf-8') as f:
            decry_js = f.read()
        self.decry_js = execjs.compile(decry_js)

        self.b_date = b_date
        self.e_date = e_date
        self.rela_path = rela_path

    def work(self, filepath):
        """
        调用nodejs解密整个文件内容
        :param filepath: 文件路径
        :return:
        """
        if not os.path.exists(filepath):
            return 0

        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        docids_list = self.decry_js.call("get_file_ids", text)

        topath = filepath.split('.txt')[0]
        topath += '-id.txt'
        with open(topath, 'w', encoding='utf-8') as f:
            for docid in docids_list:
                f.write(docid + '\n')
        return len(docids_list)

    def works(self):
        """
        解决一段日期的文件
        :param begin_date:
        :param end_date:
        :return:
        """
        total = 0
        for date in TimeUtils.get_between_day(self.b_date, self.e_date):
            year = date[:4]
            dirpath = self.rela_path + year + '/'
            filepath = dirpath + date + '.txt'
            num = self.work(filepath)
            print('日期:{0}, 文书数量: {1}'.format(date, num))
            total += num
        return total


if __name__ == '__main__':

    args = sys.argv

    if len(args) == 2:  # 一个参数，输入年份
        b_date = args[1] + '-01-01'
        e_date = args[1] + '-12-31'
        c = GetDocId(b_date, e_date)
    elif len(args) == 3:  # 两个参数，开始日期和结束日期
        c = GetDocId(args[1], args[2])
    else:  # 没有参数，或者多了
        c = GetDocId()

    cur_time = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
    total = c.works()
    print('******开始时间：' + cur_time)
    print('******解析总数: {}'.format(total))
    cur_time = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
    print('******结束时间：' + cur_time)
