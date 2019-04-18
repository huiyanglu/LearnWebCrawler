# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MylouspiderPipeline(object):
    def process_item(self, item, spider):
        with open('courses.txt','a',encoding='utf-8') as file:
            line = u'course name:{0},learned_people:{1},img_url:{2}\n'.format(
                item['name'],item['learned_people'],item['img_url'])
            file.write(line)
        return item

# 报错'ascii' codec can't encode characters in position
# 爬取的内容无法保存
# 在pipeline文件中加入encoding='utf-8'即可解决