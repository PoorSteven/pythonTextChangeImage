# coding:utf-8
import re

#创建日志字典
log_dict = {}

url_dict = {}

url_path_re = {}
#遍历日志文件获取每条日志文件
for line in open('test_web_log'):
    #去除文件中的换行符
    line = line.strip()
    #获取日志中的状态码
    code = line.split(' ')[8]
    url = line.split(' ')[6]
    # print (code)



    #遍历URL链接存放到字典中，并统计数量
    if url_dict.__contains__(url):
        url_dict[url] += 1
    else:
        url_dict[url] = 1


    # print (url)
    #判断日志中百度爬虫的数据存放日志字典中
    if 'Baiduspider' in line:
        #判断百度键值，如果没有创建，如果有则加1
        if log_dict.__contains__('baidu'):
            log_dict['baidu']['总抓取量'] += 1
            #判断百度状态码，如果没有键值创建键值
            if log_dict.__contains__(code):
                log_dict['baidu'][code] += 1
            else:
                log_dict['baidu'][code] = 1
        else:
            log_dict['baidu'] = {'总抓取量':1}

    elif '360Spider' in line:
        #判断百度键值，如果没有创建，如果有则加1
        if log_dict.__contains__('360'):
            log_dict['360']['总抓取量'] += 1
            #判断百度状态码，如果没有键值创建键值
            if log_dict.__contains__(code):
                log_dict['360'][code] += 1
            else:
                log_dict['360'][code] = 1
        else:
            log_dict['360'] = {'总抓取量':1}

    #统计搜狗爬虫的爬取数量
    elif 'Sogou web spider' in line:
        #判断百度爬虫的的键是否存在于spider_dict的字典中
        if log_dict.__contains__('Sogou'):
            log_dict['Sogou']['总抓取量'] += 1
            #判断状态码是否存在字典中
            if log_dict.__contains__(code):
                log_dict['Sogou'][code] += 1
            else:
                log_dict['Sogou'][code] = 1

        else:
            log_dict['Sogou'] = {'总抓取量':1}
    
        #正则替换获取相似URL
    url_re = re.sub(r'd+','ID',url)

    if url_path_re.__contains__(url_re):
        url_path_re[url_re] += 1
    else:
        url_path_re[url_re] = 1
#获取相似类型的页面，按照降序排列
url_same = sorted(url_path_re.items(),key=lambda url_path_re:url_path_re[1],reverse=True)
#遍历相似类型的页面前10种
print ('最多的前10种页面类型》》》》》')
for url_same_path in url_same[:10]:
    
    print (url_same_path)

#获取URL链接按照降序排列
url_dict_max = sorted(url_dict.items(),key=lambda url_dict:url_dict[1],reverse=True)
#遍历抓取页面最大的前10位
print ('抓取页面最多的前10个URL链接》》》》》》')
for url_max in url_dict_max[:10]:
    
    print (url_max)

            
print ('爬虫抓取日志状态》》》》》》》》》')                
print (log_dict)
