#!/usr/bin/python3
# 使用说明只需要替换cookie变量的值为你的值

import pymysql
from lxml import etree
import requests
import time

nowTime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# 定义热榜类
class HotList():
    def __init__(self,ranking,title,link,heat,create_time):
        self.ranking = ranking
        self.title = title
        self.link = link
        self.heat = heat
        self.create_time = create_time

cookie='_zap=69801e0d-25a8-4951-a3fc-bf9e5c95cbfa; d_c0="AFDml21tKg6PTlmiAwKJWuwRvGXIPMpZJv0=|1536145426"; _ga=GA1.2.141879976.1536502460; UM_distinctid=16aee4f58fe4f4-0a307826c74beb-37657e03-13c680-16aee4f58ff67a; z_c0="2|1:0|10:1559910214|4:z_c0|92:Mi4xT1dXbEFnQUFBQUFBVU9hWGJXMHFEaVlBQUFCZ0FsVk5ScVhuWFFCb044VHR4RXFNa3VJOFB2TWQxUjBVN01feVZ3|6f9bd7cec0f5f0940a6e2331efb502218d55df51b46c78cd6c36d5505b900c8a"; _xsrf=838066d9-d505-4072-963d-89543b92255c; __utma=51854390.141879976.1536502460.1559822185.1562169869.19; __utmc=51854390; __utmz=51854390.1562169869.19.12.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=51854390.100--|2=registration_date=20160220=1^3=entry_date=20160220=1; q_c1=0c1798f5916b441fbafd1e9ecf1366c9|1562509819000|1536502456000; tgw_l7_route=a37704a413efa26cf3f23813004f1a3b; CNZZDATA1272960301=1874253637-1558773511-https%253A%252F%252Fwww.google.com.hk%252F%7C1562972018; tst=h; tshl='

url = "https://www.zhihu.com/hot"
headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Cookie": cookie
}

response = requests.get(url, headers=headers)
html_str = response.content.decode()
html = etree.HTML(html_str)
print(html)

#获取知乎排名、标题、链接、标题热度
ret = html.xpath("//section[@class='HotItem']")
# print(ret)

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "zhihu")

for table in ret:
    ranking = table.xpath(".//div[@class='HotItem-index']/div/text()")[0]
    title = table.xpath(".//div[@class='HotItem-content']/a/@title")[0]
    link = table.xpath(".//div[@class='HotItem-content']/a/@href")[0]
    ## 热度的class可能出现HotItem-metrics HotItem-metrics--bottom或HotItem-metrics，因此加以判断
    hot1 = table.xpath(".//div[@class='HotItem-metrics HotItem-metrics--bottom']/text()")
    hot2 = table.xpath(".//div[@class='HotItem-metrics']/text()")
    if len(hot1) == 0:
        heat = hot2[0]
    else:
        heat = hot1[0]


    hotList = HotList(ranking,title,link,heat,nowTime)

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sql = "INSERT INTO hot_list (ranking,title,link,heat,create_time) VALUES ('" + ranking + "', '" + title + "', '" + link + "', '" + heat + "','" + nowTime + "')"
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

# 关闭数据库连接
db.close()