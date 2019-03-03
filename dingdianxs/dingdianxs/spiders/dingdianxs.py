import scrapy
from scrapy.http import Request
from dingdianxs.items import DingdianxsItem

class Myspider(scrapy.Spider):
    name = 'dingdianxs'
    allowed_domains = ['23us.us']
    bash_url = 'https://www.23us.us/list/'
    bashurl = '.html'

    def start_requests(self):
        for i in range(1,11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url,self.parse)
        yield Request('https://www.23us.us/quanben/1',self.parse)

    def parse(self, response):
        print(response.text)



