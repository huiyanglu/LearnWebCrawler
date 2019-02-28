import scrapy #导入scrapy包
from scrapy.http import Request ##一个单独的request的模块，需要跟进URL的时候，需要用它
from bs4 import BeautifulSoup
from dingdian.items import DingdianItem


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
            yield Request(url,self.parse) #回调函数

    def parse(self, response):
        max_num = BeautifulSoup(response.text,'lxml').find('div',{'class':'pagelink'}).find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        for num in range(1,int(max_num)+1):
            url = bashurl + '_' + str(num) + self.bashurl
            yield Request(url,callback=self.get_name)
        #print(response.text)

    def get_name(self,response): #获取小说名
        tds = BeautifulSoup(response.text,'lxml').find_all('tr',{'bgcolor':'#FFFFFF'})
        for td in tds: #find_all取出的标签是以列表形式存在的，所以要用循环
            novelname = td.find('a').get_text()
            novelurl = td.find('a')['href']
            yield Request(novelurl,callback=self.get_chapterurl,meta={'name':novelname,'url':novelurl})

    def get_chapterurl(self,response):#获取章节URL
        item = DingdianItem()
        item['name'] = str(response.meta['name']).replace('\xa0','')
        item['novelurl'] = response.meta['url']
        category = BeautifulSoup(response.text,'lxml').find('table').find('a').get_text()
        author = BeautifulSoup(response.text,'lxml').find('table').find_all('td')[1].get_text()
        bash_url = BeautifulSoup(response.text,'lxml').find('p',{'class':'btnlinks'}).find('a',{'class':'read'})['href']
        name_id = str(bash_url)[-6:-1].replace('/','')
        item['category'] = str(category).replace('/','')
        item['author'] = str(author).replace('/','')
        item['name_id'] = name_id
        return item





