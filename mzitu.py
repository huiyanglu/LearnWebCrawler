from bs4 import BeautifulSoup
import os
from Download import download
import time
import requests


class mzitu(download):
    file = os.getcwd() + 'meitu/'
    def all_url(self, url):
        html = download.get(self, url, 3)  ##这儿替换了，并加上timeout参数
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a[1:]:
            title = a.get_text()
            print(u'开始保存：', title)
            path = str(title).replace("?", '_')
            self.mkdir(path)
            os.chdir(self.file + path)
            href = a['href']
            self.html(href)

    def html(self, href):
        html = download.get(self, href, 3)
        max_span = BeautifulSoup(html.text, 'lxml').find_all('span')[10].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.img(page_url)

    def img(self, page_url):
        img_html = download.get(self, page_url, 3)  ##这儿替换了
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):
        name = img_url[-9:-4]
        print(u'开始保存：', img_url)
        img = download.get(self, img_url, 3)  ##这儿替换了，并加上timeout参数
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join(self.file, path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join(self.file, path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False


Mzitu = mzitu()  ##实例化
Mzitu.all_url('http://www.mzitu.com/all')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）