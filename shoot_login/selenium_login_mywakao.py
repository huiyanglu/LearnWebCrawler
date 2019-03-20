"""
selenium初学
使用selenium登录哇靠网http://www.mywakao.com/
验证码采用保存人工识别
用户名和密码可事先填好
"""
import os
from PIL import Image
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

url = 'http://www.mywakao.com/login'
driver = webdriver.Chrome()
driver.maximize_window()  # 将浏览器最大化
driver.get(url)

#保存网页获得验证码图片
driver.save_screenshot(os.getcwd()+'/printscreen.png')
im = Image.open('printscreen.png')
im.show()
im.close()
captcha = input('please input the captcha:')

username = input('please input your username: ')
password = input('please input your password: ')

#填写用户名、密码、验证码
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(password)
driver.find_element_by_name('captcha').send_keys(captcha)

#点击登录（通过xpath找到登录按钮)
driver.find_element_by_xpath('//*[@id="submit"]').click()

