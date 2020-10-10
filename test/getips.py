#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2020-8-9 23:11:00
# version: 1.0
# __author__: zhilong
import pymysql
import requests
import logging
import os
import xlwt

logging.basicConfig(
    filename=os.path.join(os.getcwd(), 'all.log'),
    level=logging.INFO,
    format='%(asctime)s %(filename)s %(levelname)s %(message)s',  # 定义输出log的格式
    filemode='a',
    datefmt='%Y/%m/%d %H:%M:%S'
)

dicts_list = []


def get_ips():
    conn = pymysql.connect(host='localhost', user='root', passwd='rootpwd', db='spider')
    cursor = conn.cursor()
    sql = 'select * from proxy_ip order by id asc LIMIT 31'
    cursor.execute(sql)
    conn.commit()
    datas = cursor.fetchall()
    for data in datas:
        dicts = {}
        print(data[1], data[2])  # 打印到控制台，方便查看ip port
        logging.info(data)
        dicts['ip'] = data[1]
        dicts['port'] = data[2]
        dicts_list.append(dicts)
    # print(dicts, '======================')
    conn.close()
    cursor.close()
    return dicts_list


def test(lists):
    for ls in lists:
        print(ls)
        http_url = 'http://www.baidu.com'
        proxy_url = 'http://{0}:{1}'.format(ls['ip'], ls['port'])
        proxy_dict = {
            'http': proxy_url,
        }
        try:
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print(ls['ip'], '无效ip值')
            delete(ls['ip'])
        else:

            if 200 <= response.status_code < 300:
                print(ls['ip'], '有效ip值')
            else:
                print(ls['ip'], '无效ip值')
                delete(ls['ip'])


def delete(ip):
    conn = pymysql.connect(host='localhost', user='root', passwd='rootpwd', db='spider')
    cursor = conn.cursor()
    sql = 'delete from proxy_ip where ip = "{0}"'.format(ip)
    print('sql语句', sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    cursor.close()


def write_ip(ip):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet01')


if __name__ == '__main__':
    ips = get_ips()
    # 测试列表中的ip数值是否正确
    # for i in ips:
    #     for k, v in i.items():
    #         print(k, v)
    print('------------------------')
    # # print(ips[0]['ip'], ips[0]['port'])  # 取到了ip 和 port的数据
    test(ips)
