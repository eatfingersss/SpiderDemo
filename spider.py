# -*- encoding:utf-8 *-*
import re
import random
import sys
import math
import os
import chardet
from urllib import request
from bs4 import BeautifulSoup

ua_list = [ "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
            ]
user_agent = random.choice(ua_list)


def getPage():
    url =sys.argv[1]#input('>>')
    response = getResponse(url)
    page = response.read()
    page = page.decode("utf-8")
    #charset = chardet.detect(page)
    #page = page.decode(charset.get('encode'))
    #print(page)
    return page


def getResponse(url):
    # url请求对象 Request是一个类
    url_request = request.Request(url)
    url_request.add_header('User-Agent', user_agent)
    # print("这个对象的方法是：",url_request.get_method())
    # print ('request:'+str(url_request))

    # 上下文管理器，HTTPResponse 对象，包含一系列方法
    try:
        url_response = request.urlopen(url)  # 打开一个url或者一个Request对象
    except Exception as e:
        print('The server couldnt fulfill the request.')
        print('Error code: ', e.code)
        exit()
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

    return url_response  # 返回这个对象


def main():
    html=getPage()
    soup = BeautifulSoup(html,"html.parser")
    for link in soup.find_all('h4'):#'a',name_=re.compile(r'[0-9]?[0-9]')):
        #print('getit')
        print(link.string)
        #temp=link.next_sibling
        for element in link.next_siblings:
            print('\t'+element.string)
        #while True:
            #print('\t'+temp.text)
            #temp=temp.next_s
            try:
                if 'element.name' in vars() :
                    break
            except:
                continue

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e))
        # os.system('PAUSE')
