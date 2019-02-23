"""
小白爬虫第三弹之去重去重
https://cuiqingcai.com/3314.html
1.将图片信息存入MySQL
2.当爬虫中断恢复时检测已爬取的内容防止重复
3.运行开始时数据库中无数据（如何在每次运行开始时使DB保持无数据状态，删除原有数据）
"""

from bs4 import BeautifulSoup
import os
from aiyo_2 import request
import pymysql.cursors

class Mzitu():

    def __init__(self):
        # 保存路径
        #self.file = '/Users/luhuiyang/PycharmProjects/LearnWebcrawler/meitu/' #绝对路径
        self.file = os.getcwd() + '/meitu/' #当前路径+文件夹名

        #保存信息
        self.title = ''
        self.url = ''
        self.img_urls = ''

        # 连接数据库
        self.connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='87869973lhy',
            db='mzitu',
            charset='utf8'
        )
        # 获取游标
        self.cursor = self.connect.cursor()

    def all_url(self,url):
        start_html = request.get(url,3) #调用
        Soup = BeautifulSoup(start_html.text, 'html.parser')
        all_a = Soup.find('div', {'class': 'postlist'}).find_all('a')
        for a in all_a:
            title = a.get_text()
            self.title = title #标题保存
            if not title:
                pass
            else:
                path = str(title)
                self.mkdir(path)
                href = a['href']
                self.html(href)

    def html(self,href): #获取每套图中每张图的地址
        html = request.get(href,3)
        html_Soup = BeautifulSoup(html.text, 'html.parser')
        max_span = html_Soup.find('div', {'class': 'pagenavi'}).find_all('span')[-2].get_text()
        page_num = 0
        for page in range(1, int(max_span) + 1):
            page_num += 1
            page_url = href + '/' + str(page)
            self.url = page_url

            sql = "SELECT url FROM mzitu_1 WHERE url = '%s' "
            data = str(page_url)
            self.cursor.execute(sql % data)
            if self.cursor.fetchall():
                print('已爬取过该图片')
            else:
                self.img(page_url,max_span,page_num)

    def img(self,page_url,max_span,page_num): # 根据每张图的页面地址获取图片的实际地址
        img_html = request.get(page_url,3)
        img_Soup = BeautifulSoup(img_html.text, 'html.parser')
        img_url = img_Soup.find('div', {'class': 'main-image'}).find('img')['src']
        self.img_urls = img_url
        print(str(self.title),str(self.url),str(self.img_urls))
        #if int(max_span)==page_num:
        self.save(img_url)

        sql = "INSERT INTO mzitu_1 VALUES ( '%s', '%s', '%s' )"
        data = (str(self.title),str(self.url),str(self.img_urls))
        self.cursor.execute(sql % data)
        self.connect.commit()
        print('成功插入数据')

    def mkdir(self,path): # 创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join(self.file,path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join(self.file,path)) # 新建文件夹
            os.chdir(os.path.join(self.file, path)) # 切换到当前目录
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def save(self,img_url): #根据图片地址保存图片
        name = img_url[-9:-4]
        img = request.get(img_url,3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

Mzitu = Mzitu() #实例化
Mzitu.all_url('https://www.mzitu.com/') #给函数all_url传入参数，作为启动爬虫的入口

