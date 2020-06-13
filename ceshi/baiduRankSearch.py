# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
import lxml
#请求抱头

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'',
'Host':'www.baidu.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}
url = 'https://www.baidu.com/s?wd=description'
response = requests.get(url,headers=headers).text
soup = BeautifulSoup(response,'lxml')
#提取单个div网站内容,遍历出来
for line in soup.find_all("div",class_='c-container'):
    title = line.h3.get_text().strip()
    #描述异常处理
    try:
        description = line.find("div", class_="c-abstract").get_text().strip()
    except:
        description = '特性展示，百度系产品'
    #异常处理域名地址
    try:
        domain = line.find("a",class_="c-showurl").get_text().strip()
        domain = re.sub(r".nor-src-[\s\S]*?}","",domain).strip()
    except:
        domain = line.find("span",class_="c-showurl").get_text().strip()
    rank = line['id']

    print(rank,title,description,domain)
    print('\n')
