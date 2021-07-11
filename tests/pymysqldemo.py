#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/11 21:55
# @Author  : LLP
# @Site    : 
# @File    : pymysqldemo.py
# @Software: PyCharm

import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='0522'
)

cur = conn.cursor()
cur.execute("create database if not exists pytest")
cur.execute("insert into lp.student values(%s,%s,%s)",('lp','20','play'))
cur.close()
conn.commit()