#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/10 19:43
# @Author  : LLP
# @Site    : 
# @File    : SpiderDemo.py
# @Software: PyCharm

import sys
from bs4 import BeautifulSoup
import re
import urllib.request
import xlwt
import pymysql
import sqlite3

def main():
    print('开始爬取豆瓣top250电影信息')
    baseurl = 'https://movie.douban.com/top250?start='
    datalist = getData(baseurl)
    savepath = '.\\豆瓣电影top250.xls'
    # saveData(savepath,datalist)

    saveMysql(datalist)

# 创建正则表达式
findLink = re.compile(r'<a href="(.*?)">')  # 找链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)  # 找图片链接的规则，re.S 忽略换行符
findName = re.compile(r'<span class="title">(.*?)</span>') # 名字
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>') #评分
findComment = re.compile(r'<span>(\d*)人评价</span>') #评分
findFlag = re.compile(r'<span class="inq">(.*)</span>') #口号
findInfo = re.compile(r'<p class="">(.*)</p>\n<div class="star">',re.S) #口号
findOtherName = re.compile(r'<span class="other"> / (.*)</span>')
findDirector = re.compile(r'导演: (.*)主演:',re.S)
findActor = re.compile(r'主演: (.*)...<br/>',re.S)
findDesc = re.compile(r'...<br/>(.*)',re.S)
findList = [findName,findOtherName,findRating,findComment,findFlag,findLink,findImgSrc,findInfo]
# 获取数据
def getData(baseurl):
    dataList = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)
        soup = BeautifulSoup(html,'html.parser')
        for item in soup.find_all('div',class_ = "item"): # 查找符合要求的内容形成列表
            movie = []
            # html 转化成 String
            item = str(item)
            for i in range(0,len(findList)) :
                findItemList = re.findall(findList[i], item)
                if i == 0 :
                    if len(findItemList) == 2:
                        cName = findItemList[0]
                        movie.append(cName)
                        fName = findItemList[1].replace('/','')
                        movie.append(fName)
                    else :
                        movie.append(findItemList[0])
                        movie.append('')
                elif (len(findItemList) > 0):
                    movie.append(re.sub('\n*','',findItemList[0]))
                else:
                    movie.append('')
            # print(movie)
            # 处理电影信息问题，获取导演和主演
            movieInfo = str(movie[8]).lstrip()
            # print(movieInfo)
            movie.remove(movie[8])
            #print(re.findall(findDesc, movieInfo))
            director = ''
            actor = ''
            year = ''
            country = ''
            type = ''
            if (len(re.findall(findDirector, movieInfo))>0):
                director = re.findall(findDirector,movieInfo)[0]
                # print(director)
                movie.append(director)
            else:
                movie.append('')
            if (len(re.findall(findActor,movieInfo))>0):
                actor = re.findall(findActor,movieInfo)[0]
                actor = actor.replace('...<br/>','').replace('/','')
                # print(actor)
                movie.append(actor)
            else:
                movie.append('')
            if (len(re.findall(findDesc,movieInfo))>0):
                desc = re.findall(findDesc,movieInfo)[0].strip()
                descList = str(desc).split('/')
                if (len(descList)==3):
                    year = descList[0]
                    country = descList[1]
                    type = descList[2]
                elif (len(descList) == 2):
                    year = descList[0]
                    country = descList[1]
                elif (len(descList) == 1):
                    year = descList[0]
                movie.append(year)
                movie.append(country)
                movie.append(type)
            dataList.append(movie)
    return dataList
# 保存数据
def saveData(path,dataList):
   workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
   worksheet = workbook.add_sheet('豆瓣Top250',cell_overwrite_ok=True)
   col = ("序号","电影名称","外文名称","其他名称","豆瓣评分","评论人数","概况","影片链接","图片链接","导演","主演","年份","国家","类型")
   for i in  range(0,len(col)):
       worksheet.write(0,i,col[i])
   #workbook.save(path)
   print(len(dataList))
   for i in range(0,len(dataList)):
       print("第%d个电影"%i)
       for j in range(0,len(list(dataList[i]))):
           if (j == 0):
               worksheet.write(i+1,0,i)
               worksheet.write(i+1,j+1,dataList[i][j])
           else:
            worksheet.write(i+1,j+1,dataList[i][j])
   workbook.save(path)
# 保存进mysql
def saveMysql(dataList):
    conn = pymysql.connect(
        host= 'localhost',
        user = 'root',
        passwd = '0522',
        database= 'lp',
        charset= 'utf8'
    )
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    for i in range(0,len(dataList)):
        tem = dataList[i]
        cur.execute("insert into movie values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    ,(str(i),tem[0],tem[1],tem[2],tem[3],tem[4],tem[5],tem[6],tem[7],tem[8],tem[9],tem[10],tem[11],tem[12]))
    cur.close()
    conn.commit()
    conn.close()

# 获取网页内容
def askURL(url):
    head = { # 模拟浏览器头部信息
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # header = [{ "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}]
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        return html
        # print(html)
    except Exception as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

if __name__ == '__main__':
    main()
