"""
静觅爬虫教程之小白爬虫第二弹
https://cuiqingcai.com/3256.html
1. headers随机
2. 代理IP
3.headers加referer破解防盗链
"""
import requests
import random
from bs4 import BeautifulSoup
import time

class download:
    def __init__(self):
        self.iplist = [] # 初始化一个list用来存放我们获取到的IP
        html = requests.get('http://www.89ip.cn/').text
        soup = BeautifulSoup(html, 'html.parser')
        content_tag = soup.find('table', {'class': 'layui-table'})
        p_tag = content_tag.find_all('tr')
        for each in p_tag[1:]:
            chapter_each = each.get_text().split()[0] + ':' + each.get_text().split()[1]
            self.iplist.append(chapter_each) # IP列表

        self.user_agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
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

    def get(self,url,timeout,proxy=None,num_retries=6): # 给函数一个默认参数proxy为空
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': UA ,'referer':url} # 随机选headers,加referer破解防盗链

        if proxy == None: #当代理为空时，不使用代理获取response
            try:
                return requests.get(url,headers = headers,timeout=timeout)
            except:
                if num_retries > 0: # 限定的重试次数
                    time.sleep(10) # 延迟10秒
                    print(u'获取网页出错，10秒后将获取倒数第：',num_retries,u'次')
                    return self.get(url,timeout,num_retries-1) # 调用自身，次数-1
                else: # 重试6次失败后使用代理IP
                    print('开始使用代理')
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http':IP}
                    return self.get(url,timeout,proxy,)
        else: # 当代理不为空时
            try:
                IP = ''.join(str(random.choice(self.iplist)).strip())
                proxy = {'http':IP} # 构造成一个代理
                return requests.get(url,headers=headers,proxies = proxy,timeout=timeout)
            except:
                if num_retries > 0:
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    print(u'正在更换代理，10秒后重新获取倒数第：',num_retries,u'次')
                    print(u'当前代理是：',proxy)
                    return self.get(url,timeout,proxy,num_retries-1)
                else:
                    print(u'代理也不好使了！取消代理')
                    return self.get(url,3)

request = download() #不需要新建init文件，直接调用request实例

