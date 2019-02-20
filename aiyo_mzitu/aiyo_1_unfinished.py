"""
小白爬虫第一弹之抓取妹子图
https://cuiqingcai.com/3179.html
1.学会分文件夹批量爬取图片
2.遇到困难：图片链接被拒绝访问
"""

import requests
from bs4 import BeautifulSoup
import os
import urllib.request

# 保存路径
file = os.getcwd() + '/meitu/'

# 网站headers（包含referer破解盗链）
Hostreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://www.mzitu.com'
               }

# 图片链接的headers（包含referer破解盗链）
Picreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://i.meizitu.net'
              }

all_url = 'https://www.mzitu.com/'
start_html = requests.get(all_url,headers=Hostreferer)
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
        html = requests.get(href,headers=Hostreferer)
        html_Soup = BeautifulSoup(html.text,'html.parser')
        max_span = html_Soup.find('div',{'class': 'pagenavi'}).find_all('span')[-2].get_text()
        for page in range(1,int(max_span)+1):
            page_url = href + '/' + str(page)
            img_html = requests.get(page_url,headers=Hostreferer)
            img_Soup = BeautifulSoup(img_html.text,'html.parser')
            img_url = img_Soup.find('div',{'class': 'main-image'}).find('img')['src']
            name = img_url[-9:-4]
            img = requests.get(img_url,headers=Picreferer)
            f = open(name+'.jpg','ab')
            f.write(img.content)
            f.close()

            print(img_url)