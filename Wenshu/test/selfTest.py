# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  selfTest.py
@time:  2018/11/16
"""


class A:
    def __init__(self):
        print("***A construct***")
        self.n = 2

    def add(self, m):
        print('self is {0} @A.add'.format(self))
        self.n += m


class B(A):
    n = 5

    def __init__(self):
        print("***B construct***")

    def add(self, m):
        print('self is {0} @B.add'.format(self))
        super().add(m)
        self.n += 3

    def get_n(self):
        return self.n


b = B()
b.add(2)
print(b.get_n())
