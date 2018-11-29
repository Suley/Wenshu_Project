# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  doSomeTest.py
@time:  2018/11/15
"""
import logging
import re

import execjs


runeval = 'w61ZS27CgzAQPQtRFsK2wqh6AcKUVcKOw5DDpcOIQhVJGxYNwpVDV1HDrl7CoMKUw7IxwoHClMOYwp3DgsKTw5BEw5jDs3nDs8OGHmxlfcKId8O7U8Kkw6PDt3TDs8KUw6rDuMO4w7rDuMKiwpPCt8Otw6FZb8KTw51ew7jCnk8KwoLCtXgACRDDi1ghc0hkIcObFV0JwrXChQDDr2AWAsOVA2MoLjgBO8KgA8KpwoMJw6QPEkAMEgZPSA4pwqECEFgIw4zChQzCgnDCs8KKwpLDoynDlR9RwprDqFUQUsKowrJHCMO/fMOJw5XCqsOnfMKRw7RlScKZUMOKF14xIcKpw6kzwp8Ywp4pXsOXP8O/w5PCk8OIwoczDcOyw7IZUsKUw73CtAI2w5XCvcOSwqA/WAvCt1HDtyrCpsK6N8OzeBXCqkDDncKlwqgDw4HCmMODFcOfFcOIccKMw5ZeB2HCj8OUwrhFw61mw53DnxlMwrDCmmp6F8O7w7s5w6EIw4fChjvCtnnDlh3Ci8OWVsKkw4HCtsOCwogXYw42UcObwq3ChgPDrw3DmsO6PgDCrXbDnMKnNxcWwqrDj8Kdw7PDqMKuwoLCscOtwpN/wr/DmMOtLsOicnF9wp8Mw79xw43CrcOSw6h0wr8NR3QPw4fDsWbCmFd3W0IwRsKxSwDCnVPDgsKYKyk3wpYMwpfDj8Ouw6nCp8ORw4LDjcKjdcKHNMOhw7rDjMKDN0BRUsOIw6AT'

# casewenshuid = 'FcKNw4ENADEIw4NWCi0UeALChcO9R8K6w54rwpbDoihnwozCtsKSWsOKwqHDmcOkwrZMwqFZw4TDu2LDsyXChsKdwoUuURXDgTTDoG0+FsK+w4rCqVUow6w8wovCuyomUighw6zCuHPCtjNJw4PCk8Oiw5kpL1dpwplVFGPDhcOZBcKJa8KdwpvCvcOYw7/Cg8KLw4zCrMOrHMOVOsOTwoEFwrDDsnNJF8Kxw5/DpcKcwolmHsOsYsOBwqHDl8OUQsO0KXvCi8K6MjjDt8OhSH0='
#
# with open('D:\AllCode\Wenshu_Project\Wenshu\spiders\docid.js') as fp:
#     js = fp.read()
#     js_2 = execjs.compile(js)
#
#
# def decrypt_id(RunEval, id):
#     """
#     docid解密
#     """
#     js = js_2.call("GetJs", RunEval)
#     js_objs = js.split(";;")
#     js1 = js_objs[0] + ';'
#     js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
#     key = js_2.call("EvalKey", js1, js2)
#     key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]
#     docid = js_2.call("DecryptDocID", key, id)
#     return docid

# print(decrypt_id(runeval, casewenshuid))


logging.info('日期: {0}, 案由: {1} 条件下超过200条数据'.format(1, 2))
