# coding:utf-8
import requests
import re
import json
from requests.exceptions import RequestException

def get_one_page():
    url = 'https://www.ixigua.com/home/67773411283/video/?preActiveKey=home'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('获取错误！')

def main():
    get_one_page()

if __name__ == '__main__':
    main()

#获取代理Ip
def get_http_ip():
    url = 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=efd63e5a9ebc4083ae1f8c24616138ef&count=1&expiryDate=0&format=2&newLine=2'
    html = requests.get(url,timeout=30)
    ip = html.content.strip()
    return bytes.decode(ip)

proxy_ip = get_http_ip()
proxies = {
    "http":"http://{ip}".format(ip=proxy_ip),
    "https":"https://{ip}".format(ip=proxy_ip),
}