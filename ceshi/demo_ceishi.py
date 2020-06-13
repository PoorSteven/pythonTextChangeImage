# coding:utf-8
import requests
from bs4 import BeautifulSoup
import pymysql

#插入数据库
sql = "UPDATE table_name SET column1_name,column2_name2 WHERE some_column = some_name"
sql = "INSERT INTO Persons (LastName,Address) VALUE ('wilson','Champs-elysees')"
try:
    cursor.execute(sql)
    con.commit()
except:
    con.rollback()

    #插入数据库
    sql = "UPDATE table_name SET column1_name,column2_name2 WHERE some_column = some_name"
    sql = "INSERT INTO Persons (LastName,Address) VALUE ('wilson','Champs-elysees')"
    try:
        cursor.execute(sql)
        con.commit()
    except:
        con.rollback()