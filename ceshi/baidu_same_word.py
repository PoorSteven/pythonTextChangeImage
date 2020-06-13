# coding:utf-8
import requests,pymysql,re
import datetime,time
from bs4 import BeautifulSoup

#百度关键词相关搜索词挖掘工具

#获取当前时间

def get_now_time():
    a = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return a

#获取代理Ip
def get_http_ip():
    url = 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=efd63e5a9ebc4083ae1f8c24616138ef&count=1&expiryDate=0&format=2&newLine=2'
    html = requests.get(url,timeout=30)
    ip = html.content.strip()
    return bytes.decode(ip)


headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'BIDUPSID=9F32EE839A028B968AF261C5E22D76A8; PSTM=1588210753; BAIDUID=9F32EE839A028B9609AC9C8FFB2BC475:FG=1; BD_UPN=12314753; ispeed_lsm=2; H_WISE_SIDS=147767_146326_143879_148320_141744_147895_148194_148867_147684_147280_146536_148001_148824_147722_148643_147829_147637_148754_147891_146574_148524_147347_127969_148794_147238_146548_146456_145417_146653_147024_131953_146732_131423_100808_142205_147528_145600_107318_145287_147535_148030_146396_144966_147302_145607_146785_148346_144762_146054_145397_148869_146796_110085; BDUSS=VmZnlNVUJVYjBSOXFpeGtlbWx6OEY1VTRBTUJWcWJvc3FoSm9LYUhYdUZEQVpmSVFBQUFBJCQAAAAAAAAAAAEAAAAH-T800fS54nZpcMXg0bUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIV~3l6Ff95eLW; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a03417051255; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; sug=3; sugstore=1; ORIGIN=0; bdime=0; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=5; H_PS_PSSID=31726_1431_31669_21127_31321_30823; H_PS_645EC=2c7aBLn4mTvas4otBpnZvLoFKfkFpCbeWzcONq9pY0FwmnIygyAsaZG8thg; COOKIE_SESSION=441_0_7_3_4_7_1_0_4_4_4_0_0_0_0_0_1591708755_0_1591715818%7C9%23580968_38_1591513502%7C7; BDSVRTM=373; WWW_ST=1591715827153',
'Host':'www.baidu.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}
query = ['老台门']
#连接MySQL数据库
con = pymysql.connect(
    host = '127.0.0.1',
    db = '127.0.0.10',
    user = '127.0.0.10',
    passwd = 'h940834918',
    port = 3306,
    charset = 'utf8'
)
#获取游标
cursor = con.cursor()

#正则匹配模块
req = '老台门|加盟|包子|多少钱|费用|条件|电话|地址|官网|利润|价格|菜单|图片|早餐|餐饮|可靠|多少|'
def search(req,content,n):
    text = re.search(req,content)
    if text:
        data = text.group(n)
    else:
        data = 'no'
    return data
#获取网页响应数据
def get_html(query):
    n = 1
    while n <= 3:
        try:
            proxy_ip = get_http_ip()
            proxies = {
                "http": "http://{ip}".format(ip=proxy_ip),
                "https": "http://{ip}".format(ip=proxy_ip),
            }

            response = requests.get('https://www.baidu.com/s?wd=%s' % query, headers=headers, proxies=proxies)
            content = response.text
            return content
        except:
            print('Request HTTPerror %s' % n)
            n += 1
            continue

def action_baidu_lunxun(keywords):
    # 所有轮巡关键词存放,创建轮巡关键词列表
    all_words = []
    for query in keywords:
        print('【目前查询的关键词相关词】》》》》：%s' % query)
        content = get_html(query)
        soup = BeautifulSoup(content,'html.parser')
        div = soup.find('div',id="rs")
        # print(div)
        for a in div.find_all('a'):
            lunxun_word = a.get_text()
            # print(lunxun_word)
            #判断当前相关词时候匹配
            if search(r'(%s)' % req,lunxun_word,1) == 'no':
                print('>>>>>>【不相关】%s' % lunxun_word)
            else:
                print('>>>>>>%s' % lunxun_word)
                #查询关键词去重
                cursor.execute(" select count(1) from keywords where query='%s'" % lunxun_word)
                result = cursor.fetchone()
                #当前相关搜索词，为处在数据库字段中
                if result[0] == 0:
                    #插入数据库
                    sql = "INSERT INTO keywords (query,lunxun_words,input_date) VALUE ('%s','%s','%s')" % (
                        query,lunxun_word,get_now_time()
                    )
                    try:
                        cursor.execute(sql)
                        con.commit()
                    except:
                        con.rollback()
                        print('>>>>>>INSERT MySQL error')
                    #将当前搜索词传入轮巡关键词列表中
                    all_words.append(lunxun_word)
                else:
                    print('>>>>>>当前关键词已经查询到！')

    action_baidu_lunxun(all_words)

action_baidu_lunxun(query)
