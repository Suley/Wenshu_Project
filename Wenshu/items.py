# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 需要案件详情
class WenshuCaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    casecourt = scrapy.Field()
    casecontent = scrapy.Field()
    casetype = scrapy.Field()
    casereason = scrapy.Field()
    casejudgedate = scrapy.Field()
    caseparty = scrapy.Field()
    caseprocedure = scrapy.Field()
    casenumber = scrapy.Field()
    casenopublicreason = scrapy.Field()
    casedocid = scrapy.Field()
    casename = scrapy.Field()
    casecontenttype = scrapy.Field()
    caseuploaddate = scrapy.Field()
    casedoctype = scrapy.Field()
    caseclosemethod = scrapy.Field()
    caseeffectivelevel = scrapy.Field()


# 只要docid和裁判日期
class WenshuDocidItem(scrapy.Item):
    docid = scrapy.Field()
    judgedate = scrapy.Field()


# 只要json数据
class WenshuJsonItem(scrapy.Item):
    # 要解密的json数据
    json_data = scrapy.Field()
    date = scrapy.Field()
