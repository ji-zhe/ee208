import requests
import bs4
from urllib.parse import urljoin
import sys
import re

def parseURL(url, content):
    urlset = set()
    soup = bs4.BeautifulSoup(content, 'html.parser')
    for a in soup.find_all('a',{'href':re.compile('^http|^/')}):
        if a.get('href'):
            urlset.add(urljoin(url, a.get('href')))
    return urlset
def write_outputs(urls, filename):
    with open(filename, 'w') as f:
        for url in urls:
            f.write(url)
            f.write('\n')


def main():
    #url = 'http://www.baidu.com'
    url = 'http://www.sjtu.edu.cn'
    if len(sys.argv) > 1:
        url = sys.argv[1]
    r = requests.get(url,headers = {'User-Agent':'Chrome'})
    r.raise_for_status()
    urls = parseURL(url, r.text)
    write_outputs(urls, 'res1.txt')


if __name__ == '__main__':
    main()
