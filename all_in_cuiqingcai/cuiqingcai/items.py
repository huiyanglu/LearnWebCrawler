# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CuiqingcaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field() #类型
    title = scrapy.Field() #标题
    url = scrapy.Field() #页面地址
    imgurl = scrapy.Field()


