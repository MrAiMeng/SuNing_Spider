# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningbookItem(scrapy.Item):
    # define the fields for your item here like:
    big_type_name =  scrapy.Field()
    big_type_url = scrapy.Field()
    book_type_url = scrapy.Field()
    book_type_name = scrapy.Field()
    book_name = scrapy.Field()
    book_url = scrapy.Field()
    book_net_price = scrapy.Field()
    book_ref_price = scrapy.Field()
