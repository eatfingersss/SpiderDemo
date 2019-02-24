# -*- encoding:utf-8 *-*
import os
import re
import random
from urllib import request
from bs4 import BeautifulSoup

ua_list = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
        ] 
user_agent = random.choice(ua_list)

URL='http://www.docin.com/p-816419878.html'


class DB(object):
    def __init__(self):
        self.province=''
        self.conn = pymysql.connect(host='', port=3306, user='', passwd='', db='',
                                    charset='utf8')
        self.cur = self.conn.cursor()
        #self.num = self.cur.execute()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        self.cur.close()


def get_page():
    url = URL
    response = get_response(url)
    page = response.read()
    page = page.decode("utf-8")
    # charset = chardet.detect(page)
    # page = page.decode(charset.get('encode'))
    # print(page)
    return page


def get_response(url):
    # url请求对象 Request是一个类
    url_request = request.Request(url)
    url_request.add_header('User-Agent', user_agent)
    # print("这个对象的方法是：",url_request.get_method())
    # print ('request:'+str(url_request))

    # 上下文管理器，HTTPResponse 对象，包含一系列方法
    try:
        urlResponse = request.urlopen(url)  # 打开一个url或者一个Request对象
    except Exception as e:
        print('The server couldnt fulfill the request.')
        print('Error code: ' + str(e))
        
    #    geturl()：返回 full_url地址
    #      info(): 返回页面的元(Html的meta标签)信息
    #      <meta>：可提供有关页面的元信息（meta-information），比如针对搜索引擎和更新频度的描述和关键词。
    #   getcode(): 返回响应的HTTP状态代码
    #   100-199 用于指定客户端应相应的某些动作。
    #   200-299 用于表示请求成功。      ------>  200
    #   300-399 用于已经移动的文件并且常被包含在定位头信息中指定新的地址信息。
    #   400-499 用于指出客户端的错误。  ------>  404
    #   500-599 用于支持服务器错误。
    #      read(): 读取网页内容，注意解码方式(避免中文和utf-8之间转化出现乱码)
    # '''
    # print (url_response)

    return urlResponse  # 返回这个对象


def main():
    html = get_page()
    soup = BeautifulSoup(html, "html.parser")
    print('begin to work')
    for link in soup.find_all('p', {'class': re.compile('reader-word-layer reader-word-s3-[0-9]?[0-9]')}):
        print(link.string)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e))
    os.system('PAUSE')
