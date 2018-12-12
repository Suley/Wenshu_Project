# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# 直接存储，一行一行json数据
import os
import re

BASE_PATH = 'Wenshu/answer/'


class WenshuPipeline(object):

    def process_item(self, item, spider):

        date = item['date']

        # 一个年份一个文件夹
        year = date[:4]
        dirpath = BASE_PATH + year + '/'
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        # 一个日期一个文件
        with open(dirpath + date + '.txt', 'a', encoding='utf-8') as f:
            f.write(self.clean_json(item['json_data']) + "\n")

    def clean_json(self, text):
        x = re.search(r'\\"RunEval\\":\\"(.*?)\\"', text)
        x = x.group(1)
        y = re.findall(r'\\".*?ID\\":\\"(.*?)\\"', text)
        sss = x
        for i in y:
            sss += ','
            sss += i
        return sss



# # 1.简单同步存储item
# class WenshuPipeline(object):
#     def __init__(self):
#         host = settings['MONGODB_HOST']
#         port = settings['MONGODB_PORT']
#         dbname = settings['MONGODB_DBNAME']
#         docname = settings['MONGODB_DOCNAME']
#         self.client = pymongo.MongoClient(host=host,port=port)
#         db = self.client[dbname]
#         db[docname].ensure_index('casedocid', unique=True)  # 设置文书ID为唯一索引,避免插入重复数据
#         self.post = db[docname]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         '''插入数据'''
#         try:
#             data = dict(item)
#             self.post.insert_one(data)
#             return item
#         except DuplicateKeyError:
#             # 索引相同,即为重复数据,捕获错误
#             spider.logger.debug('Duplicate key error collection')
#             return item
