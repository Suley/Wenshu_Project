# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  maptree2.py
@time:  2018/11/27
"""
import json


class InnerCase(object):

    def __init__(self, cid, cname, pid=None):
        self.id = cid
        self.name = cname
        self.pid = pid
        self.son_list = []


class WenshuCase(object):

    def __init__(self):
        self.mp = {'#': InnerCase('#', '请选择')}
        # 默认自动读取case.json文件
        with open('Wenshu/utils/case/case.json', encoding='utf-8') as f:
            text = f.read()
        json_data = json.loads(text)
        for i in json_data:
            self.add_case(i)

    def add_case(self, case):
        """
        新增一个案由
        :param case: 字典格式的案由
        :return: True
        """
        cid = case['id']
        cname = case['name']
        pid = case['parentId']
        self.mp[cid] = InnerCase(cid, cname, pid)
        self.mp[pid].son_list.append(cid)

    def display_all_case(self):
        """
        显示所有的案由
        :return:
        """
        self.display_case('#')

    def display_case(self, id):
        """
        递归显示一个案由下所有子案由
        :param id: id
        :param pid: parentid,可以不写
        :return:
        """
        cas = self.mp[id]
        print('id: {0}, name: {1}, pid: {2}'.format(id, cas.name, cas.pid))
        for i in cas.son_list:
            self.display_case(i)


if __name__ == '__main__':
    w = WenshuCase()
    w.display_all_case()
