import scrapy #导入scrapy包
from scrapy.http import Request ##一个单独的request的模块，需要跟进URL的时候，需要用它


class Myspider(scrapy.Spider): #这个类继承自scrapy.Spider

    # name就是我们在entrypoint.py文件中的第三个参数！
    # 此Name的！名字！在整个项目中有且只能有一个、名字不可重复！
    name = 'dingdian'
    allowed_domains = ['x23us.com']
    bash_url = 'https://www.x23us.com/class/'
    bashurl = '.html'

    def start_requests(self):
        for i in range(1,11):
            url = self.bash_url + str(i) +'_1' + self.bashurl
            yield Request('https://www.x23us.com/quanben/1',self.parse) #回调函数

    def parse(self, response):
        print(response.text)


