#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "zhihu")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO hot_list (ranking,title,link,heat) VALUES ('1','1','1','1')"
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