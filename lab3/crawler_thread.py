# -*- coding:utf-8 -*-
#!usr/bin/python3
from urllib.parse import urljoin
import re
import os
import sys
import requests
import threading
import queue
import time
import BloomFilter

count = 0
num_of_thread = 7
q = queue.Queue()
varlock = threading.Lock()
indexlock = threading.Lock()
htmllock = threading.Lock()
bflock = threading.Lock()
cntlock = threading.Lock()
printed = False

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
        url = re.search(r'''href=['"]?.*?['";\s]''',tag).group()[5:-1].strip('"').strip("'")
        url = urljoin(page, url)
        if '://' in url:
            links.append(url)
    return links
       
def add_page_to_folder(page, content): #将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'    #index.txt中每行是'网址 对应的文件名'
    folder = 'html'                 #存放网页的文件夹
    filename = valid_filename(page) #将网址变成合法的文件名
    indexlock.acquire()
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore').decode('ascii') + '\t' + filename + '\n')
    index.close()
    indexlock.release()
    htmllock.acquire()
    if not os.path.exists(folder):  #如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'wb')
    f.write((page+'\n').encode('utf8'))
    title = re.search(r'<title>.*?</title>', content)
    if title:
        title = title.group()[7:-8]
    else:
        title = ''
    f.write((title+'\n').encode('utf8'))
    f.write(content.encode('utf8'))                #将网页存入文件
    f.close()
    htmllock.release()
    
def crawl():
    global count, printed, bf
    
    while count < max_page:
        #try:
            page = q.get()
            if page not in bf:
                cntlock.acquire()
                print(count, page)
                cntlock.release()
                content = get_page(page)
                if not content:
                    continue
                add_page_to_folder(page, content)
                outlinks = get_all_links(content, page)
                for link in outlinks:
                    q.put(link)
                bflock.acquire()
                bf.add(page)
                bflock.release()
                cntlock.acquire()
                count += 1
                cntlock.release()
        #except:
        #    if not printed:
        #        printed = True
        #        print("\nTask done: No more URLs for the task.")
        #    break
    if not printed:
        printed = True
        print("\nTask done: Max number of pages reached.")  
    return



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Command should be: python    crawler_thread.py    url_seed    max_page.")
        print("Exit.")
        quit()
    seed = sys.argv[1]
    max_page = int(sys.argv[2])
    q.put(seed)
    task_list = list()
    bf = BloomFilter.BloomFilter(max_page, 0.1)

    for i in range(num_of_thread):
        t = threading.Thread(target=crawl)
        task_list.append(t)

    for task in task_list:
        task.start()
    
    for task in task_list:
        task.join()
    print("time cost: {}s.".format(time.perf_counter()))
