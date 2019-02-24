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

urls=('http://tutor.eol.cn/web/school/result?type=3&speid=2418&school_id=110',
		'http://tutor.eol.cn/web/school/result/2?type=3&speid=2418&school_id=110',
		'http://tutor.eol.cn/web/school/result/3?type=3&speid=2418&school_id=110')
HOST='http://tutor.eol.cn'

class DB(object):
    def __init__(self):
        self.province=''
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='fortest',
                                    charset='utf8')
        self.cur = self.conn.cursor()
        #self.num = self.cur.execute()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
        self.cur.close()


def get_page(url):
    #url = 'http://maps7.com/china_province.php'  # sys.argv[1]  # input('>>')
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
   
    return urlResponse  # 返回这个对象

def get_detail(url):
	html = get_page(url)
	soup = BeautifulSoup(html, "html.parser")
	one = soup.find_all('div', {'class': re.compile('txt')})[0]#信息界面
	result='';
	for a in one.children:#为了混淆代码:-D
		result+=a.string
	return result
    

def out_(name,message):
    ret = conn.cur.execute("insert into tutor(name,message) values(%s,%s);", (name, message))
    print(name+':'+message)

def main():
	for uu in urls:
	    html = get_page(uu)
	    soup = BeautifulSoup(html, "html.parser")
	    print('begin to work...')
	    for target in soup.find_all('div', {'class': re.compile('grid list')}):#万一有多个
	    	for link in target.find_all('a'):#遍历每一个a标签
	    		try:
	    			name=''
		    		#print('get it:'+link.text+'#')
		    		url=HOST+link.get('href')#得到详细信息链接
		    		name=link.text#得到姓名
		    		message=get_detail(url)#得到详细信息
		    		print('get one：'+name+'...')
		    		out_(name,message)#入库
		    		print('done')
		    	except Exception as e:
		    		print(name+'not success:'+str(e))



if __name__ == "__main__":
    try:
        with DB() as conn:
            main()
    except Exception as e:
        print(str(e))
