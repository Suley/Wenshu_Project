# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  getdocid.py
@time:  2018/11/29
"""

import re
import time

import execjs

# from timeutils import get_between_day
from Wenshu.utils.timeutils import get_between_day


class GetDocId(object):

    def __init__(self):
        with open('../spiders/docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_2 = execjs.compile(jsdata_2)

    def work(self, filepath):
        # 解析全部的id
        lis = []
        for i in self.get_docids(filepath):
            lis.append(i)

        topath = filepath.split('.txt')[0]
        topath += '-id.txt'
        with open(topath, 'w', encoding='utf-8') as f:
            for i in lis:
                f.write(i + '\n')
        print("解析文件 {} 完成, 共 {} 个.".format(filepath, len(lis)))
        return len(lis)

    def works(self, begin_date, end_date):
        """
        解决一段日期的文件
        :param begin_date:
        :param end_date:
        :return:
        """
        num = 0
        for date in get_between_day(begin_date, end_date):
            year = date[:4]
            dirpath = '../answer/' + year + '/'
            filepath = dirpath + date + '.txt'
            temp = self.work(filepath)
            print('日期 {0} 下文书数量: {1}'.format(date, temp))
            num += temp
        return num

    def get_docids(self, filepath):
        """
        解析docid
        :param filepath: 文件路径
        :return:
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.read()
            lis = lines.split('\n')[:-1]

        for data in lis:
            arr = data.split(',')
            runeval = arr[0]
            cids = arr[1:]
            for doc_id in self.decrypt_id(runeval, cids):
                yield doc_id
            cur_time = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
            print("时间: {}, 解析: {}个".format(cur_time, len(cids)))

    def decrypt_id(self, runeval, cids):
        """
        docid解密，必须传入一组json
        :param runeval: 运行参数
        :param cids: 待解密id列表
        :return: docid
        """
        js = self.js_2.call("GetJs", runeval)
        js_objs = js.split(";;")
        js1 = js_objs[0] + ';'
        js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
        key = self.js_2.call("EvalKey", js1, js2)
        key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]

        for cid in cids:
            yield self.js_2.call("DecryptDocID", key, cid)


if __name__ == '__main__':
    c = GetDocId()

    begin_date = '2018-07-12'
    end_date = '2018-07-12'

    cur_time = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
    num = c.works(begin_date, end_date)
    print('开始时间：' + cur_time)
    print('******解析总数: {}'.format(num))
    cur_time = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))
    print('结束时间：' + cur_time)
