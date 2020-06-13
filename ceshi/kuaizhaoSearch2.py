# coding:utf-8
import requests,re,pymysql
from bs4 import BeautifulSoup
from aip import AipImageCensor
import datetime,time

#百度AI接口 文字敏感词审核
""" 百度 APPID AK SK """
APP_ID = '20390375'
API_KEY = 'lZXLHBSBV5K0foFk4VxItVjN'
SECRET_KEY = 'NF4mgzgGfgepetMk1uo7K6RusqB5YoRv'

client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)

def get_content_spam(text):
    try:
        # result = client.antiSpam(text)
        result = client.textCensorUserDefined(text)
        return result['conclusion']
    except:
        return result

# a = get_content_spam('空包网，空包代理，空包加盟！')
# b = get_content_spam('为趣闻的百科小知识，你想要了解的都在这里')
# print(a)
#获取当前时间
def get_now_time():
    a = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return a
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

content_req = '牛彩|二八杠|人体|永久|德州|扑克|三级|AG8|足球|亚洲|亚游|香蕉|丁香|盘口|万博|秀场|飞艇|银河|走势|赌|赛车|pk10|老虎机|黄色|开户|博彩|妹妹|澳门|赌博|彩票|皇冠|娱乐|葡京|牛牛|现金|金沙|百胜|太阳城|时时彩|蛋蛋|麻将|棋牌|亚洲|开奖|被|漏|捅|穴|淫|鸭|鸡|鸟|鲍|骚|鞭|阴|逼|h|裸|蒲|蛋|荡|色|茎|脱|精液|禁|艹|潮|暴|插|慰|性|情|屌|嫖|娼|啪|勃|乳'

title_req = '牛彩|二八杠|人体|永久|德州|扑克|三级|AG8|足球|亚洲|亚游|香蕉|丁香|盘口|万博|秀场|飞艇|银河|走势|赌|赛车|pk10|老虎机|黄色|开户|博彩|妹妹|澳门|赌博|彩票|皇冠|娱乐|葡京|牛牛|现金|金沙|百胜|太阳城|时时彩|蛋蛋|麻将|棋牌|亚洲|开奖|被|漏|捅|穴|淫|鸭|鸡|鸟|鲍|骚|鞭|阴|逼|h|裸|蒲|蛋|荡|色|茎|脱|精液|禁|艹|潮|暴|插|慰|性|情|屌|嫖|娼|啪|勃|乳|申博|百家乐|老牌|搜博网|凯时|真钱|娱乐|平台'

#正则匹配模块
def search(req,content,n):
    text = re.search(req,content)
    if text:
        data = text.group(n)
    else:
        data = 'no'
    return data


#判断字符串是否包含中文
def check_contain_chinses(check_str):
    chinses_code = 0
    for  ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff' :
            chinses_code = 1
        return chinses_code

#查看当前文件中，是否包含某文件
import os
def get_include_file(filename):
    a = os.path.exists(filename)
    return a

if get_include_file('archive_url'):
    # print('>>>文件已存在')
    pass
else:
    #将one_check读取的文件，存放到archive——url中
    archive_file = open('archive_url','w')
    cursor.execute(" select domain_search, archive_url from one_check where v_domain_req = 0 and v_domain_len = 0")
    result = cursor.fetchall()
    for row in result:
        domain = row[0]
        archive_urls = row[1]
        archive_file.write('%s|%s\n' % (domain,archive_urls))
    archive_file.close()

def get_archive_html(url):
    response = requests.get(url,headers=headers)
    # response.encoding = 'utf-8'
    #自动判断字符集类型
    response.encoding = response.apparent_encoding
    content = response.text
    return content
#拆分域名和快照

def action_main(line):
    line = line.strip()
    domain_url = line.split('|')[0]
    archive_urls = line.split('|')[1]
    for archive_url in archive_urls.split('@'):
        html = get_archive_html(archive_url)
        soup = BeautifulSoup(html,'html.parser')
        #判断title中是否有违禁词
        # title = search(r'<title>(.*?)</title>',html,1)
        try:
            title = soup.title.get_text()
            title_status = 0
        except:
            title_status = 1
            print('>>>网页快照可能存在301跳转')
        if title_status == 1:
            continue
        else:
            title_weijin_word = search(r'(%s)' % title_req, title, 1)
            if title_weijin_word == 'no':
                title_weijin_word = ''
                v_title_weijin = 0

                #title继续进入百度AI 进行审查是否违禁
                v_baidu_ai = get_content_spam(title)


            else:
                v_title_weijin = 1
                v_baidu_ai = '不合规'
            # print(title, v_baidu_ai)
            #判断如果title命中规则，则不再检索余下的项目，直接返回快照不合格
            if v_title_weijin == 0:

                #判断title是否命中不包含中文
                if check_contain_chinses(title) == 0:
                    v_chinese = 1 #命中title不含包中文规则
                    v_archive_status = 1
                    v_content_weijin = 1
                    content_weijin_word = ''
                else:
                    v_chinese = 0

                    # #检测正文中是否存在违禁关键词
                    # content_weijin_word = search(r'(%s)' % content_req,html,1)
                    # if content_weijin_word == 'no':
                    #     #正文命中敏感词
                    #     v_content_weijin = 0
                    #     content_weijin_word = 0
                    # else:
                    #     v_content_weijin = 1


            else:
                v_content_weijin = 1
                content_weijin_word = ''
                v_chinese = 0
                v_archive_status = 1

        '''
        1、如果命中正文违禁，或者百度返回值为：疑似 ，则进入人工审核状态
        2、命中title违禁，title非中文，百度ai返回值为不合格，则，不合格
        3、所有规则都正常，则合格
        '''
        # if v_title_weijin == 1 or v_baidu_ai == "疑似" :
        #     v_archive_status = 2
        # elif  v_content_weijin== 1 or v_baidu_ai == '不合规':
        #     v_archive_status = 1
        # elif v_title_weijin == 0 or v_baidu_ai == "合规" or v_chinese == 0:
        #     v_archive_status = 0
        if v_title_weijin == 1:
            v_archive_status = 1
        elif v_chinese == 1:
            v_archive_status == 1
        elif v_baidu_ai == '不合规':
            v_archive_status == 1
        else:
            v_archive_status ==0

        # print(title,v_archive_status,v_baidu_ai)
            # print(title,v_chinese,v_title_weijin,title_weijin_word)
        # 插入数据库
        sql = "UPDATE table_name SET column1_name,column2_name2 WHERE some_column = some_name"
        sql = "INSERT INTO two_check (domain_url,archive_url,v_title_weijin,title_weijin_word,v_chinese,input_date,v_archive_status,v_baidu_ai) VALUE ('{domain_url}','{archive_url}',{v_title_weijin},'{title_weijin_word}',{v_chinese},'{input_date}',{v_archive_status},'{v_baidu_ai}')".format(domain_url=domain_url,archive_url=archive_url,v_title_weijin=v_title_weijin,title_weijin_word=title_weijin_word,v_chinese=v_chinese,input_date=get_now_time(),v_archive_status=v_archive_status,v_baidu_ai=v_baidu_ai)
        try:
            cursor.execute(sql)
            con.commit()
            print('>>>>数据入库成功')
        except:
            con.rollback()
            print('>>>error!!!!!')

#多线程运行
import multiprocessing

if __name__=='__main__':
    r = open('archive_url').readlines()[5:]
    pool = multiprocessing.Pool(processes=2)
    for url in r:
        url = url.strip()
        pool.apply_async(action_main,(url,))
        pool.close()
        pool.join()