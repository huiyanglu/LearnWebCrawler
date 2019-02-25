"""
小白爬虫第四弹之爬虫快跑（多进程+多线程）
https://cuiqingcai.com/3363.html
1.使用多进程+多线程修改爬虫代码（from multiprocessing import Pool）
2.连接到MySQL保存信息
3.测试爬取时间
4.问题：多进程函数若放在class中就会出错，因此取消了class的使用
"""

from bs4 import BeautifulSoup
import os
from aiyo_2 import request
import pymysql.cursors
import time
from multiprocessing import Pool

def all_url(url): #获取所有套图的url和title
    start_html = request.get(url,3) #调用
    Soup = BeautifulSoup(start_html.text, 'html.parser')
    all_a = Soup.find('div', {'class': 'postlist'}).find_all('a')[:-5]
    img_all_dict = {}
    for a in all_a:
        title = a.get_text()
        print(title)
        if not title:
            pass
        else:
            img_all_dict[title] = a['href']
    return img_all_dict

def mkdir(path):  # 创建文件夹
    file = '/Users/luhuiyang/PycharmProjects/LearnWebcrawler/meitu/'  # 绝对路径
    path = path.strip()
    isExists = os.path.exists(os.path.join(file, path))
    if not isExists:
        print(u'建了一个名字叫做', path, u'的文件夹！')
        os.makedirs(os.path.join(file, path))  # 新建文件夹
        os.chdir(os.path.join(file, path))  # 切换到当前目录
        return True
    else:
        print(u'名字叫做', path, u'的文件夹已经存在了！')
        return False

def html(title,href): #获取每套图中每张图的地址
    path = str(title)
    mkdir(path)
    html = request.get(href,3)
    html_Soup = BeautifulSoup(html.text, 'html.parser')
    max_span = html_Soup.find('div', {'class': 'pagenavi'}).find_all('span')[-2].get_text()
    page_num = 0
    for page in range(1, int(max_span) + 1):
        page_num += 1
        page_url = href + '/' + str(page)
        # 连接数据库
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='87869973lhy',
            db='mzitu',
            charset='utf8'
        )
        # 获取游标
        cursor = connect.cursor()
        sql = "SELECT url FROM mzitu_1 WHERE url = '%s' "
        data = str(page_url)
        cursor.execute(sql % data)
        if cursor.fetchall():
            print('已爬取过该图片')
        else:
            img(page_url,path)

def img(page_url,path): # 根据每张图的页面地址获取图片的实际地址
    img_html = request.get(page_url,3)
    img_Soup = BeautifulSoup(img_html.text, 'html.parser')
    img_url = img_Soup.find('div', {'class': 'main-image'}).find('img')['src']
    save(img_url,path)
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='87869973lhy',
        db='mzitu',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()
    sql = "INSERT INTO mzitu_1 VALUES ( '%s', '%s', '%s' )"
    data = (str(path), str(page_url), str(img_url))
    cursor.execute(sql % data)
    connect.commit()
    print('成功插入数据')

def save(img_url,path): #根据图片地址保存图片
    name = img_url[-9:-4]
    img = request.get(img_url,3)
    file = '/Users/luhuiyang/PycharmProjects/LearnWebcrawler/meitu/'  # 绝对路径
    os.chdir(os.path.join(file, path))  # 切换到当前目录
    f = open(name + '.jpg', 'ab')
    f.write(img.content)
    #print('已保存%s',name)
    f.close()

if __name__ == '__main__':
    start = time.perf_counter() # 程序运行起始时间
    img_info = all_url('https://www.mzitu.com/') #返回所有图片标题和URL的字典
    pool = Pool(processes=24)
    for key,value in img_info.items():
        pool.apply_async(html, [key,value])
    pool.close()
    pool.join()
    end = time.perf_counter() # 记录程序结束时间
    print('保存结束，花费时间：%f s'%(end-start))

