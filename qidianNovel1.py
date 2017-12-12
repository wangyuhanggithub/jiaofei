# -*- coding: utf-8 -*-
import re
import requests
from time import sleep, ctime
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
from lxml import etree
from qidianNovel2 import getseClassFind

import redis

r = redis.Redis(host='192.168.60.112', port=6379, db=0, charset='utf-8')

a = r.lrange('Novelurl', 0, -1)
for item in a:
    Novelurls = bytes.decode(item)

    arr = Novelurls.split(',')  # 分割字符串
    print(arr[0])
    getseClassFind(arr[0])