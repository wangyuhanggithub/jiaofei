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

# proxy = {'https': '144.52.215.39:808'}
# proxy_support = ProxyHandler(proxy)
# opener = build_opener(proxy_support)

client = pymongo.MongoClient(host="127.0.0.1")
db = client.QiDian            #库名dianping
collection = db.Novel          #表名classification


import redis        #导入redis数据库
r = redis.Redis(host='127.0.0.1', port=6379, db=0)


def Public(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}    #协议头
    req_timeout = 5
    req = Request(url=url, headers=headers)
    f = urlopen(req, None, req_timeout)
    s = f.read()
    s = s.decode("utf-8")
    # beautifulsoup提取
    soup = BeautifulSoup(s, 'html.parser')
    links = soup.find_all(name='div', class_="work-filter type-filter")
    for link in links:

        selector = etree.HTML(str(link))
        indexTitleUrls = selector.xpath('//ul[@type="category"]/li[@class=""]/a/@href')
        # 获取一级类别url和title
        for Novelurl in indexTitleUrls:
            print(Novelurl)
            r.lpush('Novelurl',Novelurl)
        indexTitles = selector.xpath('//ul[@type="category"]/li[@class=""]/a/text()')
        for title in indexTitles:
            print(title)
            bookid = collection.insert({'bookname': title, 'pid': None})
            getseClassFind(selector, bookid)

    a = r.lrange('Novelurl', 0, -1)
    for item in a:
        Novelurls = bytes.decode(item)

        arr = Novelurls.split(',')  # 分割字符串
        print(arr[0])
        getseClassFind(arr[0])

def getseClassFind(bookid,url):
    db = client.QiDian  # 库名dianping
    collection = db.novelname
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



Public('https://www.qidian.com/all')
