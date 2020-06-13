# coding:utf-8
import requests,re
from bs4 import BeautifulSoup
from lxml import etree
import json
import time
import random
import hashlib

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'UM_distinctid=172a2cd43fe746-08859b4a103804-c373667-1fa400-172a2cd43ffc60; CNZZDATA1278890279=34606622-1591865624-https%253A%252F%252Fwww.baidu.com%252F%7C1591931106',
'Host':'www.zu158.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}
url ='https://www.zu158.com/dongwugushi/'

response = requests.get(url,headers=headers)
html = response.text
soup = BeautifulSoup(html,'lxml')
url_links = re.findall(r'<h1>.*?<strong>.*?<a href="(.*?)" target="_blank" ',html)

print(url_links)

