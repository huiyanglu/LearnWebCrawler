"""
爬取网站http://www.89ip.cn/的IP地址，生成列表形式
"""
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
def ans(url):
    content_html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(content_html, 'html.parser')
    content_tag = soup.find('table', {'class': 'layui-table'})
    p_tag = content_tag.find_all('tr')
    chapter_all_dict = []
    for each in p_tag[1:]:
        chapter_each = each.get_text().split()[0]+':'+each.get_text().split()[1]
        chapter_all_dict.append(chapter_each)
    return chapter_all_dict

url = 'http://www.89ip.cn/'
print(ans(url))