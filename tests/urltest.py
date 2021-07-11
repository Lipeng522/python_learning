#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/10 20:35
# @Author  : LLP
# @Site    : 
# @File    : urltest.py
# @Software: PyCharm

import urllib.request
response = urllib.request.urlopen("http://www.baidu.com")

print(response.read().decode('utf-8'))
