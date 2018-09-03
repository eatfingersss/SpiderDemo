# -*- encoding:utf-8 *-*
import random
import math
import os
import chardet
from urllib import request


def getPage():
    url = input('>>')
    response = getResponse(url)
    page = response.read()
    charset = chardet.detect(page)
    page = page.decode(charset.get('encode'))
    return page


def getResponse(url):
    # url请求对象 Request是一个类
    url_request = request.Request(url)
    # print("这个对象的方法是：",url_request.get_method())
    # print ('request:'+str(url_request))

    # 上下文管理器，HTTPResponse 对象，包含一系列方法
    url_response = request.urlopen(url)  # 打开一个url或者一个Request对象
    # '''
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

    return url_response  # 返回这个对象


def main():
    html=getPage()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e))
        # os.system('PAUSE')
