# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  nodejs_test.py
@time:  2018/12/11
"""
import execjs

with open('xiaxie.js', encoding='utf-8') as f:
    jsdata_2 = f.read()
js_2 = execjs.compile(jsdata_2)

while True:
    x = js_2.call("GetJs")


# with open('../spiders/docid.js', encoding='utf-8') as f:
#     jsdata_2 = f.read()
# js_2 = execjs.compile(jsdata_2)
#
# while True:
#     js = js_2.call("GetJs", 'w61aS8KOwoMwDD0LwqjCi0TCjMOmAsKowqseYcKWVsKEKsO6YzFlwpQywqvCqncfwqDCiMOySQMdAk3DqcKTwpArEsObw49+ThwidXHCiDbDm1MowqPCn2TDucKVw4jDqMK4w7/DnMOJw7h7dVjDi1XCvMOZMsOPw7FIQFgtPkACw4R7wqzCkDkkw7Imw5sVXQnCtcKFAMOvYBYCw5UDYyguEgYnYAd0IHXDpA8Sw4AEwohBw5bDoAnDiSElVAACC8OBQsOBfT9YwrphfDwlw7I3TGLDqcO6AQUifRjDs8OOwpdMwq18w44XTldLSsKFEB5zw7IJTnXCn8OZRMO3TMO+wrrCuMO9O8KBWDbCnGrCkMKTw43CkMKgw7TCpwFYV3cKwoPDu2DCjcK4wpXCusOawpjCqsOew5TDoyVUHnXCm8KiVgjDihw0wr7DiyDDuzFaecOtDMK7wqfDhiNqD8Orw77Dj2DCgMOVUFMjw7bCncO7w4TCgHvDg8KeXsOAXcK5F8KLwo5FeQcZFW1cw4cTeMKfCmLCshXCrwXCp1rCp8Kkw47Crm8ew5lswrLDtw/CnnkXFMOew63DgTEHw7bChMOWwq3CjWXDnMKdNcOOw6Fnw4F3wo1hw5gnw4U0PcK2wqE9NCsnL1M8TRTDjcODwr/Dl33Dk0rCvhTDl8OLVnJUw6vDoMOqw5HCqkMacEHCtsKIPMOEU8KBw6XCjMO7fw==')
#