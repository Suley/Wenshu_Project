# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  court.py
@time:  2018/12/04
"""
import json


class InnerCourt(object):

    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.son_keys = []


class Court(object):

    def __init__(self):
        self.mp = {'001000': InnerCourt('001000', '最高人民法院')}

        # 默认自动读取
        with open('Wenshu/utils/regionAndcourt/court.json', 'r', encoding='utf-8') as f:
            dic = json.loads(f.read())
            for i in dic:
                self.add_court(i)

    def add_court(self, jsdata):
        key = jsdata['key']
        name = jsdata['name']

        tail = key[-3:]
        if tail == '000':
            pkey = key[:-6] + '000'
        else:
            pkey = key[:-3] + '000'

        self.mp[key] = InnerCourt(key, name)
        self.mp[pkey].son_keys.append(key)

    def get_son_keys(self, key):
        """
        返回key对应的法院辖区的子法院list
        :param key: 法院key
        :return: 子法院list_id
        """
        return self.mp[key].son_keys

    def show_court(self, key="001000"):
        print('key: {}, name: {}'.format(key, self.mp[key].name))
        lis = self.get_son_keys(key)
        for i in lis:
            self.show_court(i)


if __name__ == '__main__':
    c = Court()
    c.show_court()


