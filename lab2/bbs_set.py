import requests
from bs4 import BeautifulSoup
import sys


def bbs_set(id, pw, text):

    bbs_session = requests.session()
    bbs_session.post("https://bbs.sjtu.edu.cn/bbslogin",{'id':id, 'pw':pw, 'submit':'login'})
    bbs_session.post("https://bbs.sjtu.edu.cn/bbsplan",{'type':'update','text':text})

    content = bbs_session.get('https://bbs.sjtu.edu.cn/bbsplan').text
    soup = BeautifulSoup(content,'html.parser')
    print(soup.find('textarea').string.strip())


if __name__ == '__main__':
	
    id = sys.argv[1]
    pw = sys.argv[2]
    text = sys.argv[3].encode('gbk')

    bbs_set(id, pw, text)