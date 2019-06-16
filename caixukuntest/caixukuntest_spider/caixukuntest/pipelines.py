# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# pipelines.py是设置抓取内容存储方式的文件

from pymongo import MongoClient
from scrapy.conf import settings
from pymongo.errors import DuplicateKeyError
from traceback import format_exc


class CaixukuntestPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        _ = spider
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db] #指定数据库
        self.db['repost'].ensure_index('mid', unique=True) #创建索引
        # 定义唯一索引，方法就是指定unique键位true

    def close_spider(self, spider):
        _ = spider
        self.client.close()  # 关闭数据库

    def process_item(self, item, spider):
        try:
            self.db['repost'].update({'mid': item['mid']}, {'$set': item}, upsert=True)
            # 通过mid判断，有就更新，没有就插入

        except DuplicateKeyError:
            spider.logger.debug('duplicate key error collection')  # 唯一键冲突报错
        except Exception as e:
            _ = e
            spider.logger.error(format_exc())
        return item
