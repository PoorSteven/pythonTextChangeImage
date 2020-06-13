# coding:utf-8
import re
import json
import requests
from requests.exceptions import RequestException
from multiprocessing import Pool

#获取猫眼页面响应数据
def get_one_page(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
#正则匹配
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?class="name"><a href="(.*?)".*?data-val=".*?">(.*?)</a>.*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?class="integer">(.*?)</i>.*?class="fraction">(.*?)</i>.*?</dd>',re.S)

    items = re.findall(pattern,html)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'url':'https://maoyan.com'+item[2],
            'title':item[3],
            'actor':item[4].strip()[3:],
            'time':item[5].strip()[5:],
            'score':item[6]+item[7]
         }
#写入文件
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()
#执行文件
def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

#遍历top100
if __name__ == "__main__":
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
