# -*- encoding:utf-8 *-*
import random
import math
import os
import chardet
from urllib import request
from bs4 import BeautifulSoup
from sys import argv

url = 'http://www.iciba.com/'


# url='https://fanyi.baidu.com/translate#en/zh/'

def getResponse(url):
    url_request = request.Request(url)
    # url_request.add_header(header)
    url_response = request.urlopen(url)  # 打开一个url或者一个Request对象
    return url_response  # 返回这个对象


def main(words):

    print('开始获取: ', end='')
    response = getResponse(url + words)
    page = response.read()
    charset = chardet.detect(page)
    html = page.decode('utf-8')  # (charset.get('encoding'))
    soup = BeautifulSoup(html, "html.parser")

    target = soup.find_all('div', {'class': 'base-speak'})
    if target.__len__() == 0:
        raise Exception('一无所获')
    target = str(target[0].contents[3].contents[1].text)[2:]  # 选取美式发音('美 [bʊk]')
    # target = target[1]  # 选取美式发音
    # ps = target.find('b')  # 遍历第一个b标签
    print('得到' + words + '的音标:' + target, end='')
    return target


if __name__ == "__main__":
    try:
        main('book')
    except Exception as e:
        print(str(e))
        # os.system('PAUSE')
