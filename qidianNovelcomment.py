from urllib.request import urlopen
from urllib.request import Request
import http.cookiejar
import urllib.request

#安装cookie
head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def PublicSpider(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req_timeout = 5
    req = Request(url=url, headers=headers)
    f = urlopen(req, None, req_timeout)
    s = f.read()
    html = s.decode("utf-8")
    return html
