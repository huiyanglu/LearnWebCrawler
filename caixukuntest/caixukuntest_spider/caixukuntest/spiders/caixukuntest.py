#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
import scrapy
import json
import random
from aiyo_2 import request

class CaixukuntestSpider(scrapy.Spider):
    name = 'caixukuntest'
    allowed_domains = ['m.weibo.cn']

    def start_requests(self):  # 以start_requests代替strat_urls启动爬虫
        urls = ['https://m.weibo.cn/api/statuses/repostTimeline?'
                'id=4362729449834537&page={}'.format(i) for i in range(10000)]  # 该链接通过浏览器抓包得来（微博移动端）
        random.shuffle(urls)  # 这个api的数据是实时更新的，所以不需要按照顺序爬，shuffle一下可以增加爬虫效率

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):  # 解析函数
            res = json.loads(response.text)
            if res['ok'] == 1:
                data = res['data']['data']
                for rep_data in data:
                    del rep_data['text']
                    del rep_data['retweeted_status']
                    del rep_data['visible']
                    del rep_data['number_display_strategy']
                    item = rep_data
                    yield item