#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
import scrapy
from mylouspider.items import MylouspiderItem
from scrapy.selector import Selector

class MyLouSpider(scrapy.Spider):
    name = 'mylouspider'
    allowed_domains = ['shiyanlou.com']
    start_urls = ['https://www.shiyanlou.com/courses/?category=all&course_type=all&tag=all&fee=free']

    def parse(self,response):
        content = Selector(response)
        courses = content.xpath('//div[@class="col-md-3 col-sm-6  course"]')
        for each in courses:
            item = MylouspiderItem()
            item['name'] = each.xpath('.//div[@class="course-name"]/text()').extract()[0].strip()
            item['img_url'] = each.xpath('.//div[@class="course-img"]/img/@src').extract()[0].strip()
            item['learned_people'] = each.xpath('.//span[@class="course-per-num pull-left"]/text()').extract()[1].strip()
            yield item
        # yield放在循环里面 每个都yield
        # strip()移除字符串头尾指定的字符
        # scrapy.Spider不要拼错
