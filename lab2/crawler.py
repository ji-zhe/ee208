# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os
import sys
import requests

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s[:min(100, len(s))]

def get_page(page):
    try:
        r = requests.get(page,timeout = 1, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'})
        r.raise_for_status()
        return r.content
    except:
        return b''

def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content, 'html.parser', from_encoding='gbk')
    for a in soup.findAll('a'):
        temp = urljoin(page, a.get('href'))
        if re.compile('^http').match(temp):
            links.append(temp)
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
    f.write(content)                #将网页存入文件
    f.close()
    
def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0
    max_page = int(max_page)
    
    while tocrawl and count < max_page:
        page = tocrawl.pop()
        if page not in crawled:
            print(page)
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            globals()['union_' + method](tocrawl, outlinks)
            crawled.append(page)

            count += 1
            graph[page] = outlinks
            crawled.append(page)
    return graph, crawled

if __name__ == '__main__':

    seed = sys.argv[1]
    method = sys.argv[2]
    max_page = sys.argv[3]
    
    graph, crawled = crawl(seed, method, max_page)