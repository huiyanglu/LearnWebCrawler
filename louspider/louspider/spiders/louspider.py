#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
import scrapy
from louspider.items import LouspiderItem
from scrapy.selector import Selector

class LouSpider(scrapy.Spider):
    name = "louspider"
    # 定义允许的域名
    allowed_domains = ["shiyanlou.com"]
    # 定义进行爬取的url列表
    start_urls = ['https://www.shiyanlou.com/courses/?category=all&course_type=all&tag=all&fee=free']

    def parse(self, response):
        hxs = Selector(response)

        courses = hxs.xpath('//div[@class="col-md-3 col-sm-6  course"]')

        for course in courses:
            item = LouspiderItem()
            item['name'] = course.xpath('.//div[@class="course-name"]/text()').extract()[0].strip()
            item['learned'] = course.xpath('.//span[@class="course-per-num pull-left"]/text()').extract()[1].strip()
            item['image'] = course.xpath('.//div[@class="course-img"]/img/@src').extract()[0].strip()
            print(item)
            yield item

