# -*- encoding:utf-8 *-*
import re
import random
from urllib import request
from bs4 import BeautifulSoup
import pymysql

ua_list = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
           "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 "
           "Safari/535.11 "
           ]
user_agent = random.choice(ua_list)



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
    url = 'http://maps7.com/china_province.php'  # sys.argv[1]  # input('>>')
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


def iterable_judge(target):
    if target.next_sibling is not None:
        return target.next_siblings
    else:
        return target.parent.next_siblings


def out_province(string):
    conn.province = string
    ret = conn.cur.execute("insert into maps(name,type) values(%s,%s);", (string, 'province'))
    print(string+':'+str(ret))

def out_city(string):
    ret = conn.cur.execute("insert into maps(name,dependence,type) values(%s,%s,%s);", (string,conn.province, 'city'))
    print('\t'+string+':'+str(ret))

def main():
    html = get_page()
    soup = BeautifulSoup(html, "html.parser")
    print('begin to work')
    for link in soup.find_all('a', {'name': re.compile('[0-9]?[0-9]')}):
        out_province(link.string)  # province
        for element in iterable_judge(link):
            if element.name == 'hr':  # 只有省份的a标签有name属性
                break
            elif element.name is None:  # 过滤换行符
                continue
            out_city(element.string)  # city


if __name__ == "__main__":
    try:
        with DB() as conn:
            main()
    except Exception as e:
        print(str(e))
