#-*- coding:utf-8 -*-
import psycopg2
conn = psycopg2.connect(database='cobweb-prod',user='postgres',password='root',host='124.16.138.75',port='5432')
cur = conn.cursor()
cur.execute("SELECT * FROM table1 LIMIT 10")
rows = cur.fetchall()
print(rows)
conn.commit()
cur.close()
conn.close()