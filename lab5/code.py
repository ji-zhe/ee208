import web
from web import form
import urllib2
import os
import jieba


import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

def parseCommand(command):
    allowed_opt = ['title', 'site', 'contents']
    command_dict = {}
    opt = 'title'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict


def run(searcher, analyzer,command):
    if command == '':
        return
    command = " ".join(jieba.cut(command))
    command_dict = parseCommand(command)
    querys = BooleanQuery()
    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 10).scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    result = []
    for scoreDoc in scoreDocs:
        a = {}
        doc = searcher.doc(scoreDoc.doc)
        a['keywords']=doc.get('keywords')
        a['url'] = doc.get('url')
        a['title'] = doc.get('title').replace(' ','')
        result.append(a)
    return result
    ##            print explanation


urls = (
    '/', 'index',
    '/s', 's'
)


render = web.template.render('/mnt/hgfs/lab5/')# your templates

login = form.Form(
    form.Textbox('keyword'),
    form.Button('Search'),
)

def func(command):
    STORE_DIR = "index_html"
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    result = run(searcher, analyzer,command)
    return result

class index:
    def GET(self):
        f = login()
        return render.formtest(f)

class s:
    def GET(self):
        user_data = web.input()
        f = login()
        a = func(user_data.keyword)
        return render.result(user_data.keyword,a,f)

if __name__=='__main__':
	lucene.initVM(vmargs=['-Djava.awt.headless=true'])
	app = web.application(urls, globals())
	app.run()
