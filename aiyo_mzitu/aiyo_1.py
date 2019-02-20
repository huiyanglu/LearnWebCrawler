"""
小白爬虫第一弹之抓取妹子图
https://cuiqingcai.com/3179.html
1.学会分文件夹批量爬取图片
2.遇到困难：图片链接被拒绝访问。通过更改headers的referer破解防盗链
3.导入download文件可获取随机headers和代理IP
4.区分绝对路径和相对路径
"""

from bs4 import BeautifulSoup
import os
from aiyo_2 import request

class Mzitu():

    def __init__(self):
        # 保存路径
        #self.file = '/Users/luhuiyang/PycharmProjects/LearnWebcrawler/meitu/' #绝对路径
        self.file = os.getcwd() + '/meitu/' #当前路径+文件夹名

    def all_url(self,url):
        start_html = request.get(url,3) #调用
        Soup = BeautifulSoup(start_html.text, 'html.parser')
        all_a = Soup.find('div', {'class': 'postlist'}).find_all('a')
        for a in all_a:
            title = a.get_text()
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
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)

    def img(self,page_url): # 根据每张图的页面地址获取图片的实际地址
        img_html = request.get(page_url,3)
        img_Soup = BeautifulSoup(img_html.text, 'html.parser')
        img_url = img_Soup.find('div', {'class': 'main-image'}).find('img')['src']
        self.save(img_url)

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

