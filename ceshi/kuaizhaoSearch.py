# coding:utf-8
import requests,re,pymysql
import datetime,time
from bs4 import BeautifulSoup
'''http://web.archive.org/cdx/search/cdx?url=oa24h.com&output=json&from=2014&to=2016&fl=timestamp,original'''
'''http://web.archive.org/web/20140625131200/http://www.kanzhun.com/'''


#抱头
headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'',
'Host':'web.archive.org',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}

#获取当前时间

def get_now_time():
    a = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return a

#连接MySQL数据库
con = pymysql.connect(
    host = '127.0.0.1',
    db = 'domain',
    user = 'root',
    passwd = 'h940834918',
    port = 3306,
    charset = 'utf8'
)
#获取游标
cursor = con.cursor()


domain_req = 'fuck|sex|prxon|-|girl|boy'

#正则匹配模块
def search(req,content,n):
    text = re.search(req,content)
    if text:
        data = text.group(n)
    else:
        data = 'no'
    return data

def get_archive_html(url):
    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'
    content = response.text
    return content
#导入老域名
for domain in open('domain.txt').readlines()[0:]:
    domain = domain.strip()
    print(domain)
    #查询当前域名是否存在数据库中，如果有则删除
    cursor.execute(" SELECT COUNT(1) FROM one_check WHERE domain_search='%s' " % domain)
    result = cursor.fetchone()
    # print(result)
    if result[0] > 0:
        print('>>>当前域名以存在于Mysql数据库中')
    else:
        if search(r'(%s)' % domain_req, domain, 1) != "no":
            print('>>>命中域名过滤规则，删除域名中')
            v_domain_req = 1
            v_domain_len = 0
            domain_mumber = 0
        elif len(domain) >= 25:
            v_domain_len = 1
            v_domain_req = 0
            domain_mumber = 0
        else:
            # print(domain)
            url = "http://web.archive.org/cdx/search/cdx?url=%s&output=json&from=2014&to=2016&fl=timestamp,original" % domain
            html = get_archive_html(url)
            data_tupe = re.findall(r'"(\d+)", "(http://[^"]*?)"', html)
            print(data_tupe)
            #过滤17年到20年没有建站历史的域名
            if len(data_tupe) == 0:
                print('>>>该域名无快照历史，删除！')
            else:
                #存放每个域名的历史快照url
                archive_links = []
                for line in data_tupe:
                    archive_url = 'http://web.archive.org/web/%s/%s/' % (line[0],line[1])
                    # print(archive_url)

                    archive_links.append(archive_url)
                v_domain_len = 0
                v_domain_req = 0
                domain_mumber = len(archive_links)
                archive_url = "@".join(archive_links)

            #插入数据库

            sql = "INSERT INTO one_check (domain_search,archive_url,imput_date,v_domain_req,v_domain_len,domain_mumber) VALUE ('{domain_search}','{archive_url}','{imput_date}',{v_domain_req},{v_domain_len}, {domain_mumber})".format(domain_search=domain, archive_url=archive_url, imput_date=get_now_time(), v_domain_req=v_domain_req, v_domain_len=v_domain_len, domain_mumber=domain_mumber)
            try:
                cursor.execute(sql)
                con.commit()
                print('>>>数据入库成功！')
            except:
                con.rollback()







