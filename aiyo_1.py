"""
小白爬虫第一弹之抓取妹子图
https://cuiqingcai.com/3179.html
1.学会分文件夹批量爬取图片
2.遇到困难：图片链接被拒绝访问
"""

import requests
from bs4 import BeautifulSoup
import os

file = os.getcwd() + '/meitu/'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}  ##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'https://www.mzitu.com/'
start_html = requests.get(all_url,headers=headers)
Soup = BeautifulSoup(start_html.text, 'html.parser')
all_a = Soup.find('div',{'class': 'postlist'}).find_all('a')
for a in all_a:
    title = a.get_text()
    if not title:
        pass
    else:
        path = str(title).strip()
        os.makedirs(os.path.join(file,path))
        os.chdir(file+path)
        href = a['href']
        html = requests.get(href,headers=headers)
        html_Soup = BeautifulSoup(html.text,'html.parser')
        max_span = html_Soup.find('div',{'class': 'pagenavi'}).find_all('span')[-2].get_text()
        for page in range(1,int(max_span)+1):
            page_url = href + '/' + str(page)
            img_html = requests.get(page_url,headers=headers)
            img_Soup = BeautifulSoup(img_html.text,'html.parser')
            img_url = img_Soup.find('div',{'class': 'main-image'}).find('img')['src']
            name = img_url[-9:-4]
            img = requests.get(img_url,headers=headers)
            f = open(name+'.jpg','ab')
            f.write(img.content)
            f.close()

            print(img_url)