 # coding:utf-8

#创建抓取字典
spider_dict = {}

url_dict = {}
#遍历日志文件
for line in open('jk.log'):
    #去除换行符
    line = line.strip()
    #获取每条日志状态码
    code = line.split(' ')[8]
    #获取每条日志爬取的URL
    url = line.split(' ')[6]
    #判断URL字典中是否存在了该链接，有则加1，没有则创建
    if url_dict.__contains__(url):
        url_dict[url] += 1
    else:
        url_dict[url] = 1
    
    #统计百度爬虫的爬取数量
    if 'Baiduspider' in line:
        #判断百度爬虫的的键是否存在于spider_dict的字典中
        if spider_dict.__contains__('baidu'):
            spider_dict['baidu']['总抓取量'] += 1
            #判断状态码是否存在字典中
            if spider_dict.__contains__(code):
                spider_dict['baidu'][code] += 1
            else:
                spider_dict['baidu'][code] = 1

        else:
            spider_dict['baidu'] = {'总抓取量':1}
    #统计360爬虫的爬取数量
    elif '360Spider' in line:
        #判断百度爬虫的的键是否存在于spider_dict的字典中
        if spider_dict.__contains__('360'):
            spider_dict['360']['总抓取量'] += 1
            #判断状态码是否存在字典中
            if spider_dict.__contains__(code):
                spider_dict['360'][code] += 1
            else:
                spider_dict['360'][code] = 1

        else:
            spider_dict['360'] = {'总抓取量':1}
    #统计搜狗爬虫的爬取数量
    elif 'Sogou web spider' in line:
        #判断百度爬虫的的键是否存在于spider_dict的字典中
        if spider_dict.__contains__('Sogou'):
            spider_dict['Sogou']['总抓取量'] += 1
            #判断状态码是否存在字典中
            if spider_dict.__contains__(code):
                spider_dict['Sogou'][code] += 1
            else:
                spider_dict['Sogou'][code] = 1

        else:
            spider_dict['Sogou'] = {'总抓取量':1}


#获取前10名爬虫爬取链接最多的URL
    # url_dict_max = sorted(url_dict.items(),key=lambda url_dict:url_dict[1]: reverse=True)[:10]
print ('日志中爬取最多的页面前10名:')   
url_dict_line = sorted(url_dict.items(),key=lambda url_dict:url_dict[1],reverse=True)[:10]
 #遍历出前10名
for url_dict_max in url_dict_line:
    print (url_dict_max)
print ('爬虫爬取页面数量及状态:')
print (spider_dict)
