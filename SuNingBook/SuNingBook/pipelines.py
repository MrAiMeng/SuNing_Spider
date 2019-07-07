# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class SuningbookPipeline(object):
    def process_item(self, item, spider):
        # item是类字典格式，非字典
        self.collection.insert_one(dict(item))
        return item

    def open_spider(self,spider):
        self.client = MongoClient()
        self.collection = self.client['SuNing']['book']
    # pymongo不需要断开连接，会自动断开
    def close_spider(self,spider):
        self.client.close()