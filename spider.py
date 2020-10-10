# -*- coding = utf-8 -*-
# @Time:2020/06/27 11:28
# @Author: w
# @File:spider.py
# @Software:PyCharm
import time

import bs4
import re
import xlwt
import urllib.request, urllib.error
import sqlite3
import logging
import random
import requests
import pymysql

logging.basicConfig(
    level=logging.INFO,
    filename='out.log',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def get_log():
    logger.info('This is a log info')
    logger.debug('Debugging')
    logger.warning('Warning exists')
    logger.error('This is a error')
    logger.info('Finish')


def main():
    # 爬取网页
    # 解析数据
    # 保存数据
    base_url = "https://movie.douban.com/top250?start={j}&filter="
    datalist = getData(base_url)
    # savepath = ".\\豆瓣电影Top250_02.xls"
    dbpath = "movietest.db"
    saveData2DB(datalist, dbpath)  # 将数据存储到movietest.db中
    # saveData(datalist, savepath)    # 将数据保存到表格中

    # askURL(base_url)


# 影片链接
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示字符串的模式
# 影片图片
findImage = re.compile(r'<img .* src="(.*?)"', re.S)
# 影片片名
findTitle = re.compile(r'<span class="title">(.*?)</span>')
# 影片的评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 评价人数
findJudge = re.compile(r'<span>(.*?)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*?)</span>')
# 找到影片的相关内容
findDb = re.compile(r'<p class="">(.*?)</p>', re.S)


# <img .* src="(.*?)" width="100"/>


def getData(base_url):
    datalist = []
    pools = get_ip()

    for i in range(0, 10):
        url = base_url.format(j=i * 25)
        logger.info(url)  # 显示每条url的信息
        num = random.randrange(3)
        da1 = pools[num]['ip']
        da2 = pools[num]['port']
        print('url地址为：', url)
        print(da1, da2, '///////////////////////////////////////////')
        html = askURL(url, da1, da2)  # 保存获取到的网页源码
        # break
        # 逐个网页进行解析
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_="item"):
            # print(item)
            data = []
            item = str(item)
            # print(item)
            # break  跳出循环

            link = re.findall(findLink, item)[0]  # 通过正则表达式查找
            data.append(link)
            imgSrc = re.findall(findImage, item)[0]
            data.append(imgSrc)

            title = re.findall(findTitle, item)
            if len(title) == 2:
                ctitle = title[0]
                data.append(ctitle)
                etitle = title[1].replace("/", "")  # 去掉无关的符号
                data.append(etitle)
            else:
                data.append(title[0])
                data.append(" ")  # 留空

            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judge = re.findall(findJudge, item)[0]
            data.append(judge)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace('。', "")
                data.append(inq)  # 添加概述
            else:
                data.append(" ")
            db = re.findall(findDb, item)[0]
            db = re.sub(r'<br(\s+)?/>(\s+)?', " ", db)
            db = re.sub('/', " ", db)
            data.append(db.strip())  # 去掉空格
            # global logger
            # logger.info(data)
            print('获得第i条数据', data)
            datalist.append(data)  # 将每个电影的信息传入datalist
            # print(link)
    # for j in datalist:
    #     print(j)

    return datalist


def saveData(datalist, savepath):
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet1')
    col = ('电影详情链接', "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])

    for i in range(0, 250):
        print('第%d条' % i)
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    workbook.save(savepath)
    print('save........')


def saveData2DB(datalist, dbpath):
    # init_db(dbpath)
    print('正在执行写入数据库程序')
    print(len(datalist), '写入的数据库为', dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    print('连接数据库成功！')
    for data in datalist:
        for i in range(len(data)):
            if i == 4 or i == 5:
                continue
            data[i] = '"' + data[i] + '"'
        sql = '''
                insert into movie250 (info_link,pic_link,cname,ename,score,rated,introduction,info) values(%s)
            ''' % (",".join(data))
        print(sql)
        # global logger
        # logger.info(sql)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()

    print("ok")


def init_db(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    sql = '''
        create table movie250(
        id integer not null primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        introduction text,
        info text
        
        )
    '''
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 得到指定url网页内容
def askURL(url, ip, port):
    proxy_url = 'http://{0}:{1}'.format(ip, port)
    proxy_dict = {
        'http': proxy_url,
    }
    agent_lists = ['Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 '
                   'Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 '
                   'Safari/534.57.2',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 '
                   'Safari/535.11 SE 2.X MetaSr 1.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363 '
                   ]
    Cookie = 'bid=-nXoQdoKu6w; __yadk_uid=w1lYZp9vrSzsOrdLJ3c91po5kRF8i3Oj; ' \
             '__gads=ID=112a3ae8064962c9:T=1593224636:S=ALNI_MaKetmNKFK3x06Dq6YFQhUaswnbaA; ll="118210"; ' \
             '_vwo_uuid_v2=D26C4B3CAFE90CF4EF936EF2475779FF2|13eefe6a68b518488b8086e504a16ffa; douban-fav-remind=1; ' \
             'gr_user_id=8a45926a-01c9-49f5-b3b5-553fe9f7281c; _ga=GA1.2.185180075.1593224636; ' \
             '__utmv=30149280.21900; douban-profile-remind=1; viewed="3111224_5333562_30377532_11522125_30314653"; ' \
             '__utmz=30149280.1599569933.13.11.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(' \
             'not%20provided); dbcl2="219003272:AvIBYiupX6I"; _gid=GA1.2.1595072202.1602249674; ck=tkpo; ' \
             '__utma=30149280.185180075.1593224636.1599569933.1602249699.14; __utmc=30149280; __utmt=1; ' \
             '__utmt_douban=1; __utmc=223695111; ' \
             '_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1602249703%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ' \
             '_pk_ses.100001.4cf6=*; push_noty_num=0; push_doumail_num=0; __utmb=30149280.10.10.1602249699; ' \
             '__utma=223695111.1405734866.1593224636.1602249702.1602249772.7; __utmb=223695111.0.10.1602249772; ' \
             '__utmz=223695111.1602249772.7.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ' \
             '_pk_id.100001.4cf6=c78c29218d90e2a4.1593224635.6.1602249776.1598804188. '
    head = {"user-agent": agent_lists[random.randrange(9)], 'Cookie': Cookie}
    # html = ""     不应该是字符串类型
    try:
        html = requests.get(url, headers=head, proxies=proxy_dict).text
        # html = urllib.request.urlopen(req)
        # print("11111")
        # print(html.read().decode())
    except Exception as e:
        print(e)
    # except urllib.error.URLError as e:
    # if hasattr(e, "code"):
    #     print('++++++++++++++++++++++++++')
    #     print(e.code)
    # if hasattr(e, "reason"):
    #     print("---------------------------")
    #     print(e.reason)
    time.sleep(5)  # 防止ip被封
    print('########################################################')
    # print(html)

    # with open('hello.html', 'w') as f:
    #     f.write(html)
    return html


def user_proxy(proxy_addr, url):
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    html = urllib.request.urlopen(url)
    return html


# 为爬虫添加ip代理池
def get_ip():
    conn = pymysql.connect(host='localhost', user='root', passwd='rootpwd', db='spider')
    cursor = conn.cursor()
    sql = 'select * from proxy_ip'
    cursor.execute(sql)
    datas = cursor.fetchall()

    pools = []
    for data in datas:
        pool = {}
        print(data[1], data[2])  # 输出ip 和 port
        pool['ip'] = data[1]
        pool['port'] = data[2]
        pools.append(pool)
    conn.close()
    cursor.close()
    # http_url = 'http://www.baidu.com'
    # num = random.randrange(3)
    # ip = ips[num]
    # port = ports[num]
    # proxy_url = 'http://{0}:{1}'.format(ip, port)
    # proxy_dict = {
    #     'http': proxy_url,
    # }
    # try:
    #     response = requests.get(http_url, proxies=proxy_dict)
    # except Exception as e:
    #     print('出现错误了', e)
    return pools


if __name__ == '__main__':
    get_log()  # 显示log的内容
    main()
    # init_db("movietest.db")
    print("执行操作完毕")
