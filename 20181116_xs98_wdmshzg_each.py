# 爬取小说《我的秘书会捉鬼》
# 网站：https://www.xs98.com/xs201429/
# charset = utf-8
# 每个章节生成一个txt文件

import requests
import os
import time
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

# 获取小说各个章节的名字和url
def getChapterInfo(novel_url):
    chapter_html = requests.get(novel_url, headers=headers)
    chapter_html.encoding ='utf-8'
    soup = BeautifulSoup(chapter_html.text,'html.parser')
    soup2 = soup.find('div',{'id':'list'})
    chapter_list = soup2.find_all('dd') # 先找到'li'
    chapter_all_dict = {}
    for each in chapter_list:
        import re
        chapter_each = {}
        chapter_each['title'] = each.find('a').get_text()
        chapter_each['chapter_url'] = 'https://www.xs98.com/xs201429/'+each.find('a')['href']
        chapter_num = int(re.findall('\d+',each.get_text())[0])
        chapter_all_dict[chapter_num] = chapter_each # 记录到所有的章节的字典中保存，返回字典
    return chapter_all_dict

# 获取小说章节内容，写入文本
def getChapterContent(each_chapter_dict):
    content_html = requests.get(each_chapter_dict['chapter_url'],headers=headers)
    content_html.encoding ='utf-8'
    soup = BeautifulSoup(content_html.text,'html.parser')
    content_tag = soup.find_all('div',{'id':'content'})
    content_tag = str(content_tag[0])
    content_tag = content_tag.replace('<br/>', '\n') #<br/>替换为换行符
    #content_tag = content_tag.strip()
    #p_tag = content_tag.find_all('')
    print('正在保存的章节-->'+ each_chapter_dict['title'])
    match = re.compile('<(.*)>') #删掉所有< >
    taglist = match.findall(content_tag)
    for tag in taglist:
        tag = '<' + tag + '>'
        content_tag = content_tag.replace(tag, '')
    #content_tag = content_tag.replace('\n', '')
    with open(each_chapter_dict['title'] + r'.txt', 'a', encoding='utf8')as f:
        f.write('' + content_tag + '\n\n')
        f.close()

if __name__ == '__main__':
    start = time.clock() # 程序运行起始时间
    novel_url = 'https://www.xs98.com/xs201429/'
    novel_info = getChapterInfo(novel_url)
    dir_name = '我的秘书会捉鬼'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)
    for each in novel_info:
        getChapterContent(novel_info[each])
    end = time.clock() # 记录程序结束时间
    print('保存结束，共保存 %d 章，花费时间：%f s'%(len(novel_info),(end-start)))
