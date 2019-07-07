# -*- coding: utf-8 -*-
import scrapy
from SuNingBook.items import SuningbookItem
import re
from copy import deepcopy

class SnBookSpider(scrapy.Spider):
    name = 'sn_book'
    allowed_domains = ['book.suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 解析第一页url地址获取信息
        item = SuningbookItem()
        div_list = response.xpath('//div[@class = "submenu-left"]')
        for div in div_list:
            item['big_type_name'] = div.xpath('./p/a/text()').extract_first()
            item['big_type_url'] = div.xpath('./p/a/@href').extract_first()
            li_list = div.xpath('./ul/li')
            for li in li_list:
                # 文本也需要进行extract_first操作，因为xpath结果为一个列表
                item['book_type_name'] = li.xpath('./a/text()').extract_first()
                item['book_type_url'] = li.xpath('./a/@href').extract_first()
                yield scrapy.Request(
                    item['book_type_url'],
                    callback=self.parse_book,
                    # 由于还有部分信息在详情页，所以要将item以字典格式传入详情页解析方法
                    # 此时多个li列表在同一个item下，为防止数据保存前就发生替换，需deepcopy之后再传item
                    meta={'item': deepcopy(item)},
                    dont_filter="True" # 可能存在过滤已经访问过的url地址情况，可以打开不过滤
                )

    def parse_book(self, response):
        # 解析详情页地址获取信息
        # 传入此方法的meta为response的一个属性
        item = response.meta['item']
        li_list = response.xpath('//ul[@class = "clearfix"]/li')
        for li in li_list:
            # srcapy里xpath得到的列表不是普通列表，而是scrapy特殊定义的所以可以用extract
            item['book_name'] = li.xpath(
                './/img[@class = "search-loading"]/@alt').extract_first()
            item['book_url'] = li.xpath('.//a[@class = '
                                        '"sellPoint"]/@href').extract_first()
            yield item

        # 注意此处获取的文本内容是从访问书本小分类后获得的响应
        page_text = response.xpath(
            '//span[@class="page-more"]/text()').extract_first()
        print('*' * 100)
        page_num = int(re.findall(r'共(\d+)页', page_text)[0])
        print(page_num)
        num = 0
        if num <= page_num:
            next_url = re.sub(r'-0', '-{}'.format(num), item['book_type_url'])
            yield scrapy.Request(
                next_url,
                callback=self.parse_book
            )

