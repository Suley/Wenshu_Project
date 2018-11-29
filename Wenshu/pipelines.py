# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# 直接存储，一行一行json数据
import os


class WenshuPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        # 根据配置中的日期决定文件名
        s_date = crawler.settings['BEGIN_DATE']
        e_date = crawler.settings['END_DATE']
        if s_date == e_date:
            return cls(s_date)
        else:
            return cls(s_date + '_to_' + e_date)

    def __init__(self, filename):
        # 一个年份一个文件夹
        year = filename[:4]
        dirpath = './Wenshu/answer/' + year + '/'

        isexists = os.path.exists(dirpath)
        if not isexists:
            os.makedirs(dirpath)

        filename = dirpath + filename + '.txt'
        self.f = open(file=filename, encoding='utf-8', mode='w')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        self.f.write(item['json_data'] + "\n")


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
