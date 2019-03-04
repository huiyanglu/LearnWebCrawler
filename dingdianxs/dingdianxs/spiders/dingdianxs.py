import scrapy
import re
from scrapy.http import Request
from dingdianxs.items import DingdianxsItem,DcontentItem
from bs4 import BeautifulSoup
from dingdianxs.mysqlpipelines.sql import Sql
import random
import requests

class Myspider(scrapy.Spider):
    name = 'dingdianxs'
    allowed_domains = ['23us.us']
    bash_url = 'https://www.23us.us/list/'
    bashurl = '.html'

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

    UA = random.choice(user_agent_list)
    headers = {'User-Agent': UA, 'referer': 'https://www.23us.us/'}  # 随机选headers,加referer破解防盗链

    def get_ip(self):
        iplist = []  # 初始化一个list用来存放我们获取到的IP
        html = requests.get('http://www.89ip.cn/').text
        soup = BeautifulSoup(html, 'html.parser')
        content_tag = soup.find('table', {'class': 'layui-table'})
        p_tag = content_tag.find_all('tr')
        for each in p_tag[1:]:
            chapter_each = each.get_text().split()[0] + ':' + each.get_text().split()[1]
            iplist.append(chapter_each)  # IP列表
        IP = ''.join(str(random.choice(iplist)).strip())
        print(IP)
        return IP

    def start_requests(self):
        for i in range(1,11):
            url = self.bash_url + str(i) + '_1' + self.bashurl
            yield Request(url,headers=self.headers,callback=self.parse,meta={'proxy':str(self.get_ip())})
        yield Request('https://www.23us.us/quanben/1',headers=self.headers,callback=self.parse,meta={'proxy':str(self.get_ip())})

    def parse(self, response):
        max_num = BeautifulSoup(response.text,'lxml').find('div',{'class':'pagelink'}).find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        for num in range(1,int(max_num)+1):
            url = bashurl + '_' + str(num) + self.bashurl
            yield Request(url,headers=self.headers,callback=self.get_name)

    def get_name(self,response):
        tds = BeautifulSoup(response.text,'lxml').find_all('tr',{'bgcolor':'#FFFFFF'})
        for td in tds:
            novelname = td.find('a').get_text()
            novelurl = td.find('a')['href']
            yield Request(novelurl,headers=self.headers,callback=self.get_chapterurl,meta={'name':novelname,'url':novelurl})

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
        yield Request(url=bash_url,headers=self.headers,callback=self.get_chapter,meta={'name_id':name_id})

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
                yield Request(chapterurl,headers=self.headers,callback=self.get_chaptercontent,meta={'num':num,
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



