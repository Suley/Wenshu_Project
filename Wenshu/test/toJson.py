# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:happy_code
@email: happy_code@foxmail.com
@file:  toJson.py
@time:  2018/11/29
"""
import json
import re

import execjs


class GetDocId(object):

    def __init__(self):
        with open('docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_2 = execjs.compile(jsdata_2)

    def get_docids(self, file):
        f = None
        try:
            f = open(file, 'r', encoding='utf-8')
            line = f.readline()
            while line:
                line = eval(json.loads(line))
                runeval = line[0]['RunEval']
                content = line[1:]
                for i in content:
                    wenshuid = i['文书ID']
                    doc_id = self.decrypt_id(runeval, wenshuid)
                    print(doc_id)
                line = f.readline()
        finally:
            if f:
                f.close()

    def decrypt_id(self, runeval, cid):
        """docid解密"""
        js = self.js_2.call("GetJs", runeval)
        js_objs = js.split(";;")
        js1 = js_objs[0] + ';'
        js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
        key = self.js_2.call("EvalKey", js1, js2)
        key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]
        docid = self.js_2.call("DecryptDocID", key, cid)
        return docid


if __name__ == '__main__':
    s = GetDocId()
    s.get_docids('2001-01-02.txt')
