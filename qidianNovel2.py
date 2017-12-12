# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
from lxml import etree
import pymongo
from urllib.request import Request,ProxyHandler
from qidianNovelcomment import PublicSpider
from urllib.request import build_opener

client = pymongo.MongoClient(host="127.0.0.1")
db = client.QiDian
collection = db.novels


import redis        #导入redis数据库
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

def getseClassFind(bookid,url):
    html = PublicSpider(url)#封装的一个方法


    selector = etree.HTML(html)
    secItems = selector.xpath('//div[@class="sub-type"]/dl[@class=""]/dd[@class=""]/a')
    for secItem in secItems:
        url = secItem.get('href')  # 得到url
        title = secItem.text
        print(url)
        print(title)
        bookid = collection.insert({'bookname': title, 'pid': bookid})
        Novelnameurl = '%s,%s' % (bookid, url)  # 拼串
        r.lpush('Novelnameurl', Novelnameurl)  # 入库