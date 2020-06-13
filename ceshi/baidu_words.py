# coding:utf-8
import requests, pymysql
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'BIDUPSID=9F32EE839A028B968AF261C5E22D76A8; PSTM=1588210753; BAIDUID=9F32EE839A028B9609AC9C8FFB2BC475:FG=1; BD_UPN=12314753; ispeed_lsm=2; H_WISE_SIDS=147767_146326_143879_148320_141744_147895_148194_148867_147684_147280_146536_148001_148824_147722_148643_147829_147637_148754_147891_146574_148524_147347_127969_148794_147238_146548_146456_145417_146653_147024_131953_146732_131423_100808_142205_147528_145600_107318_145287_147535_148030_146396_144966_147302_145607_146785_148346_144762_146054_145397_148869_146796_110085; BDUSS=VmZnlNVUJVYjBSOXFpeGtlbWx6OEY1VTRBTUJWcWJvc3FoSm9LYUhYdUZEQVpmSVFBQUFBJCQAAAAAAAAAAAEAAAAH-T800fS54nZpcMXg0bUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIV~3l6Ff95eLW; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a03417051255; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; sug=3; sugstore=1; ORIGIN=0; bdime=0; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=5; H_PS_PSSID=31726_1431_31669_21127_31321_30823; H_PS_645EC=2c7aBLn4mTvas4otBpnZvLoFKfkFpCbeWzcONq9pY0FwmnIygyAsaZG8thg; COOKIE_SESSION=441_0_7_3_4_7_1_0_4_4_4_0_0_0_0_0_1591708755_0_1591715818%7C9%23580968_38_1591513502%7C7; BDSVRTM=373; WWW_ST=1591715827153',
    'Host': 'www.baidu.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}
query = '台门里加盟'
# url = 'https://www.baidu.com/s?wd=%s&ie=utf-8&tn=02049043_52_pg&ssl_s=1&ssl_c=ssl6_172944e2a9e' % query
# 创建轮巡关键词列表
all_words = []
#起始关键词搜索相关关键词，提取加入轮巡关键词列表
def action_one_word(query):
    print('【目前查询的关键词是】》》》：%s' % query)
    response = requests.get('https://www.baidu.com/s?wd=%s&ie=utf-8&tn=02049043_52_pg&ssl_s=1&ssl_c=ssl6_172944e2a9e' % query, headers=headers)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    div = soup.find('div', id='rs')
    for a in div.find_all('a'):
        lunxun_words = a.get_text()
        all_words.append(lunxun_words)
        # return all_words
        print(lunxun_words)

def main(all_words):
    for query in all_words:
        action_one_word(query)


if __name__ == '__main__':
    action_one_word(query)
    main(all_words)


