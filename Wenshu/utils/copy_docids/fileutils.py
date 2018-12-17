# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  fileutils.py
@time:  2018/12/17
"""
import datetime
import os
import shutil
import sys
import time

BEGIN_DATE = '2001-01-01'
ENDED_DATE = '2018-12-10'

SRC_FILE_PATH = '../../answer'
DST_FILE_PATH = '../../docids'


class TimeUtils(object):

    @staticmethod
    def get_between_day(b_date, e_date):
        b_date = datetime.datetime.strptime(b_date, "%Y-%m-%d")
        e_date = datetime.datetime.strptime(e_date, "%Y-%m-%d")
        while b_date <= e_date:
            date_str = b_date.strftime("%Y-%m-%d")
            b_date += datetime.timedelta(days=1)
            yield date_str


class FileUtils(object):
    @staticmethod
    def get_file_path_and_name(filepath):
        strlist = filepath.split('/')
        fpath = ''
        for i in range(len(strlist)-1):
            fpath += strlist[i] + '/'
        fname = strlist[-1]
        return fpath, fname

    @staticmethod
    def copy_file(srcfile, dstfile):
        if not os.path.isfile(srcfile):
            print("源文件: %s 不存在!" % srcfile)
        else:
            fpath, fname = FileUtils.get_file_path_and_name(dstfile)   # 分离文件名和路径
            print(fpath, fname)
            if not os.path.exists(fpath):
                os.makedirs(fpath)                # 创建路径
            shutil.copyfile(srcfile, dstfile)      # 复制文件
            print("复制 %s -> %s" % (srcfile, dstfile))

    @staticmethod
    def copy_all_docids(b_date, e_date):
        src_path_temp = '{}/{}/{}{}.txt'
        dst_path_temp = '{}/{}/{}{}.txt'
        for day in TimeUtils.get_between_day(b_date, e_date):
            year = day[:4]
            src_filepath = src_path_temp.format(SRC_FILE_PATH, year, day, '-id')
            dst_filepath = dst_path_temp.format(DST_FILE_PATH, year, day, '-id')
            FileUtils.copy_file(src_filepath, dst_filepath)


if __name__ == '__main__':
    args = sys.argv

    cur_time = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))

    if len(args) == 2:  # 一个参数，输入年份
        b_date = args[1] + '-01-01'
        e_date = args[1] + '-12-31'
        FileUtils.copy_all_docids(b_date, e_date)
    elif len(args) == 3:  # 两个参数，开始日期和结束日期
        FileUtils.copy_all_docids(args[1], args[2])
    else:  # 没有参数，或者多了
        FileUtils.copy_all_docids(BEGIN_DATE, ENDED_DATE)

    print('******开始时间：' + cur_time)
    cur_time = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
    print('******结束时间：' + cur_time)




