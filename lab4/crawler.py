# -*- coding:utf-8 -*-
from urllib.parse import urljoin
import re
import os
import sys
import requests
import BloomFilter

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    s = s[:min(len(s), 100)]#防止文件名过长产生错误
    return s

def get_page(page):
    try:
        r = requests.get(page,timeout = 1, stream=True, headers = {'User-Agent':'Chrome'})
        r.raise_for_status()
        if 'html' in r.headers['content-type']:
            r.encoding = r.apparent_encoding
            return r.text
        else:
            return ''
    except:
        return ''

def get_all_links(content, page):
    links = list()
    for tag in re.findall(r'<a.*?href=.*?</a>', content):
        mmm=re.search(r'''href=['"]?.*?['";\s]''',tag)
        if mmm:
            url = mmm.group()[5:-1].strip('"').strip("'")
            url = urljoin(page, url)
            if '://' in url:
                links.append(url)
    return links
        
def union_dfs(a,b):
    for e in b:
        if e not in a:
            a.append(e)
            
def union_bfs(a,b):
    for e in b:
        if e not in a:
            a.insert(0,e)
       
def add_page_to_folder(page, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'    #index.txt中每行是'网址 对应的文件名'
    folder = 'html'                 #存放网页的文件夹
    filename = valid_filename(page) #将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore').decode('ascii') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  #如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'wb')
    f.write((page+'\n').encode('utf8'))
    f.write(content.encode('utf8'))                #将网页存入文件
    f.close()
    
def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = BloomFilter.BloomFilter(5000, 0.01)
    graph = {}
    count = 0
    max_page = int(max_page)
    
    while tocrawl and count < max_page:
        page = tocrawl.pop()
        if page not in crawled:
            print(count, page)
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            globals()['union_' + method](tocrawl, outlinks)
            crawled.add(page)

            count += 1
            graph[page] = outlinks
            crawled.add(page)
    return graph, crawled

if __name__ == '__main__':

    seed = sys.argv[1]
    method = sys.argv[2]
    max_page = sys.argv[3]
    
    graph, crawled = crawl(seed, method, max_page)