import requests
import bs4
from urllib.parse import urljoin
import sys

def parseIMG(url, content):
    imgset = set()
    soup = bs4.BeautifulSoup(content, 'html.parser')
    for img in soup.findAll('img'):
        if img.get('src'):
            imgset.add(urljoin(url,img.get('src')))
    return imgset
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
    r = requests.get(url, headers = {'User-Agent': 'Chrome'})
    r.raise_for_status()
    urls = parseIMG(url, r.text)
    write_outputs(urls, 'res2.txt')


if __name__ == '__main__':
    main()
