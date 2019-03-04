import scrapy
import re
from scrapy.http import Request
from dingdianxs.items import DingdianxsItem,DcontentItem
from bs4 import BeautifulSoup
from dingdianxs.mysqlpipelines.sql import Sql


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
        max_num = BeautifulSoup(response.text,'lxml').find('div',{'class':'pagelink'}).find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        for num in range(1,int(max_num)+1):
            url = bashurl + '_' + str(num) + self.bashurl
            yield Request(url,callback=self.get_name)

    def get_name(self,response):
        tds = BeautifulSoup(response.text,'lxml').find_all('tr',{'bgcolor':'#FFFFFF'})
        for td in tds:
            novelname = td.find('a').get_text()
            novelurl = td.find('a')['href']
            yield Request(novelurl,callback=self.get_chapterurl,meta={'name':novelname,'url':novelurl})

    def get_chapterurl(self, response):  # 获取章节URL
        item = DingdianxsItem()
        item['name'] = str(response.meta['name']).replace('\xa0', '')
        item['novelurl'] = response.meta['url']
        category = BeautifulSoup(response.text, 'lxml').find('table').find('a').get_text()
        author = BeautifulSoup(response.text, 'lxml').find('table').find_all('td')[1].get_text()
        bash_url = \
        BeautifulSoup(response.text, 'lxml').find('p', {'class': 'btnlinks'}).find('a', {'class': 'read'})['href']
        name_id = str(bash_url)[-6:-1].replace('/', '')
        item['category'] = str(category).replace('/', '')
        item['author'] = str(author).replace('\xa0', '')
        item['name_id'] = name_id
        yield item
        yield Request(url=bash_url,callback=self.get_chapter,meta={'name_id':name_id})

    def get_chapter(self,response):
        urls = re.findall(r'<td class="L"><a href="(.*?)">(.*?)</a></td>',response.text)
        num = 0
        for url in urls:
            num+=1
            chapterurl = url[0]
            chaptername = url[1]
            rets = Sql.select_chapter(chapterurl)
            if rets[0] == 1:
                print('章节已经存在了')
            else:
                yield Request(chapterurl,callback=self.get_chaptercontent,meta={'num':num,
                                                                            'name_id':response.meta['name_id'],
                                                                            'chaptername':chaptername,
                                                                            'chapterurl':chapterurl
                                                                            })

    def get_chaptercontent(self,response):
        item2 = DcontentItem()
        item2['num'] = response.meta['num']
        item2['id_name'] = response.meta['name_id']
        item2['chaptername'] = str(response.meta['chaptername']).replace('\xa0','')
        item2['chapterurl'] = response.meta['chapterurl']
        content = BeautifulSoup(response.text,'lxml').find('dd', {'id': 'contents'}).get_text()
        item2['chaptercontent'] = str(content).replace('\xa0','')
        return item2



