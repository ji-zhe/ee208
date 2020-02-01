#!/usr/bin/env python

import web
from web import form
import urllib2
import os

INDEX_DIR = "IndexFiles.index"
import jieba
import sys, os, lucene
import re

from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'content' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def parseCommand(command):
    allowed_opt = ['site', 'title', 'content']
    command_dict = {}
    opt = 'title'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
            else:
                opt = 'title'
                command_dict[opt] = command_dict.get(opt, '') + ' ' + i
        else:
            opt = 'title'
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict

def run(searcher, analyzer, command):   
    command_dict = parseCommand(command)
    querys = BooleanQuery()
    for k,v in command_dict.iteritems():
        if k in ['title', 'content']:
            v= ' '.join(jieba.cut(v))
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 50).scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    result = list()
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
##            explanation = searcher.explain(query, scoreDoc.doc)
        a = dict()
        title = doc.get("title").replace(' ','')
        content = re.sub(r'''[a-zA-Z0-9\%\=\[\]\(\)'"\.\/\_\!\\\#\s]''','',doc.get("content"))
#            keywords = ' '.join(jieba.cut(command_dict['title'])).split(' ')
        keywords = list()
        if 'title' in command_dict:
            keywords += list(jieba.cut(command_dict['title']))[1:]
        if 'content' in command_dict:
            keywords += list(jieba.cut(command_dict['content']))[1:]
        beginning = max(map(content.find, keywords))
        if beginning<0:
            continue
        context = content[max(0, beginning-10): beginning+50]
        for keyword in keywords:
            #print "keyword", keyword
            context = context.replace(keyword.strip(), '<span style="color:red;font-weight:bold">'+keyword+"</span>")
            #print "original title: ", title
            title = title.replace(keyword.strip(), '<span style="color:red;font-weight:bold">'+keyword+"</span>") 
            #print "final title", title

        a['context'] = context
        a['title'] = title
        a['url'] = doc.get("url")
        result.append(a)
    return result
        #print 'language:', doc.get('language')
##            print explanation


urls = (
    '/', 'index',
    '/s', 's'
)


render = web.template.render('templates') # your templates

login = form.Form(
    form.Textbox('keyword'),
    form.Button('Search'),
)

def func(command):
    STORE_DIR = "index_html"
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    return run(searcher, analyzer, command)

class index:
    def GET(self):
        f = login()
        return render.formtest(f)

class s:
    def GET(self):
        user_data = web.input()
        f = login()
        if 'keyword' not in user_data or not user_data['keyword']:
            return render.formtest(f)
        a = func(user_data.keyword)
        return render.result(user_data, a, f)

if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    app = web.application(urls, globals())
    app.run()

    
