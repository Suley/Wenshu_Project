# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  region.py
@time:  2018/12/04
"""
from Wenshu.utils.regionAndcourt.court import Court


class InnerRegion(object):

    def __init__(self, key, name, court_key):
        self.key = key
        self.name = name
        # 下属高级人民法院id
        self.court_key = court_key


class Region(object):

    def __init__(self):
        self.mp = {}
        # 默认打开region.txt文件
        with open('Wenshu/utils/regionAndcourt/region.txt', 'r', encoding='utf-8') as f:
            lis = f.read().split('\n')
            for i in range(len(lis)):
                key = i+1
                name = lis[i]
                ckey = '001' + ('%03d' % key) + '000'
                self.mp[key] = InnerRegion(key, name, ckey)

    def get_regions(self):
        for i in range(1, 32):
            yield i, self.mp[i+1].name

    def show_region(self, key):
        print('key: {}, name: {}, court_key: {}'.format(key, self.mp[key].name, self.mp[key].court_key))


if __name__ == '__main__':
    r = Region()
    c = Court()
    for i, j in r.get_regions():
        print(i, j)
