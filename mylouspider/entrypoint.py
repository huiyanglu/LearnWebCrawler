#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huiyang Lu
"""
本项目包用于爬取shiyanlou.com网站首页的所有课程信息
属于最基础的scrapy爬虫练习
难点：ASCII格式encoding为utf-8格式
xpath还需要进一步学习
"""
from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'mylouspider'])