"""
登录GitHub
通过爬取账号邮箱，检测是否登录成功。
"""
import requests
from bs4 import BeautifulSoup

r1 = requests.get(
    url='https://github.com/login'
)
s1 = BeautifulSoup(r1.text, 'html.parser')
token = s1.find(name='input', attrs={'name': 'authenticity_token'}).get('value')
# 取到token值
r1_cookie_dict = r1.cookies.get_dict()
r2 = requests.post(
    url='https://github.com/session',
    data={
        'commit':'Sign in',
        'utf8':'✓',
        'authenticity_token':token,
        'login':'huiyanglu',
        'password':'87869973lhy'  # 要输入正确的账号密码
    },
    cookies=r1_cookie_dict
)
r2_cookie_dict = r2.cookies.get_dict()

#获取个人信息
r1=requests.get(url='https://github.com/huiyanglu')  #访问登录后页面
jx_1=BeautifulSoup(r1.text,'html.parser')                  #解析当前页面
name=jx_1.find('span',attrs={'itemprop':'name'})         #抓取名字
account=jx_1.find('span',attrs={'itemprop':'additionalName'})  #抓取账号
site=jx_1.find('a',attrs={'rel':'nofollow me'})        #抓取地址
#login=jx_1.find('relative-time')                          #抓取注册时间

r2=requests.get(url='https://github.com/settings/emails',cookies = r2_cookie_dict)  #访问登录后页面
jx_2=BeautifulSoup(r2.text,'html.parser')
email=jx_2.find('span',attrs={'class':'css-truncate-target'})
#打印资料
print('姓名：',name.text)
print('账号：',account.text)
print('地址：',site.text)
print('邮箱',email.text)
#print('注册时间：',login.text)
