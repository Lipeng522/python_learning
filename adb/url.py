'''BeatifulSoup4 将复杂的html转换成树形结构，每个节点都是python对象，所有对象都可以归纳为四种
Tag # 标签及其内容，默认找到的第一个内容
NavigableString   # 标签里的内容（字符串）
BeautifulSoup   # 表示整个文档
Comment # 注释
'''

# 文档的遍历
print(bs.head.content)

# 文档的搜索,用的更为频繁







from bs4 import BeautifulSoup
file = open('https://movie.douban.com/top250','rb')
html= file.read()
bs=BeautifulSoup(html,'html.parser')
print(bs.title)
print(bs.head)
print(bs.title.string)

