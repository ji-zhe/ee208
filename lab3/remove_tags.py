#!usr/bin/env python
import os
#import sys
import html2text

#reload(sys)
#sys.setdefaultencoding('utf-8')

for root, dirnames, filenames in os.walk("./html"):
    for filename in filenames:
        f = open(root+'/'+filename, 'r', encoding='utf8').read()
        f = html2text.html2text(f) 
        print(filename) 
        g = open('plaintext/'+filename, 'w', encoding='utf8')
        g.write(f)
        g.close()
