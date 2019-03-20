from scrapy.spiders import CrawlSpider,Rule  ##CrawlSpider与Rule配合使用可以骑到历遍全站的作用
from scrapy.linkextractors import LinkExtractor ##配合Rule进行URL规则匹配
from cuiqingcai.items import CuiqingcaiItem

class myspider(CrawlSpider):
    name = 'cuiqingcai'
    allowed_domains = ['cuiqingcai.com']
    start_urls = ['https://cuiqingcai.com/']

    rules = (Rule(LinkExtractor(allow=('\.html',)),callback='parse_item',follow=True),)

    def parse_item(self,response):
        item = CuiqingcaiItem()
        item['url'] = response.url
        item['category'] = response.xpath('//*[@id="mute-category"]/a/text()').extract()[0]
        item['title'] = response.xpath('/html/body/section/div[2]/div/header/h1/a/text()').extract()[0]
        item['imgurl'] = response.xpath('/html/body/section/div[2]/div/article/p/img/@src').extract()
        print(item)
        return item

