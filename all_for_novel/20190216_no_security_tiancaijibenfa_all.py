# coding: utf-8
#  爬取小说《天才基本法》，作者：长洱
# 网站：https://www.fpzw.com/xiaoshuo/106/106431/
# charset = utf-8
# 所有章节放在同一个TXT文件中

import requests
import os
import time
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

# 获取小说各个章节的名字和url
def getChapterInfo(novel_url):
    chapter_html = requests.get(novel_url, headers=headers)
    chapter_html.encoding='gbk'
    chapter_html2 = chapter_html.text
    soup = BeautifulSoup(chapter_html2,'html.parser')
    soup2 = soup.find_all({'dd'})
    chapter_list = soup2[4:] #排除前面无用的
    chapter_all_dict = {}
    for each in chapter_list:
        import re
        chapter_each = {}
        chapter_each['title'] = each.find('a').get_text()
        chapter_each['chapter_url'] = 'https://www.fpzw.com/xiaoshuo/106/106431/'+each.find('a')['href']
        chapter_num = int(re.findall('\d+',each.get_text())[0])
        chapter_all_dict[chapter_num] = chapter_each # 记录到所有的章节的字典中保存，返回字典
    print(chapter_all_dict)
    return chapter_all_dict

# 获取小说章节内容，写入文本
def getChapterContent(each_chapter_dict):
    content_html = requests.get(each_chapter_dict['chapter_url'],headers=headers)
    content_html.encoding='gbk' #gbk解码
    content_html2 = content_html.text #先解码再转text
    new_html = (content_html2.replace('<br />','<a>'))
    soup = BeautifulSoup(new_html,'html.parser')
    content_tag = soup.find('p',{'class':'Text'})
    p_tag = content_tag.find_all('a')[15].get_text().replace('<a>',''+'\n') #<a>变成空格
    print('正在保存的章节-->'+ each_chapter_dict['title'])
    p_tag2 = [each_chapter_dict['title']]+p_tag.split()[:-1] #以空格分割，加每章标题，去掉结尾广告
    for each in p_tag2:
        paragraph = '\n'+each.strip()# 去掉首尾字符
        with open(r'天才基本法全文.txt','a',encoding = 'utf8')as f:
            f.write(''+ paragraph + '\n')
            f.close()

if __name__ == '__main__':
    start = time.clock() # 程序运行起始时间
    novel_url = 'https://www.fpzw.com/xiaoshuo/106/106431/'
    novel_info = getChapterInfo(novel_url)
    dir_name = '天才基本法'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)
    for each in novel_info:
        getChapterContent(novel_info[each])
    end = time.clock() # 记录程序结束时间
    print('保存结束，共保存 %d 章，花费时间：%f s'%(len(novel_info),(end-start)))
