from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mzitu_scrapytest.items import MzituScrapytestItem


class Spider(CrawlSpider):
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/']
    img_urls = []
    rules = (
        Rule(LinkExtractor(allow=('(http|https)://www.mzitu.com/\d{1,6}',), deny=('(http|https)://www.mzitu.com/\d{1,6}/\d{1,6}')), callback='parse_item', follow=True),
    )


    def parse_item(self, response):
        """
        :param response: 下载器返回的response
        :return:
        """
        item = MzituScrapytestItem()
        # max_num为页面最后一张图片的位置
        max_num = response.xpath("descendant::div[@class='main']/div[@class='content']/div[@class='pagenavi']/a[last()-1]/span/text()").extract_first(default="N/A")
        # extract_first(default=”N/A”)的意思是：取xpath返回值的第一个元素。如果xpath没有取到值，则返回N/A
        item['name'] = response.xpath("./*//div[@class='main']/div[1]/h2/text()").extract_first(default="N/A")
        item['url'] = response.url
        for num in range(1, int(max_num)):
            # page_url 为每张图片所在的页面地址
            page_url = response.url + '/' + str(num)
            yield Request(page_url, callback=self.img_url)
        item['image_urls'] = self.img_urls
        yield item

    def img_url(self, response,):
        """取出图片URL 并添加进self.img_urls列表中
        :param response:
        :param img_url 为每张图片的真实地址
        """
        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            print(img_url)
            self.img_urls.append(img_url)
