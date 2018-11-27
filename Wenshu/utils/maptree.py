# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  maptree.py
@time:  2018/11/26
"""
import json


class WenshuCase(object):

    def __init__(self):
        # id -> list[son_id]
        self.index_mp = {'#': []}
        # id -> name
        self.name_mp = {'#': '请选择'}
        # 默认自动读取case.json文件
        with open('case.json', encoding='utf-8') as f:
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
        id = case['id']
        pid = case['parentId']
        name = case['name']
        if pid in self.index_mp.keys():
            self.index_mp[pid].append(id)
            self.index_mp[id] = []
            self.name_mp[id] = name
            return True
        else:
            raise KeyError('pid is not existence')

    def display_all_case(self):
        """
        显示所有的案由
        :return:
        """
        self.display_case('#', None)

    def display_case(self, id, pid=None):
        """
        递归显示一个案由下所有子案由
        :param id: id
        :param pid: parentid,可以不写
        :return:
        """
        l = self.index_mp[id]
        print('id: {0}, name: {1}, pid: {2}'.format(id, self.name_mp[id], pid))
        for i in l:
            self.display_case(i, id)


if __name__ == '__main__':
    w = WenshuCase()
    w.display_all_case()
