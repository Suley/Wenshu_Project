# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# 1.简单同步存储item
class WenshuPipeline(object):
    def process_item(self, item, spider):
        return item


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
